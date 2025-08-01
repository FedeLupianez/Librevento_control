from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session, asc, select, func
from Tablas import MEDICION_POR_HORA, GENERADOR
from fastapi import HTTPException


def crear(session: Session, medicion: MEDICION_POR_HORA) -> dict:
    """Función para crear una nueva medicion
    engine (sqlalchemy.exc.engine) : conexión con la base de datos
    medicion (Tablas.MEDICION_POR_HORA) : objeto clase MEDICION_POR_HORA"""

    try:
        session.add(medicion)
        session.commit()
        session.refresh(medicion)
    except IntegrityError as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=400, detail="Violación de restricción de datos")
    except OperationalError as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Error en base de datos")
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=500, detail="Error inesperado")
    return {"message": "Medicion creada exitosamente"}


def obtener(session: Session, id_medicion: int) -> dict:
    query = select(MEDICION_POR_HORA).where(
        MEDICION_POR_HORA.id_medicion == id_medicion
    )
    medicion = session.exec(query).first()

    if not (medicion):
        raise HTTPException(status_code=404, detail="medicion no encontrada")
    session.refresh(medicion)
    return {"detail": "Medicion encontrada", "medicion": medicion.model_dump()}


def obtener_id(session: Session, macAddress: str) -> int:
    id = session.exec(
        select(GENERADOR.id_generador).where(GENERADOR.mac_address == macAddress)
    ).first()
    if not (id):
        raise HTTPException(status_code=404, detail="Generador no encontrado")
    return id


def obtener_voltajes(
    session: Session,
    macAddress: str,
    filter: str | None = None,
    id_generador: int | None = None,
) -> dict:
    id = id_generador or obtener_id(session, macAddress)

    if not filter:
        query = select(
            MEDICION_POR_HORA.voltaje_generado, MEDICION_POR_HORA.fecha
        ).where(MEDICION_POR_HORA.id_generador == id)
        query = query.order_by(asc(MEDICION_POR_HORA.fecha))
        query = query.order_by(asc(MEDICION_POR_HORA.hora))
    elif filter == "dia":
        query = (
            select(
                func.avg(MEDICION_POR_HORA.voltaje_generado),
                MEDICION_POR_HORA.fecha,
            )
            .where(MEDICION_POR_HORA.id_generador == id)
            .group_by(MEDICION_POR_HORA.fecha)
            .order_by(MEDICION_POR_HORA.fecha)
        )
    elif filter == "hora":
        query = (
            select(
                func.avg(MEDICION_POR_HORA.voltaje_generado),
                MEDICION_POR_HORA.hora,
            )
            .where(MEDICION_POR_HORA.id_generador == id)
            .group_by(MEDICION_POR_HORA.hora)
            .order_by(MEDICION_POR_HORA.hora)
        )

    resultado = session.exec(query).all()
    voltajes = [{"value": v, "timestamp": str(f)} for v, f in resultado]
    if not (voltajes):
        raise HTTPException(status_code=404, detail="Voltajes no encontrados")

    if len(voltajes) > 7:
        voltajes = voltajes[-7:]

    return {
        "detail": "Voltajes encontrados",
        "data": voltajes,
    }


def obtener_consumos(
    session: Session,
    macAddress: str,
    filter: str | None = None,
    id_generador: int | None = None,
) -> dict:
    id = id_generador or obtener_id(engine, macAddress)

    if not filter:
        query = select(MEDICION_POR_HORA.cosumo, MEDICION_POR_HORA.fecha).where(
            MEDICION_POR_HORA.id_generador == id
        )
        query = query.order_by(asc(MEDICION_POR_HORA.fecha))
        query = query.order_by(asc(MEDICION_POR_HORA.hora))
    elif filter == "dia":
        query = (
            select(
                func.avg(MEDICION_POR_HORA.consumo),
                MEDICION_POR_HORA.fecha,
            )
            .where(MEDICION_POR_HORA.id_generador == id)
            .group_by(MEDICION_POR_HORA.fecha)
            .order_by(MEDICION_POR_HORA.fecha)
        )
    elif filter == "hora":
        query = (
            select(
                func.avg(MEDICION_POR_HORA.consumo),
                MEDICION_POR_HORA.hora,
            )
            .where(MEDICION_POR_HORA.id_generador == id)
            .group_by(MEDICION_POR_HORA.hora)
            .order_by(MEDICION_POR_HORA.hora)
        )

    resultado = session.exec(query).all()
    consumos = [{"value": v, "timestamp": str(f)} for v, f in resultado]
    if not (consumos):
        raise HTTPException(status_code=404, detail="Consumos no encontrados")

    if len(consumos) > 7:
        consumos = consumos[-7:]

    return {
        "detail": "Consumos encontrados",
        "data": consumos,
    }
