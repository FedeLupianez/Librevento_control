from sqlmodel import create_engine
from dotenv import dotenv_values
from fastapi import FastAPI
import Tablas

# Carpeta de Services, (funciones para interactuar con la base de datos)
from Services import GeneradorService

Config = dotenv_values(".env")  # Configuraciones
engine = create_engine(
    f"{Config['ENGINE']}://{Config['USER']}:{Config['PASSWORD']}@{Config['HOST']}:{Config['PORT']}/{Config['DATABASE']}",
)  # motor para la base de datos
print("Base de datos conectada")


class Rutas:
    Generador = "/generador"
    Usuario = "/usuario"


app = FastAPI()


# GENERADOR :
#   Página :
# endpoint para crear un generador
@app.post(Rutas.Generador)
def crear_generador(generador: Tablas.GENERADOR):
    return GeneradorService.crear(engine, generador)


# endpoint para obtener un generador por su id
@app.get(Rutas.Generador)
def obtener_generador(id_generador: int):
    return GeneradorService.obtener(engine, id_generador)


# endpoint para borrar un generador por su id
@app.delete(Rutas.Generador)
def borrar_generador(id_generador: int):
    return GeneradorService.borrar(engine, id_generador)


#   Hardware :
@app.patch(Rutas.Generador + "/config_mac")
def config_macAddress(email_usuario: str, macAddress: str):
    return GeneradorService.config_macAddress(engine, email_usuario, macAddress)
