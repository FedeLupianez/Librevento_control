from fastapi import APIRouter, Depends, HTTPException, Request
from dependencies import get_session
from Services import GeneradorService, UsuarioService
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
async def obtener_macAddress(request: Request, session: Session = Depends(get_session)):
    token_id = request.cookies.get("librevento_token_id")
    print(request.cookies)
    print(token_id)
    if not token_id:
        print("Usuario no logueado")
        raise HTTPException(status_code=404, detail="Usuario no logueado")
    id_usuario = UsuarioService.obtener(session, token_id).get("id_usuario")
    if not id_usuario:
        print("Usuario no encontrado")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return GeneradorService.obtener_macAddress(session, id_usuario)


#   Hardware :
@router.patch("/config_mac")
async def config_macAddress(
    email_usuario: str, macAddress: str, session: Session = Depends(get_session)
):
    id_usuario = UsuarioService.obtener_id(session, email_usuario).get("id", None)
    if not id_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return GeneradorService.config_macAddress(session, id_usuario, macAddress)
