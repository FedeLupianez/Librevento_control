from sqlmodel import select, create_engine, Session
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Query
import Tablas

Config = dotenv_values(".env")  # Configuraciones
engine = create_engine(
    "mysql+pymysql://root:password@localhost:3306/test"
)  # motor para la base de datos

app = FastAPI()


@app.get("/generador/")
def get_id(user_id: int = Query(None, ge=0)):
    with Session(engine) as session:
        # Armar la query
        query = select(Tablas.GENERADOR.id_generador).where(
            Tablas.GENERADOR.id_usuario == user_id
        )
        # Ejecutar la query
        generadores = session.exec(query).all()
        # Si no encuentra ningun generador devuelve una lista vacía
        if not generadores:
            return HTTPException(status_code=404, detail="usuario no encontrado")

        # Devuelve el último elemento porque queremos que se asocie el
        # generador que el cliente compró y acaba de instalar con el
        # ultimo id de un generador en su cuenta ya que este ya está creado
        return {"id_nuevo_generador": generadores[-1]}
