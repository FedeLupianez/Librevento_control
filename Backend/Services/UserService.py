from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session, select
from Tablas import USUARIO
from fastapi import HTTPException
import bcrypt
import secrets


def create(session: Session, user: USUARIO) -> dict:
    """Function to create a new user
    Args:
        session (sqlmodel.Session): connection to the database
        user (Tablas.USUARIO): USUARIO class object to create
    """
    tempPassword = user.clave.encode("utf-8")
    print(user)
    # Hash the password
    hashedPassword = bcrypt.hashpw(tempPassword, bcrypt.gensalt())
    new_token_id = secrets.token_hex(16)
    user.clave = hashedPassword.decode("utf-8")
    user.token_id = new_token_id
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except IntegrityError as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=400, detail="Data constraint violation")
    except OperationalError as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error")
    return {"id": user.id_usuario}


def delete(session: Session, token_id: str) -> dict:
    """Function to delete a record from the user table
    Args:
        session (sqlmodel.Session): connection to the database
        token_id (str): token of the user
    """
    query = select(USUARIO).where(USUARIO.token_id == token_id)
    user = session.exec(query).first()

    if not (user):
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "user deleted successfully"}


def get(session: Session, token_id: str) -> dict:
    """Function to get a user record by its id
    Args:
        session (sqlmodel.Session): connection to the database
        token_id (str): id of the user to get
    """
    query = select(USUARIO).where(USUARIO.token_id == token_id)
    user = session.exec(query).first()
    if not (user):
        raise HTTPException(status_code=404, detail="User not found")
    session.refresh(user)
    return user.model_dump(exclude={"clave"})


def get_id(session: Session, user_email: str) -> dict:
    """Function to get a user record by its email
    Args:
        session (sqlmodel.Session): connection to the database
        user_email (str): email of the user to get
    """
    query = select(USUARIO.token_id).where(USUARIO.email == user_email)
    token = session.exec(query).first()
    if not (token):
        raise HTTPException(status_code=404, detail="user not found")
    return {"id": token}


def login(session: Session, user_email: str, password: str) -> dict:
    """Function to get a user record by its email
    Args:
        session (sqlmodel.Session): connection to the database
        user_email (str): email of the user to get
        password (str): password that the user entered
    """
    user = session.exec(select(USUARIO).where(USUARIO.email == user_email)).first()
    if not (user) or not bcrypt.checkpw(
        password.encode("utf-8"), user.clave.encode("utf-8")
    ):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    return user.model_dump(exclude={"clave", "id_usuario"})
