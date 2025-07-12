from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session, asc, select
from Tablas import MEDICION_POR_HORA, GENERADOR
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


def obtener(engine, id_medicion: int) -> dict | HTTPException:
    with Session(engine) as session:
        query = select(MEDICION_POR_HORA).where(
            MEDICION_POR_HORA.id_medicion == id_medicion
        )
        medicion = session.exec(query).first()

        if not (medicion):
            raise HTTPException(status_code=404, detail="medicion no encontrada")
        session.refresh(medicion)
        return {"detail": "Medicion encontrada", "medicion": medicion}


def obtener_id(engine, macAddress: str) -> int | HTTPException:
    with Session(engine) as session:
        id = session.exec(
            select(GENERADOR.id_generador).where(GENERADOR.macaddress == macAddress)
        ).first()
        if not (id):
            raise HTTPException(status_code=404, detail="Generador no encontrado")
        return id


def obtener_voltajes(
    engine, macAddress: str, id_generador: int | None = None
) -> dict | HTTPException:
    with Session(engine) as session:
        id = id_generador or obtener_id(engine, macAddress)
        query = (
            select(MEDICION_POR_HORA.voltaje_generado)
            .where(MEDICION_POR_HORA.id_generador == id)
            .order_by(asc(MEDICION_POR_HORA.fecha))
            .order_by(asc(MEDICION_POR_HORA.hora))
        )
        resultado = session.exec(query).all()
        voltajes = list(resultado)
        if not (voltajes):
            raise HTTPException(status_code=404, detail="Voltajes no encontrados")

        return {"detail": "Voltajes encontrados", "data": voltajes}


def obtener_consumos(
    engine, macAddress: str, id_generador: int | None = None
) -> dict | HTTPException:
    with Session(engine) as session:
        id = id_generador or obtener_id(engine, macAddress)
        query = (
            select(MEDICION_POR_HORA.consumo)
            .where(MEDICION_POR_HORA.id_generador == id)
            .order_by(asc(MEDICION_POR_HORA.fecha))
            .order_by(asc(MEDICION_POR_HORA.hora))
        )
        resultado = session.exec(query).all()
        consumos = list(resultado)
        if not (consumos):
            raise HTTPException(status_code=404, detail="Consumos no encontrados")

        return {"detail": "Consumos encontrados", "data": consumos}
