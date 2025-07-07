from fastapi import APIRouter, Depends, HTTPException
import Tablas
from Services import MedicionService
from sqlalchemy.engine import Engine
from dependencies import get_engine

router = APIRouter(prefix="/medicion", tags=["Medicion"])


# Endpoints para las mediciones:
@router.post("/")
async def crear(
    medicion: Tablas.MEDICION_POR_HORA, engine: Engine = Depends(get_engine)
):
    try:
        return MedicionService.crear(engine, medicion)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/id")
async def obtener(id_medicion: int, engine: Engine = Depends(get_engine)):
    try:
        return MedicionService.obtener(engine, id_medicion)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_id")
async def obtener_medicion_id(macAddress: str, engine: Engine = Depends(get_engine)):
    try:
        return MedicionService.obtener_id(engine, macAddress)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_voltajes")
async def obtener_voltajes(
    macAddress: str,
    id_generador: int | None = None,
    engine: Engine = Depends(get_engine),
):
    try:
        return MedicionService.obtener_voltajes(engine, macAddress, id_generador)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_consumos")
async def obtener_consumos(
    macAddress: str,
    id_generador: int | None = None,
    engine: Engine = Depends(get_engine),
):
    try:
        return MedicionService.obtener_consumos(engine, macAddress, id_generador)
    except HTTPException as error:
        print(error)
        raise error
