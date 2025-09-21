from dotenv import dotenv_values
from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from typing import Optional
from sshtunnel import SSHTunnelForwarder


def _build_database_url(host: str, port: int = 5432) -> str:
    if port != 5432:
        return (
            f"{Config['ENGINE']}://{Config['USER']}:{Config['PASSWORD']}@{host}:{port}/"
            f"{Config['DATABASE']}"
        )
    return (
        f"{Config['ENGINE']}://{Config['USER']}:{Config['PASSWORD']}@{host}/"
        f"{Config['DATABASE']}"
    )


Config = dotenv_values("school.env")  # Configuraciones
engine: Optional[Engine] = None
tunnel: Optional[SSHTunnelForwarder] = None

# Verifico si la configuración tiene algo de SSH
if Config.get("SSH_USER", None) is not None:
    # Si es así, creo un tunel ssh hacia el servidor del colegio
    assert Config["SSH_PORT"] is not None
    assert Config["REMOTE_BIND_PORT"] is not None
    assert Config["LOCAL_BIND_HOST"] is not None
    assert Config["LOCAL_BIND_PORT"] is not None
    tunnel = SSHTunnelForwarder(
        (Config["SSH_HOST"], int(Config["SSH_PORT"])),
        ssh_username=Config["SSH_USER"],
        ssh_password=Config["SSH_PASSWORD"],
        remote_bind_address=(
            Config["REMOTE_BIND_HOST"],
            int(Config["REMOTE_BIND_PORT"]),
        ),
        local_bind_address=(Config["LOCAL_BIND_HOST"], int(Config["LOCAL_BIND_PORT"])),
    )
    tunnel.start()  # Inicio el tunel, el cual no se cierra hasta que lo diga
    print("Tunel ssh inicializado")
    engine = create_engine(
        _build_database_url(Config["LOCAL_BIND_HOST"], port=tunnel.local_bind_port)
    )
else:
    # Si no tiene nada de ssh, creo el engine para la configuración actual
    assert Config["HOST"] is not None
    assert Config["LOCAL_PORT"] is not None
    engine = create_engine(
        _build_database_url(Config["HOST"], port=int(Config["LOCAL_PORT"]))
    )  # motor para la base de datos

# Intento conectar la base de datos  para ver si funciona
try:
    with engine.connect() as connection:
        pass
    print("✅ Base de datos conectada exitosamente")
except OperationalError as e:
    print("❌Error al conectar la base de datos")
    print("Details : ", e)
    if tunnel:
        tunnel.stop()


def get_config() -> dict[str, str | None]:
    return Config


def get_engine() -> Engine:
    if not engine:
        raise RuntimeError("Motor no inicializado")
    return engine


def get_session():
    with Session(engine) as session:
        yield session
