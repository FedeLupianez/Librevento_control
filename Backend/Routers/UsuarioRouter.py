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
            secure=True,
            samesite="none",
            path="/",
        )

        # Cookie del usuario para que la use el frontend
        json_data = dumps(temp)
        base64_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")

        response.set_cookie(
            key="librevento_user",
            value=base64_data,
            max_age=max_age,
            httponly=False,
            secure=True,
            samesite="none",
            path="/",
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
async def logout(response: Response):
    response.delete_cookie(key="librevento_token_id", path="/")
    response.delete_cookie(key="librevento_user", path="/")
    return {"message": "Usuario deslogueado"}


# Endpoints de usuario :
@router.post("/")
async def crear_usuario(
    usuario: Tablas.USUARIO, response: Response, session: Session = Depends(get_session)
):
    try:
        nuevoUsuario = UsuarioService.crear(session, usuario)
        print("nuevo usuario : ", nuevoUsuario)

        response.set_cookie(
            key="librevento_token_id",
            value=nuevoUsuario["token_id"],
            max_age=60 * 60 * 24 * 7,
            httponly=True,
            secure=True,
            samesite="none",
            path="/",
        )

        temp = {
            "nombre": nuevoUsuario["nombre"],
            "sexo": nuevoUsuario["sexo"],
            "email": nuevoUsuario["email"],
            "foto_perfil": nuevoUsuario["foto_perfil"],
        }
        base_64_data = dumps(temp)
        response.set_cookie(
            key="librevento_user",
            value=base_64_data,
            max_age=60 * 60 * 24 * 7,
            httponly=False,
            secure=True,
            samesite="none",
            path="/",
        )
        return {"message": "Usuario creado", "usuario": temp}
    except HTTPException as error:
        print(error)
        raise error


@router.get("/")
async def obtener_usuario(request: Request, session: Session = Depends(get_session)):
    token_id = request.cookies.get("librevento_token_id")
    if not token_id:
        raise HTTPException(status_code=404, detail="Usuario no logueado")
    return UsuarioService.obtener(session, token_id)


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
    token_id = request.cookies.get("librevento_token_id")
    if not token_id:
        raise HTTPException(status_code=404, detail="Usuario no logueado")
    return UsuarioService.borrar(session, token_id)
