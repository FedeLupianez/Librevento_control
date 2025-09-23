from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session, select, text
from Tablas import USUARIO
from fastapi import HTTPException
import bcrypt


def crear(session: Session, usuario: USUARIO) -> dict:
    """Función para crear un nuevo usuario
    engine (sqlalchemy.exc.engine) : conexión con la base de datos
    usuario (Tablas.USUARIO) : objeto clase USUARIO a crear
    """
    tempClave = usuario.clave.encode("utf-8")
    print(usuario)
    # Hasheo la password
    claveHasheada = bcrypt.hashpw(tempClave, bcrypt.gensalt())
    usuario.clave = claveHasheada.decode("utf-8")
    try:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
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
    return {"id": usuario.id_usuario}


def borrar(session: Session, id_usuario: int) -> dict:
    """Función para borrar un registro de la tabla usuario
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        idUsuario (str) : dirección mac del dispositivo
    """
    query = select(USUARIO).where(USUARIO.id_usuario == id_usuario)
    usuario = session.exec(query).first()

    if not (usuario):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    session.delete(usuario)
    session.commit()
    return {"message": "usuario borrado exitosamente"}


def obtener(session: Session, id_usuario: int) -> dict:
    """Función para obtener un registro de usuario por su id
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        id_usuario (int) : id del usuario a obtener
    """
    query = select(USUARIO).where(USUARIO.id_usuario == id_usuario)
    usuario = session.exec(query).first()
    if not (usuario):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.refresh(usuario)
    return usuario.dict(exclude={"clave"})


def obtener_id(session: Session, email_usuario: str) -> dict:
    """Función para obtener un registro de usuario por su email
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        email_usuario (str) : email del usuario a obtener
    """
    query = select(USUARIO.id_usuario).where(USUARIO.email == email_usuario)
    id_usuario = session.exec(query).first()
    if not (id_usuario):
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    return {"id": id_usuario}


def login(session: Session, email_usuario: str, clave: str) -> dict:
    """Función para obtener un registro de usuario por su email
    Args:
        engine (sqlalchemy.exc.engine) : conexión con la base de datos
        email_usuario (str) : email del usuario a obtener
        clave (str) : clave que puso el usuario
    """
    tempClave = clave.encode("utf-8")
    login_approved = session.execute(
        text("select validar_usuario(:email_usuario, :clave)"),
        {"email_usuario": email_usuario, "clave": tempClave},
    )

    if not login_approved:
        raise HTTPException(status_code=404, detail="usuario no encontrado")

    usuario = session.exec(select(USUARIO).where(USUARIO.email == email_usuario)).one()

    return usuario.model_dump(exclude={"clave"})
