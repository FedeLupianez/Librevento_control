from fastapi import APIRouter, Depends, HTTPException, Request, Response
from json import dumps, loads
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
    data: loginInput,
    response: Response,
    session: Session = Depends(get_session),
):
    try:
        email = base64.b64decode(data.email_usuario).decode("utf-8")
        clave = base64.b64decode(data.clave).decode("utf-8")
        usuario = UsuarioService.login(session, email, clave)
        temp = {
            "nombre": usuario["nombre"],
            "sexo": usuario["sexo"],
            "email": usuario["email"],
            "foto_perfil": usuario["foto_perfil"],
        }
        max_age = 60 * 60 * 24 * 7
        # Cookie del token de usuario para las peticiones
        response.set_cookie(
            key="librevento_token_id",
            value=usuario["token_id"],
            max_age=max_age,
            httponly=True,
            samesite="none",
        )

        # Cookie del usuario para que la use el frontend
        json_data = dumps(temp)
        base64_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")

        response.set_cookie(
            key="librevento_user",
            value=base64_data,
            max_age=max_age,
            httponly=False,
            samesite="lax",
        )
        print("usuario logueado : ", temp)
        return {
            "message": "Usuario logueado",
            "usuario": temp,
        }
    except HTTPException as error:
        print(error)
        raise error


@router.get("/logout")
async def logout(request: Request, response: Response):
    response.delete_cookie("librevento_user")
    response.delete_cookie("librevento_token_id")
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
async def obtener_usuario(request: Request, session: Session = Depends(get_session)):
    try:
        token_id = request.cookies["librevento_token_id"]
        return UsuarioService.obtener(session, token_id)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_id")
async def obtener_id(request: Request, session: Session = Depends(get_session)):
    cookie_value = request.cookies.get("librevento_user")
    if not cookie_value:
        raise HTTPException(status_code=404, detail="Usuario no logueado")

    decoded_json = base64.b64decode(cookie_value).decode("utf-8")
    user_data = loads(decoded_json)
    email = user_data["email"]

    return UsuarioService.obtener_id(session, email_usuario=email)


@router.delete("/")
async def borrar_usuario(request: Request, session: Session = Depends(get_session)):
    try:
        token_id = request.cookies["librevento_token_id"]
        return UsuarioService.borrar(session, token_id)
    except HTTPException as error:
        print(error)
        raise error
