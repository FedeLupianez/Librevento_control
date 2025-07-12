from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_engine
from Services import GeneradorService
from sqlalchemy.engine import Engine
import Tablas

router = APIRouter(prefix="/generador", tags=["Generador"])


# GENERADOR :
#   Página :
# endpoint para crear un generador
@router.post("/")
async def crear_generador(
    generador: Tablas.GENERADOR, engine: Engine = Depends(get_engine)
):
    try:
        return GeneradorService.crear(engine, generador)
    except HTTPException as error:
        print(error)
        return error


# endpoint para obtener un generador por su id
@router.get("/")
async def obtener_generador(id_generador: int, engine: Engine = Depends(get_engine)):
    try:
        return GeneradorService.obtener(engine, id_generador)
    except HTTPException as error:
        print(error)
        return error


# endpoint para borrar un generador por su id
@router.delete("/")
async def borrar_generador(id_generador: int, engine: Engine = Depends(get_engine)):
    try:
        return GeneradorService.borrar(engine, id_generador)
    except HTTPException as error:
        print(error)
        return error


@router.get("/macAddress")
async def obtener_macAddress(id_usuario: int, engine: Engine = Depends(get_engine)):
    try:
        return GeneradorService.obtener_macAddress(engine, id_usuario)
    except HTTPException as error:
        print(error)
        return error


#   Hardware :
@router.patch("/config_mac")
async def config_macAddress(
    id_usuario: int, macAddress: str, engine: Engine = Depends(get_engine)
):
    try:
        return GeneradorService.config_macAddress(engine, id_usuario, macAddress)
    except HTTPException as error:
        print(error)
        return error
