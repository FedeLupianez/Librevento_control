from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Query
import json

Config = dotenv_values(".env")  # Configuraciones

base_datos_prueba = {}
with open("./mockdata.json", "r", encoding="utf-8") as archivo:
    base_datos_prueba: dict = json.load(
        archivo
    )  # Cargo el archivo con datos de ejemplo

USUARIO = base_datos_prueba["USUARIO"]
GENERADOR = base_datos_prueba["GENERADOR"]
MEDICION_POR_HORA = base_datos_prueba["MEDICION_POR_HORA"]

app = FastAPI()


@app.get("/generador/")
def get_id(user_id: int = Query(None, ge=0)):
    generadores: list[dict] = []
    for generador in GENERADOR:
        if generador["id_usuario"] != user_id:
            continue
        generadores.append(generador)
    if not (len(generadores)):
        return HTTPException(
            status_code=404, detail="El usuario no tiene generadores o no existe"
        )

    ultimo_id = 0
    for generador in generadores:
        if generador["id_generador"] > ultimo_id:
            ultimo_id = generador["id_generador"]
    return {"message": "generador encontrado", "id": ultimo_id}
