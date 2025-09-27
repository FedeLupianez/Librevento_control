from fastapi import APIRouter, Depends, HTTPException
import Tablas
from Services import MeasurementService
from sqlmodel import Session
from dependencies import get_session
from typing import Literal

router = APIRouter(prefix="/measurement", tags=["Measurement"])


# Endpoints for measurements:
@router.post("/")
async def create(measurement: Tablas.MEDICION, session: Session = Depends(get_session)):
    try:
        return MeasurementService.create(session, measurement)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/get_id")
async def get_measurement_id(macAddress: str, session: Session = Depends(get_session)):
    try:
        return MeasurementService.get_id(session, macAddress)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/get_voltages")
async def get_voltages(
    macAddress: str | None = None,
    filter_by: Literal["day", "hour"] | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    current_date: str | None = None,
    session: Session = Depends(get_session),
):
    try:
        return MeasurementService.get_voltages(
            session=session,
            mac_address=macAddress,
            filter_by=filter_by,
            min_date=min_date,
            max_date=max_date,
            current_date=current_date,
        )
    except HTTPException as error:
        print(error)
        raise error


@router.get("/get_consumptions")
async def get_consumptions(
    macAddress: str | None = None,
    filter_by: Literal["day", "hour"] | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    current_date: str | None = None,
    session: Session = Depends(get_session),
):
    try:
        return MeasurementService.get_consumptions(
            session=session,
            mac_address=macAddress,
            filter_by=filter_by,
            min_date=min_date,
            max_date=max_date,
            current_date=current_date,
        )
    except HTTPException as error:
        print(error)
        raise error
