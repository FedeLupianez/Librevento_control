from fastapi import APIRouter, Depends, HTTPException, Request
from dependencies import get_session
from Services import GeneratorService, UserService
from sqlmodel import Session, select
import Tablas

router = APIRouter(prefix="/generator", tags=["Generator"])


# GENERATOR:
#   Page:
# endpoint to create a generator
@router.post("/create")
async def create_generator(
    generator: Tablas.GENERADOR, session: Session = Depends(get_session)
):
    try:
        return GeneratorService.create(session, generator)
    except HTTPException as error:
        print(error)
        raise error


# endpoint to get a generator by its id
@router.get("/get")
async def get_generator(id_generator: int, session: Session = Depends(get_session)):
    try:
        return GeneratorService.get(session, id_generator)
    except HTTPException as error:
        print(error)
        raise error


# endpoint to delete a generator by its id
@router.delete("/delete")
async def delete_generator(id_generator: int, session: Session = Depends(get_session)):
    try:
        return GeneratorService.delete(session, id_generator)
    except HTTPException as error:
        print(error)
        raise error


@router.get("/get_macaddress")
async def get_macAddress(request: Request, session: Session = Depends(get_session)):
    token_id = request.cookies.get("librevento_token_id")
    print(token_id)
    if not token_id:
        print("User not logged in")
        raise HTTPException(status_code=404, detail="User not logged in")
    id_user = UserService.get(session, token_id).get("id_usuario")
    if not id_user:
        print("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    return GeneratorService.get_macAddress(session, id_user)


#   Hardware:
@router.patch("/config_mac")
async def config_macAddress(
    user_email: str, macAddress: str, session: Session = Depends(get_session)
):
    user_id = UserService.get_id(session, user_email).get("id", None)
    print(user_id)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return GeneratorService.config_macAddress(session, user_id, macAddress)
