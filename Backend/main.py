from sqlmodel import create_engine
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException
import Tablas

# Carpeta de Services, (funciones para interactuar con la base de datos)
from Services import GeneradorService, UsuarioService

Config = dotenv_values("test.env")  # Configuraciones
engine = create_engine(
    f"{Config['ENGINE']}://{Config['USER']}:{Config['PASSWORD']}@{Config['HOST']}/{Config['DATABASE']}",
)  # motor para la base de datos
print("Base de datos conectada")


class Rutas:
    Generador = "/generador"
    Usuario = "/usuario"
    Login = "/login"


app = FastAPI()


# GENERADOR :
#   Página :
# endpoint para crear un generador
@app.post(Rutas.Generador)
def crear_generador(generador: Tablas.GENERADOR):
    try:
        return GeneradorService.crear(engine, generador)
    except HTTPException as error:
        print(error)


# endpoint para obtener un generador por su id
@app.get(Rutas.Generador)
def obtener_generador(id_generador: int):
    try:
        return GeneradorService.obtener(engine, id_generador)
    except HTTPException as error:
        print(error)


# endpoint para borrar un generador por su id
@app.delete(Rutas.Generador)
def borrar_generador(id_generador: int):
    try:
        return GeneradorService.borrar(engine, id_generador)
    except HTTPException as error:
        print(error)


#   Hardware :
@app.patch(Rutas.Generador + "/config_mac")
def config_macAddress(id_usuario: int, macAddress: str):
    try:
        return GeneradorService.config_macAddress(engine, id_usuario, macAddress)
    except HTTPException as error:
        print(error)


# Endpoints de usuario :
@app.post(Rutas.Usuario)
def crear_usuario(usuario: Tablas.USUARIO):
    try:
        return UsuarioService.crear(engine, usuario)
    except HTTPException as e:
        return e


@app.get(Rutas.Usuario)
def obtener_usuario(id_usuario: int):
    try:
        return UsuarioService.obtener(engine, id_usuario)
    except HTTPException as e:
        return e


@app.get(Rutas.Usuario)
def obtener_id(email_usuario: str):
    try:
        return UsuarioService.obtener_id(engine, email_usuario)
    except HTTPException as e:
        return e


@app.delete(Rutas.Usuario)
def borrar_usuario(id_usuario: int):
    try:
        return UsuarioService.borrar(engine, id_usuario)
    except HTTPException as e:
        return e


@app.get(Rutas.Login)
def login(email_usuario: str, clave: str):
    try:
        return UsuarioService.login(engine, email_usuario, clave)
    except HTTPException as e:
        return e
