from fastapi import APIRouter, Depends, HTTPException, Request, Response
from json import dumps, loads
import Tablas
from Services import UsuarioService
from pydantic import BaseModel
from sqlmodel import Session
from dependencies import get_session, Config
import base64

router = APIRouter(prefix="/usuario", tags=["Usuario"])

# --- Cookie Settings ---
# Configuración para ver si el entorno es local o de production
IS_PROD = Config.get("ENVIRONMENT") == "production"
print(Config.get("ENVIRONMENT"))
# Dominio para cookies en production
COOKIE_DOMAIN = Config.get("COOKIE_DOMAIN") if IS_PROD else None


# Helper function to set cookies consistently
def set_all_cookies(response: Response, token_id: str, user_data: dict, max_age: int):
    # Cookie for the auth token
    response.set_cookie(
        key="librevento_token_id",
        value=token_id,
        max_age=max_age,
        httponly=True,
        secure=IS_PROD,
        samesite="none" if IS_PROD else "lax",
        path="/",
    )

    # Cookie for frontend user data
    json_data = dumps(user_data)
    base64_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")
    response.set_cookie(
        key="librevento_user",
        value=base64_data,
        max_age=max_age,
        httponly=False,
        secure=IS_PROD,
        samesite="none" if IS_PROD else "lax",
        path="/",
    )


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
        max_age = 60 * 60 * 24 * 7  # 7 days

        set_all_cookies(response, usuario["token_id"], temp, max_age)

        print("usuario logueado : ", temp)
        return {
            "message": "Usuario logueado",
            "usuario": temp,
        }
    except HTTPException as error:
        print(error)
        raise error


@router.get("/is_logued")
async def is_logued(request: Request):
    token_id = request.cookies.get("librevento_token_id", None)
    if not token_id:
        raise HTTPException(status_code=401, detail="Usuario no logueado")
    data = request.cookies.get("librevento_user", None)
    return {"message": "usuario logueado", "usuario": data}


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="librevento_token_id", path="/", domain=COOKIE_DOMAIN)
    response.delete_cookie(key="librevento_user", path="/", domain=COOKIE_DOMAIN)
    return {"message": "Usuario deslogueado"}


# Endpoints de usuario :
@router.post("/")
async def crear_usuario(
    usuario: Tablas.USUARIO, response: Response, session: Session = Depends(get_session)
):
    try:
        nuevoUsuario = UsuarioService.crear(session, usuario)
        print("nuevo usuario : ", nuevoUsuario)

        temp = {
            "nombre": nuevoUsuario["nombre"],
            "sexo": nuevoUsuario["sexo"],
            "email": nuevoUsuario["email"],
            "foto_perfil": nuevoUsuario["foto_perfil"],
        }
        max_age = 60 * 60 * 24 * 7  # 7 days

        set_all_cookies(response, nuevoUsuario["token_id"], temp, max_age)

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
