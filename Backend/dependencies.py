from dotenv import dotenv_values
from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine

Config = dotenv_values("local.env")  # Configuraciones
engine = create_engine(
    f"{Config['ENGINE']}://{Config['USER']}:{Config['PASSWORD']}@{Config['HOST']}/{Config['DATABASE']}",
)  # motor para la base de datos
print("Base de datos conectada")


def get_config() -> dict[str, str | None]:
    return Config


def get_engine() -> Engine:
    return engine


def get_session():
    with Session(engine) as session:
        yield session
