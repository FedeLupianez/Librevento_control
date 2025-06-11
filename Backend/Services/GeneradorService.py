from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, OperationalError
from Tablas import GENERADOR
from fastapi import HTTPException


def crear(engine, generador: GENERADOR) -> None | HTTPException:
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
        except IntegrityError as e:
            session.rollback()
            return HTTPException(
                status_code=400, detail="Violación de restricción de datos"
            )
        except OperationalError as e:
            print(e)
            session.rollback()
            return HTTPException(status_code=500, detail="Error en base de datos")
        except Exception as e:
            print(e)
            session.rollback()
            return HTTPException(status_code=500, detail="Error inesperado")


def borrar(engine, id_generador: str) -> None | HTTPException:
    with Session(engine) as session:
        # Obtengo el objeto (registro) de la tabla por su id (macAddress)
        query = select(GENERADOR).where(GENERADOR.id_generador == id_generador)
        # Ejecuto la query y obtengo el objeto
        generador = session.exec(query).first()

        if not (generador):
            session.rollback()
            return HTTPException(status_code=404, detail="generador no encontrado")

        session.delete(generador)
        session.commit()


def obtener(engine, id_generador: str) -> GENERADOR | HTTPException:
    with Session(engine) as session:
        query = select(GENERADOR).where(GENERADOR.id_generador == id_generador)
        generador = session.exec(query).first()
        if not (generador):
            # Devuelve un error si no encuentra el generador
            return HTTPException(status_code=404, detail="Generador no encontrado")

        return generador
