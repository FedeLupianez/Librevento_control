from fastapi import APIRouter, Depends, HTTPException, Request
import Tablas
from Services import UsuarioService
from pydantic import BaseModel
from sqlalchemy.engine import Engine
from dependencies import get_engine

router = APIRouter(prefix="/usuario", tags=["Usuario"])


# Endpoints de login / logout :
class loginInput(BaseModel):
    email_usuario: str
    clave: str


@router.post("/login")
async def login(
    data: loginInput, request: Request, engine: Engine = Depends(get_engine)
):
    try:
        usuario = UsuarioService.login(engine, data.email_usuario, data.clave)
        request.session["usuario"] = {
            "id_usuario": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "email_usuario": usuario["email"],
        }
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
    usuario: Tablas.USUARIO, request: Request, engine: Engine = Depends(get_engine)
):
    try:
        nuevoUsuario = UsuarioService.crear(engine, usuario)
        id_usuario: int = nuevoUsuario["id"]

        tempUsuario = UsuarioService.obtener(engine, id_usuario)
        request.session["usuario"] = {
            "id_usuario": tempUsuario["id_usuario"],
            "nombre": tempUsuario["nombre"],
            "email_usuario": tempUsuario["email"],
        }
        return {"message": "Usuario creado", "usuario": request.session["usuario"]}
    except HTTPException as error:
        print(error)
        raise error


@router.get("/")
async def obtener_usuario(id_usuario: int, engine: Engine = Depends(get_engine)):
    try:
        return UsuarioService.obtener(engine, id_usuario)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_id")
async def obtener_id(email_usuario: str, engine: Engine = Depends(get_engine)):
    try:
        return UsuarioService.obtener_id(engine, email_usuario)
    except HTTPException as error:
        print(error)
        raise error


@router.delete("/")
async def borrar_usuario(id_usuario: int, engine: Engine = Depends(get_engine)):
    try:
        return UsuarioService.borrar(engine, id_usuario)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/actual")
async def usuario_actual(request: Request):
    usuario = request.session.get("usuario")
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no logueado")
    print(usuario)
    return usuario
