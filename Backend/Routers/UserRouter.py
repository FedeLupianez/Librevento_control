from fastapi import APIRouter, Depends, HTTPException, Request, Response
from json import dumps, loads
import Tablas
from Services import UserService
from pydantic import BaseModel
from sqlmodel import Session
from dependencies import get_session, Config
import base64

router = APIRouter(prefix="/user", tags=["User"])

# --- Cookie Settings ---
# Configuration to see if the environment is local or production
IS_PROD = Config.get("ENVIRONMENT") == "production"
print(Config.get("ENVIRONMENT"))
# Domain for cookies in production
COOKIE_DOMAIN = Config.get("COOKIE_DOMAIN") if IS_PROD else None


# Función para setear todas las cookies
def set_all_cookies(response: Response, token_id: str, user_data: dict, max_age: int):
    # Auth token
    response.set_cookie(
        key="librevento_token_id",
        value=token_id,
        max_age=max_age,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
    )

    # User data en el frontend
    json_data = dumps(user_data)
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


# Login / logout endpoints:
class loginInput(BaseModel):
    user_email: str
    password: str


@router.post("/login")
async def login(
    data: loginInput,
    response: Response,
    session: Session = Depends(get_session),
):
    try:
        email = base64.b64decode(data.user_email).decode("utf-8")
        password = base64.b64decode(data.password).decode("utf-8")
        user = UserService.login(session, email, password)
        temp = {
            "name": user["nombre"],
            "gender": user["sexo"],
            "email": user["email"],
            "profile_picture": user["foto_perfil"],
        }
        max_age = 60 * 60 * 24 * 7  # 7 days

        set_all_cookies(response, user["token_id"], temp, max_age)
        print(user["token_id"])

        print("user logged in: ", temp)
        return {
            "message": "User logged in",
            "user": temp,
        }
    except HTTPException as error:
        print(error)
        raise error


@router.get("/auth")
async def is_logged_in(request: Request):
    token_id = request.cookies.get("librevento_token_id", None)
    if not token_id:
        raise HTTPException(status_code=401, detail="User not logged in")
    data = request.cookies.get("librevento_user", None)
    return {"message": "user logged in", "user": data}


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="librevento_token_id", path="/")
    response.delete_cookie(key="librevento_user", path="/")
    return {"message": "User logged out"}


# User endpoints:
@router.post("/create")
async def create_user(
    user: Tablas.USUARIO, response: Response, session: Session = Depends(get_session)
):
    try:
        newUser = UserService.create(session, user)
        print("new user: ", newUser)

        temp = {
            "name": user.nombre,
            "gender": user.sexo,
            "email": user.email,
            "profile_picture": user.foto_perfil,
        }
        max_age = 60 * 60 * 24 * 7  # 7 days

        set_all_cookies(response, newUser["token_id"], temp, max_age)

        return {"message": "User created", "user": temp}
    except HTTPException as error:
        print(error)
        raise error


@router.get("/get")
async def get_user(request: Request, session: Session = Depends(get_session)):
    token_id = request.cookies.get("librevento_token_id")
    if not token_id:
        raise HTTPException(status_code=404, detail="User not logged in")
    return UserService.get(session, token_id)


@router.get("/get_id")
async def get_id(
    request: Request, session: Session = Depends(get_session), email: str = ""
):
    result: str = ""
    if not email:
        cookie_value = request.cookies.get("librevento_user")
        if not cookie_value:
            raise HTTPException(status_code=404, detail="User not logged in")

        decoded_json = base64.b64decode(cookie_value).decode("utf-8")
        user_data = loads(decoded_json)
        user_email: str | None = user_data.get("email", None)
        if user_email:
            result = user_data["email"]
    else:
        result = email
    return UserService.get_id(session, user_email=result)


@router.delete("/delete")
async def delete_user(request: Request, session: Session = Depends(get_session)):
    token_id = request.cookies.get("librevento_token_id")
    if not token_id:
        raise HTTPException(status_code=404, detail="User not logged in")
    return UserService.delete(session, token_id)
