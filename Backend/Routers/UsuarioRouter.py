from fastapi import APIRouter, Depends, HTTPException, Request
import Tablas
from Services import UsuarioService
from pydantic import BaseModel
from sqlmodel import Session
from dependencies import get_session
import base64

router = APIRouter(prefix="/usuario", tags=["Usuario"])


# Endpoints de login / logout :
class loginInput(BaseModel):
    email_usuario: str
    clave: str


@router.post("/login")
async def login(
    data: loginInput, request: Request, session: Session = Depends(get_session)
):
    try:
        email = base64.b64decode(data.email_usuario).decode("utf-8")
        clave = base64.b64decode(data.clave).decode("utf-8")
        usuario = UsuarioService.login(session, email, clave)
        request.session["usuario"] = {
            "token_id": usuario["token_id"],
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "foto_perfil": usuario["foto_perfil"],
            "sexo": usuario["sexo"],
        }
        print("usuario logueado : ", usuario)
        return {"message": "Usuario logueado", "usuario": request.session["usuario"]}
    except HTTPException as error:
        print(error)
        raise error


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Usuario deslogueado"}


# Endpoints de usuario :
@router.post("/")
async def crear_usuario(
    usuario: Tablas.USUARIO, request: Request, session: Session = Depends(get_session)
):
    try:
        nuevoUsuario = UsuarioService.crear(session, usuario)
        print("nuevo usuario : ", nuevoUsuario)

        request.session["usuario"] = {
            "token_id": nuevoUsuario["token_id"],
            "nombre": nuevoUsuario["nombre"],
            "email": nuevoUsuario["email"],
            "foto_perfil": nuevoUsuario["foto_perfil"],
        }
        return {"message": "Usuario creado", "usuario": request.session["usuario"]}
    except HTTPException as error:
        print(error)
        raise error


@router.get("/")
async def obtener_usuario(token_id: str, session: Session = Depends(get_session)):
    try:
        return UsuarioService.obtener(session, token_id)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_id")
async def obtener_id(email_usuario: str, session: Session = Depends(get_session)):
    try:
        email = base64.b64decode(email_usuario).decode("utf-8")
        return UsuarioService.obtener_id(session, email_usuario=email)
    except HTTPException as error:
        print(error)
        raise error


@router.delete("/")
async def borrar_usuario(token_id: str, session: Session = Depends(get_session)):
    try:
        return UsuarioService.borrar(session, token_id)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/actual")
async def usuario_actual(request: Request):
    usuario = request.session.get("usuario")
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no logueado")
    print("usuario devuelto : ", usuario)
    return usuario
