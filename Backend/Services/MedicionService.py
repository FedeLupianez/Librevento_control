from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Literal
from sqlmodel import Session, select, func
from Tablas import MEDICION, GENERADOR
from fastapi import HTTPException


def crear(session: Session, medicion: MEDICION) -> dict:
    """Función para crear una nueva medicion
    engine (sqlalchemy.exc.engine) : conexión con la base de datos
    medicion (Tablas.MEDICION) : objeto clase MEDICION"""

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


def obtener_id(session: Session, macAddress: str) -> int:
    id = session.exec(
        select(GENERADOR.id_generador).where(GENERADOR.mac_address == macAddress)
    ).first()
    if not (id):
        raise HTTPException(status_code=404, detail="Generador no encontrado")
    return id


def formatear_datos(
    datos, filtro: str, dato: Literal["voltaje", "consumo"] | None = None
):
    """
    Función para convertir los datos de una consulta en un diccionario
    para poder retornarlo como respuesta HTTP
    """
    print(datos)
    # Formatear resultados
    temp_list = []
    for fecha, hora, promedio, total, minimo, maximo in datos:
        temp = str(fecha) if (filtro == "dia") else str(hora)
        temp_list.append(
            {
                "date": temp,
                "voltage" if dato == "voltaje" else "consumption": round(
                    float(promedio), 2
                ),
                "meditions": total,
                "min_voltage": float(minimo),
                "max_voltage": float(maximo),
            }
        )
        print(
            f"Fecha: {temp}, Promedio: {round(float(promedio), 2)}, Mediciones: {total}"
        )
    return temp_list


def obtener_datos(
    session: Session,
    mac_address: str,
    filtro: Literal["dia", "hora"],
    fecha_minima: str | None = None,
    fecha_maxima: str | None = None,
    fecha_actual: str | None = None,
    dato: Literal["voltaje", "consumo"] | None = None,
):
    id = obtener_id(session, mac_address)
    query = select(
        MEDICION.fecha,
        func.hour(MEDICION.hora),
        func.avg(MEDICION.voltaje).label("promedio_voltaje")
        if dato == "voltaje"
        else func.avg(MEDICION.consumo).label("promedio_consumo"),
        func.count(MEDICION.id_medicion).label("total_mediciones"),
        func.min(MEDICION.voltaje).label("voltaje_minimo"),
        func.max(MEDICION.voltaje).label("voltaje_maximo"),
    ).where(MEDICION.id_generador == id)

    if filtro == "dia":
        query = query.group_by(MEDICION.fecha)
        query = query.order_by(MEDICION.fecha)
    elif filtro == "hora":
        query = query.group_by(func.hour(MEDICION.hora))
        query = query.order_by(func.hour(MEDICION.hora))

    # Aplicar filtros de fecha si existen
    if fecha_minima and fecha_maxima:
        print(f"Filtrando entre {fecha_minima} y {fecha_maxima}")
        query = query.filter(
            MEDICION.fecha >= fecha_minima,
            MEDICION.fecha <= fecha_maxima,
        )
    elif fecha_minima:
        query = query.filter(MEDICION.fecha >= fecha_minima)
    elif fecha_maxima:
        query = query.filter(MEDICION.fecha <= fecha_maxima)
    elif fecha_actual:
        query = query.filter(MEDICION.fecha == fecha_actual)

    result = session.exec(query).all()
    return result


def obtener_voltajes(
    session: Session,
    mac_address: str | None = None,
    filtro: Literal["dia", "hora"] | None = None,
    fecha_minima: str | None = None,
    fecha_maxima: str | None = None,
    fecha_actual: str | None = None,
) -> dict:
    if not mac_address:
        raise HTTPException(status_code=400, detail="No se proporcionó la mac_address")
    filtro = filtro or "dia"

    resultado = obtener_datos(
        session=session,
        mac_address=mac_address,
        filtro=filtro,
        fecha_minima=fecha_minima,
        fecha_maxima=fecha_maxima,
        fecha_actual=fecha_actual,
        dato="voltaje",
    )
    print(f"Encontrados {len(resultado)} registros")

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron voltajes para las fechas especificadas",
        )

    voltajes = formatear_datos(datos=resultado, filtro=filtro, dato="voltaje")

    return {
        "detail": "Promedios de voltaje por fecha encontrados",
        "data": voltajes,
        "total_fechas": len(voltajes),
    }


def obtener_consumos(
    session: Session,
    mac_address: str | None = None,
    filtro: Literal["dia", "hora"] | None = None,
    fecha_minima: str | None = None,
    fecha_maxima: str | None = None,
    fecha_actual: str | None = None,
) -> dict:
    if not mac_address:
        raise HTTPException(status_code=400, detail="No se proporcionó la mac_address")
    filtro = filtro or "dia"

    resultado = obtener_datos(
        session=session,
        mac_address=mac_address,
        filtro=filtro,
        fecha_minima=fecha_minima,
        fecha_maxima=fecha_maxima,
        fecha_actual=fecha_actual,
        dato="consumo",
    )
    print(f"Encontrados {len(resultado)} registros")

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron voltajes para las fechas especificadas",
        )

    consumos = formatear_datos(datos=resultado, filtro=filtro, dato="consumo")

    return {
        "detail": "Promedios de voltaje por fecha encontrados",
        "data": consumos,
        "total_fechas": len(consumos),
    }
