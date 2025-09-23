from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from Services import GeneradorService
from sqlmodel import Session, select
import Tablas

router = APIRouter(prefix="/generador", tags=["Generador"])


# GENERADOR :
#   Página :
# endpoint para crear un generador
@router.post("/")
async def crear_generador(
    generador: Tablas.GENERADOR, session: Session = Depends(get_session)
):
    try:
        return GeneradorService.crear(session, generador)
    except HTTPException as error:
        print(error)
        raise error


# endpoint para obtener un generador por su id
@router.get("/")
async def obtener_generador(id_generador: int, session: Session = Depends(get_session)):
    try:
        return GeneradorService.obtener(session, id_generador)
    except HTTPException as error:
        print(error)
        raise error


# endpoint para borrar un generador por su id
@router.delete("/")
async def borrar_generador(id_generador: int, session: Session = Depends(get_session)):
    try:
        return GeneradorService.borrar(session, id_generador)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/macAddress")
async def obtener_macAddress(token_id: str, session: Session = Depends(get_session)):
    id_usuario = session.exec(
        select(Tablas.USUARIO.id_usuario).where(Tablas.USUARIO.token_id == token_id)
    ).first()
    if not id_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return GeneradorService.obtener_macAddress(session, id_usuario)


#   Hardware :
@router.patch("/config_mac")
async def config_macAddress(
    id_usuario: int, macAddress: str, session: Session = Depends(get_session)
):
    try:
        return GeneradorService.config_macAddress(session, id_usuario, macAddress)
    except HTTPException as error:
        print(error)
        raise error
