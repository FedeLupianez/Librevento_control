from sqlalchemy.exc import IntegrityError, OperationalError
from typing import Literal
from sqlmodel import Session, select, func
from Tablas import MEDICION, GENERADOR
from fastapi import HTTPException


def create(session: Session, measurement: MEDICION) -> dict:
    """Function to create a new measurement
    Args:
        session (sqlmodel.Session): connection to the database
        measurement (Tablas.MEDICION): MEDICION class object
    """

    try:
        session.add(measurement)
        session.commit()
        session.refresh(measurement)
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
    return {"message": "Measurement created successfully"}


def get_id(session: Session, macAddress: str) -> int:
    id = session.exec(
        select(GENERADOR.id_generador).where(GENERADOR.mac_address == macAddress)
    ).first()
    if not (id):
        raise HTTPException(status_code=404, detail="Generator not found")
    return id


def format_data(
    data, filter_by: str, data_type: Literal["voltage", "consumption"] | None = None
):
    """
    Function to convert query data into a dictionary
    to be able to return it as an HTTP response
    """
    print(data)
    # Format results
    temp_list = []
    for date, hour, average, total, minimum, maximum in data:
        temp = str(date) if (filter_by == "day") else str(hour)
        temp_list.append(
            {
                "date": temp,
                "voltage" if data_type == "voltage" else "consumption": round(
                    float(average), 2
                ),
                "measurements": total,
                "min_voltage": float(minimum),
                "max_voltage": float(maximum),
            }
        )
        print(
            f"Date: {temp}, Average: {round(float(average), 2)}, Measurements: {total}"
        )
    return temp_list


def get_data(
    session: Session,
    mac_address: str,
    filter_by: Literal["day", "hour"],
    min_date: str | None = None,
    max_date: str | None = None,
    current_date: str | None = None,
    data_type: Literal["voltage", "consumption"] | None = None,
):
    id = get_id(session, mac_address)
    query = select(
        MEDICION.fecha,
        func.hour(MEDICION.hora),
        func.avg(MEDICION.voltaje).label("average_voltage")
        if data_type == "voltage"
        else func.avg(MEDICION.consumo).label("average_consumption"),
        func.count(MEDICION.id_medicion).label("total_measurements"),
        func.min(MEDICION.voltaje).label("min_voltage"),
        func.max(MEDICION.voltaje).label("max_voltage"),
    ).where(MEDICION.id_generador == id)

    if filter_by == "day":
        query = query.group_by(MEDICION.fecha)
        query = query.order_by(MEDICION.fecha)
    elif filter_by == "hour":
        query = query.group_by(func.hour(MEDICION.hora))
        query = query.order_by(func.hour(MEDICION.hora))

    # Apply date filters if they exist
    if min_date and max_date:
        print(f"Filtering between {min_date} and {max_date}")
        query = query.filter(
            MEDICION.fecha >= min_date,
            MEDICION.fecha <= max_date,
        )
    elif min_date:
        query = query.filter(MEDICION.fecha >= min_date)
    elif max_date:
        query = query.filter(MEDICION.fecha <= max_date)
    elif current_date:
        query = query.filter(MEDICION.fecha == current_date)

    result = session.exec(query).all()
    return result


def get_voltages(
    session: Session,
    mac_address: str | None = None,
    filter_by: Literal["day", "hour"] | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    current_date: str | None = None,
) -> dict:
    if not mac_address:
        raise HTTPException(status_code=400, detail="mac_address not provided")
    filter_by = filter_by or "day"

    result = get_data(
        session=session,
        mac_address=mac_address,
        filter_by=filter_by,
        min_date=min_date,
        max_date=max_date,
        current_date=current_date,
        data_type="voltage",
    )
    print(f"Found {len(result)} records")

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No voltages found for the specified dates",
        )

    voltages = format_data(data=result, filter_by=filter_by, data_type="voltage")

    return {
        "detail": "Average voltages per date found",
        "data": voltages,
        "total_dates": len(voltages),
    }


def get_consumptions(
    session: Session,
    mac_address: str | None = None,
    filter_by: Literal["day", "hour"] | None = None,
    min_date: str | None = None,
    max_date: str | None = None,
    current_date: str | None = None,
) -> dict:
    if not mac_address:
        raise HTTPException(status_code=400, detail="mac_address not provided")
    filter_by = filter_by or "day"

    result = get_data(
        session=session,
        mac_address=mac_address,
        filter_by=filter_by,
        min_date=min_date,
        max_date=max_date,
        current_date=current_date,
        data_type="consumption",
    )
    print(f"Found {len(result)} records")

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No voltages found for the specified dates",
        )

    consumptions = format_data(data=result, filter_by=filter_by, data_type="consumption")

    return {
        "detail": "Average voltages per date found",
        "data": consumptions,
        "total_dates": len(consumptions),
    }
