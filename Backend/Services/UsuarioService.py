from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session, select
from Tablas import USUARIO
from fastapi import HTTPException


def crear(engine, usuario: USUARIO) -> dict | HTTPException:
    """Función para crear un nuevo usuario
    engine (sqlalchemy.exc.engine) : conexión con la base de datos
    usuario (Tablas.USUARIO) : objeto clase USUARIO a crear
    """
    with Session(engine) as session:
        try:
            session.add(usuario)
            session.commit()
        except IntegrityError as e:
            print(e)
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
        return {"message": "Usuario creado exitosamente"}


def borrar(engine, id_usuario: int) -> dict | HTTPException:
    """Función para borrar un registro de la tabla usuario
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        idUsuario (str) : dirección mac del dispositivo
    """
    with Session(engine) as session:
        query = select(USUARIO).where(USUARIO.id_usuario == id_usuario)
        usuario = session.exec(query).first()

        if not (usuario):
            return HTTPException(status_code=404, detail="Usuario no encontrado")

        session.delete(usuario)
        session.commit()
        return {"message": "usuario borrado exitosamente"}


def obtener(engine, id_usuario: int) -> USUARIO | HTTPException:
    """Función para obtener un registro de usuario por su id
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        id_usuario (int) : id del usuario a obtener
    """
    with Session(engine) as session:
        query = select(USUARIO).where(USUARIO.id_usuario == id_usuario)
        usuario = session.exec(query).first()
        if not (usuario):
            return HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario


def obtener_id(engine, email_usuario: str) -> int | HTTPException:
    """Función para obtener un registro de usuario por su email
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        email_usuario (str) : email del usuario a obtener
    """
    with Session(engine) as session:
        query = select(USUARIO.id_usuario).where(USUARIO.email == email_usuario)
        id_usuario = session.exec(query).first()
        if not (id_usuario):
            return HTTPException(status_code=404, detail="usuario no encontrado")
        return id_usuario
