from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session, select
from Tablas import MEDICION_POR_HORA
from fastapi import HTTPException


def crear(engine, medicion: MEDICION_POR_HORA) -> dict | HTTPException:
    """Función para crear una nueva medicion
    engine (sqlalchemy.exc.engine) : conexión con la base de datos
    medicion (Tablas.MEDICION_POR_HORA) : objeto clase MEDICION_POR_HORA"""

    with Session(engine) as session:
        try:
            session.add(medicion)
            session.commit()
            session.refresh(medicion)
        except IntegrityError as e:
            print(e)
            session.rollback()
            raise HTTPException(
                status_code=400, detail="Violación de restricción de datos"
            )
        except OperationalError as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=500, detail="Error en base de datos")
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(status_code=500, detail="Error inesperado")
        return {"message": "Medicion creada exitosamente"}


def obtener(engine, id_medicion: int):
    with Session(engine) as session:
        query = select(MEDICION_POR_HORA).where(
            MEDICION_POR_HORA.id_medicion == id_medicion
        )
        medicion = session.exec(query).first()

        if not (medicion):
            raise HTTPException(status_code=404, detail="medicion no encontrada")
        session.refresh(medicion)
        return {"detail": "Medicion encontrada", "medicion": medicion}
