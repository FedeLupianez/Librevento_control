from sqlmodel import Session, select, update, desc
from sqlalchemy.exc import IntegrityError, OperationalError
from Tablas import GENERADOR
from fastapi import HTTPException


def create(session: Session, generator: GENERADOR) -> dict:
    """Function to create a new generator
    Args:
        session (sqlmodel.Session): connection to the database
        generator (Tablas.GENERADOR): GENERADOR class object to upload
    """
    # Create the session with the database
    try:
        session.add(generator)  # Add the object to the session
        session.commit()  # Confirm the changes
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Data constraint violation")
    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error")
    return {"message": "generator created successfully"}


def delete(session: Session, id_generator: int) -> dict:
    """Function to delete a record from the generator table
    Args:
        session (sqlmodel.Session): connection to the database
        id_generator (int): id of the generator to delete
    """
    # Get the object (record) from the table by its id
    query = select(GENERADOR).where(GENERADOR.id_generador == id_generator)
    # Execute the query and get the object
    generator = session.exec(query).first()

    if not (generator):
        raise HTTPException(status_code=404, detail="generator not found")

    session.delete(generator)
    session.commit()
    return {"message": "generator deleted successfully"}


def get(session: Session, id_generator: int) -> GENERADOR:
    """Function to get a generator record
    Args:
        session (sqlmodel.Session): connection to the database
        id_generator (int): id of the generator to get
    """
    query = select(GENERADOR).where(GENERADOR.id_generador == id_generator)
    generator = session.exec(query).first()
    if not (generator):
        # Returns an error if it does not find the generator
        raise HTTPException(status_code=404, detail="Generator not found")

    return generator


def config_macAddress(session: Session, id_user: int, macAddress: str) -> dict:
    """Function to configure a macAddress of a generator in the database
    Args:
        session (sqlmodel.Session): connection to the database
        id_user (int): user id
        macAddress (str): device macAddress
    """
    query_generator = select(GENERADOR).where(GENERADOR.id_usuario == id_user).order_by(desc(GENERADOR.id_generador))
    generator = session.exec(query_generator).first()
    print(generator)
    if not (generator):
        raise HTTPException(status_code=404, detail="The user has no generators")

    query = (
        update(GENERADOR)
        .where(GENERADOR.id_generador == generator.id_generador)
        .values(mac_address=macAddress)
    )
    session.exec(query)
    session.commit()
    return {"message": "macAddress changed"}


def get_macAddress(session: Session, id_user: int) -> dict:
    """This function returns the macAddress of a user's generators, so it returns a list"""
    query = select(GENERADOR.mac_address).where(GENERADOR.id_usuario == id_user)
    macAddress = list(session.exec(query).all())
    if not (macAddress):
        raise HTTPException(status_code=404, detail="The user has no generators")
    return {"message": "macAddress obtained", "data": macAddress}
