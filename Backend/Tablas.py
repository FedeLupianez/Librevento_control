from sqlmodel import DATE, TIMESTAMP, Field, SQLModel


class USUARIO(SQLModel, table=True):
    id_usuario: int | None = Field(default=None, primary_key=True)
    nombre: str
    sexo: str
    foto_perfil: str
    email: str


class GENERADOR(SQLModel, table=True):
    id_generador: int | None = Field(default=None, primary_key=True)
    id_usuario: int | None = Field(default=None, foreign_key="USUARIO.id_usuario")
    ciudad: str
    calle: str
    numero_vivienda: int


class MEDICIO_POR_HORA(SQLModel, table=True):
    id_medicion: int | None = Field(default=None, primary_key=True)
    id_generador: int | None = Field(default=None, foreign_key="GENERADOR.id_generador")
    voltaje_generado: int
    consumo: int
    velocidad_viento: int
    direccion_viento: int
    humedad: int
    temperatura: int
    fecha: str
    hora: str
