from datetime import date, time
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import text
from dependencies import get_config

is_ssh_active = get_config()["SSH_USER"]

class USUARIO(SQLModel, table=True):
    __tablename__ = "USUARIO" if (is_ssh_active) else "usuario"
    id_usuario: int = Field(default=None, primary_key=True)
    nombre: str
    foto_perfil: str
    sexo: str
    email: str
    clave: str


class GENERADOR(SQLModel, table=True):
    __tablename__ = "GENERADOR" if (is_ssh_active) else "generador"
    id_generador: int = Field(primary_key=True)
    mac_address: Optional[str] = Field(default=None, nullable=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario")
    ciudad: str
    calle: str
    numero_vivienda: int


class MEDICION_POR_HORA(SQLModel, table=True):
    __tablename__ = "MEDICION" if (is_ssh_active) else "medicion_por_hora"
    id_medicion: int = Field(primary_key=True)
    id_generador: int = Field(foreign_key="generador.id_generador")
    voltaje: int
    consumo: int
    velocidad: int
    direccion_viento: int
    humedad: int
    temperatura: int
    fecha: Optional[date] = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_DATE")},
    )
    hora: Optional[time] = Field(
        default=None,
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_DATE")},
    )
