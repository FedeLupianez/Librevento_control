from sqlmodel import create_engine
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import Tablas

# Carpeta de Services, (funciones para interactuar con la base de datos)
from Services import GeneradorService, UsuarioService, MedicionService

Config = dotenv_values(".env")  # Configuraciones
engine = create_engine(
    f"{Config['ENGINE']}://{Config['USER']}:{Config['PASSWORD']}@{Config['HOST']}/{Config['DATABASE']}",
)  # motor para la base de datos
print("Base de datos conectada")


class Rutas:
    Generador = "/generador"
    Usuario = "/usuario"
    Login = "/login"
    Medicion = "/medicion"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=Config["SECRET_KEY"])

# GENERADOR :
#   Página :
# endpoint para crear un generador
@app.post(Rutas.Generador)
async def crear_generador(generador: Tablas.GENERADOR):
    try:
        return GeneradorService.crear(engine, generador)
    except HTTPException as error:
        print(error)
        return error


# endpoint para obtener un generador por su id
@app.get(Rutas.Generador)
async def obtener_generador(id_generador: int):
    try:
        return GeneradorService.obtener(engine, id_generador)
    except HTTPException as error:
        print(error)
        return error


# endpoint para borrar un generador por su id
@app.delete(Rutas.Generador)
async def borrar_generador(id_generador: int):
    try:
        return GeneradorService.borrar(engine, id_generador)
    except HTTPException as error:
        print(error)
        return error


#   Hardware :
@app.patch(Rutas.Generador + "/config_mac")
async def config_macAddress(id_usuario: int, macAddress: str):
    try:
        return GeneradorService.config_macAddress(engine, id_usuario, macAddress)
    except HTTPException as error:
        print(error)
        return error


# Endpoints de usuario :
@app.post(Rutas.Usuario)
async def crear_usuario(usuario: Tablas.USUARIO, request: Request):
    try:
        nuevoUsuario = UsuarioService.crear(engine, usuario)
        id_usuario: int = nuevoUsuario["id"]

        tempUsuario = UsuarioService.obtener(engine, id_usuario)
        request.session["usuario"] = {
           "id_usuario": tempUsuario["id_usuario"],
           "nombre": tempUsuario["nombre"],
           "email_usuario": tempUsuario["email"]
        }
        return {"message": "Usuario creado", "usuario": request.session["usuario"]}
    except HTTPException as error:
        print(error)
        raise error


@app.get(Rutas.Usuario)
async def obtener_usuario(id_usuario: int):
    try:
        return UsuarioService.obtener(engine, id_usuario)
    except HTTPException as error:
        print(error)
        raise error


@app.get(Rutas.Usuario + '/id')
async def obtener_id(email_usuario: str):
    try:
        return UsuarioService.obtener_id(engine, email_usuario)
    except HTTPException as error:
        print(error)
        raise error


@app.delete(Rutas.Usuario)
async def borrar_usuario(id_usuario: int):
    try:
        return UsuarioService.borrar(engine, id_usuario)
    except HTTPException as error:
        print(error)
        raise error

class loginInput(BaseModel):
    email_usuario: str
    clave: str

@app.post(Rutas.Login)
async def login(data: loginInput, request: Request):
    try:
        usuario = UsuarioService.login(engine, data.email_usuario, data.clave)
        request.session['usuario'] = {
            "id_usuario": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "email_usuario": usuario["email"]
        }
        return {"message": "Usuario logueado", "usuario": request.session["usuario"]}
    except HTTPException as error:
        print(error)
        raise error

@app.get(Rutas.Usuario + '/actual')
async def usuario_actual(request: Request):
    usuario = request.session.get("usuario")
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no logueado")
    print(usuario)
    return usuario

@app.get(Rutas.Usuario + '/logout')
async def logout(request: Request):
    request.session.clear()
    return {"message": "Usuario deslogueado"}

# Endpoints para las mediciones:
@app.post(Rutas.Medicion)
async def crear(medicion: Tablas.MEDICION_POR_HORA):
    try:
        return MedicionService.crear(engine, medicion)
    except HTTPException as error:
        print(error)
        raise error

@app.get(Rutas.Medicion + '/id')
async def obtener(id_medicion: int):
    try:
        return MedicionService.obtener(engine, id_medicion)
    except HTTPException as error:
        print(error)
        raise error

@app.get(Rutas.Medicion + '/obtener_id')
async def obtener_id(macAddress: str):
    try:
        return MedicionService.obtener_id(engine, macAddress)
    except HTTPException as error:
        print(error)
        raise error

@app.get(Rutas.Medicion + '/obtener_voltajes')
async def obtener_voltajes(macAddress: str, id_generador: int | None = None):
    try:
        return MedicionService.obtener_voltajes(engine, macAddress, id_generador)
    except HTTPException as error:
        print(error)
        raise error


@app.get(Rutas.Medicion + '/obtener_consumos')
async def obtener_consumos(macAddress: str, id_generador: int | None = None):
    try:
        return MedicionService.obtener_consumos(engine, macAddress, id_generador)
    except HTTPException as error:
        print(error)
        raise error
