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


# --- Dynamic Environment Loading ---
Config = dotenv_values("school.env")
Config["COOKIE_DOMAIN"] = (
    "http://localhost:8000"
    if Config["ENVIRONMENT"] == "dev"
    else Config["COOKIE_DOMAIN"]
)
engine: Optional[Engine] = None
tunnel: Optional[SSHTunnelForwarder] = None

# I check if the configuration has any SSH
if Config.get("SSH_USER", None) is not None:
    # If so, I create an ssh tunnel to the school server
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
    tunnel.start()  # I start the tunnel, which does not close until I say so
    print("SSH tunnel initialized")
    engine = create_engine(
        _build_database_url(Config["LOCAL_BIND_HOST"], port=tunnel.local_bind_port)
    )
else:
    # If it has nothing of ssh, I create the engine for the current configuration
    assert Config["HOST"] is not None
    assert Config["LOCAL_PORT"] is not None
    engine = create_engine(
        _build_database_url(Config["HOST"], port=int(Config["LOCAL_PORT"]))
    )  # database engine

# I try to connect the database to see if it works
try:
    with engine.connect() as connection:
        pass
    print("✅ Database connected successfully")
except OperationalError as e:
    print("❌Error connecting to the database")
    print("Details : ", e)
    if tunnel:
        tunnel.stop()


def get_config() -> dict[str, str | None]:
    return Config


def get_engine() -> Engine:
    if not engine:
        raise RuntimeError("Engine not initialized")
    return engine


def get_session():
    with Session(engine) as session:
        yield session

