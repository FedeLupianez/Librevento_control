from sqlmodel import Session, desc, select, update
from sqlalchemy.exc import IntegrityError, OperationalError
from Tablas import GENERADOR
from fastapi import HTTPException


def crear(session: Session, generador: GENERADOR) -> dict:
    """Función para crear un nuevo generador
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        generador (Tablas.GENERADOR) : objeto clase GENERADOR a subir
    """
    # Creo la sesión con la base de datos
    try:
        session.add(generador)  # Agrego el objeto a la session
        session.commit()  # Confirmo los cambios
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Violación de restricción de datos")
    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error en base de datos")
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado")
    return {"message": "generador creado exitosamente"}


def borrar(session: Session, id_generador: int) -> dict:
    """Función para borrar un registro de la tabla generador
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        macAddress (str) : dirección mac del dispositivo
    """
    # Obtengo el objeto (registro) de la tabla por su id (macAddress)
    query = select(GENERADOR).where(GENERADOR.id_generador == id_generador)
    # Ejecuto la query y obtengo el objeto
    generador = session.exec(query).first()

    if not (generador):
        raise HTTPException(status_code=404, detail="generador no encontrado")

    session.delete(generador)
    session.commit()
    return {"message": "generador borrado exitosamente"}


def obtener(session: Session, id_generador: int) -> GENERADOR:
    """Función para obtener un registro de generador
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        macAddress (str) : dirección mac del dispositivo a obtener
    """
    query = select(GENERADOR).where(GENERADOR.id_generador == id_generador)
    generador = session.exec(query).first()
    if not (generador):
        # Devuelve un error si no encuentra el generador
        raise HTTPException(status_code=404, detail="Generador no encontrado")

    return generador


def config_macAddress(session: Session, id_usuario: int, macAddress: str) -> dict:
    """Función para configurar una macAddress de un generador en la base de datos
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        id_usuario (int) : id del usuario
        macAddress (str) : macAddress del dispositivo
    """
    try :
        query = update(GENERADOR).where(GENERADOR.id_usuario == id_usuario).values(
            mac_address=macAddress
        )
    except Exception:
        raise HTTPException(status_code=404, detail="El usuario no tiene generadores")
    session.exec(query)
    session.commit()
    return {"message": "macAddress cambiada"}


def obtener_macAddress(session: Session, id_usuario: int) -> dict:
    """Esta función retorna la macAddress de los generadores de un usuario, así que devuelve una lista"""
    query = select(GENERADOR.mac_address).where(GENERADOR.id_usuario == id_usuario)
    macAddress = list(session.exec(query).all())
    if not (macAddress):
        raise HTTPException(status_code=404, detail="El usuario no tiene generadores")
    return {"message": "macAddress obtenidas", "data": macAddress}
