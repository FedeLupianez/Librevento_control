from sqlmodel import Session, desc, select
from sqlalchemy.exc import IntegrityError, OperationalError
from Tablas import GENERADOR
from fastapi import HTTPException


def crear(engine, generador: GENERADOR) -> dict | HTTPException:
    """Función para crear un nuevo generador
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        generador (Tablas.GENERADOR) : objeto clase GENERADOR a subir
    """
    # Creo la sesión con la base de datos
    with Session(engine) as session:
        try:
            session.add(generador)  # Agrego el objeto a la session
            session.commit()  # Confirmo los cambios
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Violación de restricción de datos"
            )
        except OperationalError:
            session.rollback()
            raise HTTPException(status_code=500, detail="Error en base de datos")
        except Exception:
            session.rollback()
            raise HTTPException(status_code=500, detail="Error inesperado")
        return {"message": "generador creado exitosamente"}


def borrar(engine, id_generador: int) -> dict | HTTPException:
    """Función para borrar un registro de la tabla generador
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        macAddress (str) : dirección mac del dispositivo
    """
    with Session(engine) as session:
        # Obtengo el objeto (registro) de la tabla por su id (macAddress)
        query = select(GENERADOR).where(GENERADOR.id_generador == id_generador)
        # Ejecuto la query y obtengo el objeto
        generador = session.exec(query).first()

        if not (generador):
            raise HTTPException(status_code=404, detail="generador no encontrado")

        session.delete(generador)
        session.commit()
        return {"message": "generador borrado exitosamente"}


def obtener(engine, id_generador: int) -> GENERADOR | HTTPException:
    """Función para obtener un registro de generador
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        macAddress (str) : dirección mac del dispositivo a obtener
    """
    with Session(engine) as session:
        query = select(GENERADOR).where(GENERADOR.id_generador == id_generador)
        generador = session.exec(query).first()
        if not (generador):
            # Devuelve un error si no encuentra el generador
            raise HTTPException(status_code=404, detail="Generador no encontrado")

        return generador


def config_macAddress(engine, id_usuario: int, macAddress: str) -> dict | HTTPException:
    """Función para configurar una macAddress de un generador en la base de datos
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        id_usuario (int) : id del usuario
        macAddress (str) : macAddress del dispositivo
    """
    with Session(engine) as session:
        query = (
            select(GENERADOR)
            .where(GENERADOR.id_usuario == id_usuario)
            .order_by(desc(GENERADOR.id_generador))
        )
        generador = session.exec(query).first()

        if not (generador):
            raise HTTPException(
                status_code=404, detail="El usuario no tiene generadores"
            )
        generador.macaddress = macAddress
        session.add(generador)
        session.commit()
        return {"message": "macAddress cambiada"}
