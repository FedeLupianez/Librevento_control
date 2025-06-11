from datetime import date, time
from sqlmodel import Field, SQLModel
from typing import Optional


class USUARIO(SQLModel, table=True):
    id_usuario: int = Field(default=None, primary_key=True)
    nombre: str
    sexo: str
    foto_perfil: str
    email: str


class GENERADOR(SQLModel, table=True):
    id_generador: str = Field(primary_key=True)
    macAddress: Optional[str] = Field(default=None, nullable=True)
    id_usuario: int = Field(foreign_key="usuario.id_usuario")
    ciudad: str
    calle: str
    numero_vivienda: int


class MEDICION_POR_HORA(SQLModel, table=True):
    id_medicion: int = Field(primary_key=True)
    id_generador: str = Field(foreign_key="generador.id_generador")
    voltaje_generado: int
    consumo: int
    velocidad_viento: int
    direccion_viento: int
    humedad: int
    temperatura: int
    fecha: Optional[date] = Field(default=None, nullable=False)
    hora: Optional[time] = Field(default=None, nullable=False)
