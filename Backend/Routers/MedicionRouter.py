from fastapi import APIRouter, Depends, HTTPException
import Tablas
from Services import MedicionService
from sqlmodel import Session
from dependencies import get_session
from typing import Literal

router = APIRouter(prefix="/medicion", tags=["Medicion"])


# Endpoints para las mediciones:
@router.post("/")
async def crear(medicion: Tablas.MEDICION, session: Session = Depends(get_session)):
    try:
        return MedicionService.crear(session, medicion)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_id")
async def obtener_medicion_id(macAddress: str, session: Session = Depends(get_session)):
    try:
        return MedicionService.obtener_id(session, macAddress)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_voltajes")
async def obtener_voltajes(
    macAddress: str | None = None,
    filtro: Literal["dia", "hora"] | None = None,
    fecha_minima: str | None = None,
    fecha_maxima: str | None = None,
    fecha_actual: str | None = None,
    session: Session = Depends(get_session),
):
    try:
        return MedicionService.obtener_voltajes(
            session=session,
            mac_address=macAddress,
            filtro=filtro,
            fecha_minima=fecha_minima,
            fecha_maxima=fecha_maxima,
            fecha_actual=fecha_actual,
        )
    except HTTPException as error:
        print(error)
        raise error


@router.get("/obtener_consumos")
async def obtener_consumos(
    macAddress: str,
    filter: str | None = None,
    id_generador: int | None = None,
    session: Session = Depends(get_session),
):
    try:
        return MedicionService.obtener_consumos(
            session, macAddress, filter, id_generador
        )
    except HTTPException as error:
        print(error)
        raise error
