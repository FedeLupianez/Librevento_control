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
    macAddress: str | None = None,
    filtro: str | None = None,
    id_generador: int | None = None,
    fecha_minima: str | None = None,
    fecha_maxima: str | None = None,
    fecha_actual: str | None = None,
) -> dict:
    if not id_generador and not macAddress:
        raise HTTPException(status_code=400, detail="No se proporcionaron filtros")

    id = id_generador or obtener_id(session, macAddress)

    # Query para obtener promedio por fecha
    query = select(
        MEDICION_POR_HORA.fecha,
        func.hour(MEDICION_POR_HORA.hora),
        func.avg(MEDICION_POR_HORA.voltaje).label("promedio_voltaje"),
        func.count(MEDICION_POR_HORA.id_medicion).label("total_mediciones"),
        func.min(MEDICION_POR_HORA.voltaje).label("voltaje_minimo"),
        func.max(MEDICION_POR_HORA.voltaje).label("voltaje_maximo"),
    ).where(MEDICION_POR_HORA.id_generador == id)
    match filtro:
        case "dia":
            query = query.group_by(MEDICION_POR_HORA.fecha)
            query = query.order_by(MEDICION_POR_HORA.fecha)

        case "hora":
            query = query.group_by(func.hour(MEDICION_POR_HORA.hora))
            query = query.order_by(func.hour(MEDICION_POR_HORA.hora))

        case _:
            query = query.group_by(MEDICION_POR_HORA.fecha)
            query = query.order_by(MEDICION_POR_HORA.fecha)

    # Aplicar filtros de fecha si existen
    if fecha_minima and fecha_maxima:
        print(f"Filtrando entre {fecha_minima} y {fecha_maxima}")
        query = query.filter(
            MEDICION_POR_HORA.fecha >= fecha_minima,
            MEDICION_POR_HORA.fecha <= fecha_maxima,
        )
    elif fecha_minima:
        query = query.filter(MEDICION_POR_HORA.fecha >= fecha_minima)
    elif fecha_maxima:
        query = query.filter(MEDICION_POR_HORA.fecha <= fecha_maxima)

    # Debug: mostrar la query SQL
    print("Query SQL generada:", str(query))

    resultado = session.exec(query).all()
    print(f"Encontrados {len(resultado)} registros")

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron voltajes para las fechas especificadas",
        )

    # Formatear resultados
    voltajes = []
    for fecha, hora, promedio, total, minimo, maximo in resultado:
        temp = str(fecha)
        if filtro == "hora":
            temp = str(hora)
        voltajes.append(
            {
                "date": temp,
                "voltage": round(float(promedio), 2),
                "meditions": total,
                "min_voltage": float(minimo),
                "max_voltage": float(maximo),
            }
        )
        print(
            f"Fecha: {temp}, Promedio: {round(float(promedio), 2)}, Mediciones: {total}"
        )

    return {
        "detail": "Promedios de voltaje por fecha encontrados",
        "data": voltajes,
        "total_fechas": len(voltajes),
    }


def obtener_consumos(
    session: Session,
    macAddress: str,
    filter: str | None = None,
    id_generador: int | None = None,
) -> dict:
    id = id_generador or obtener_id(session, macAddress)

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
