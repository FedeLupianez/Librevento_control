from sqlmodel import DATE, INT, TIME, Field, SQLModel, create_engine, VARCHAR
from dotenv import dotenv_values


def init_database():
    """
    Función para crear la base de datos
    """

    class USUARIO(SQLModel, table=True):
        id_usuario: INT | None = Field(default=None, primary_key=True)
        nombre: VARCHAR
        sexo: VARCHAR
        foto_perfil: VARCHAR
        email: VARCHAR

    class GENERADOR(SQLModel, table=True):
        id_generador: INT | None = Field(default=None, primary_key=True)
        id_usuario: INT | None = Field(default=None, foreign_key="USUARIO.id_usuario")
        ciudad: VARCHAR
        calle: VARCHAR
        numero_vivienda: INT

    class MEDICIO_POR_HORA(SQLModel, table=True):
        id_medicion: INT | None = Field(default=None, primary_key=True)
        id_generador: INT | None = Field(
            default=None, foreign_key="GENERADOR.id_generador"
        )
        voltaje_generado: INT
        consumo: INT
        velocidad_viento: INT
        direccion_viento: INT
        humedad: INT
        temperatura: INT
        fecha: DATE
        hora: TIME

    Config: dict[str, str | None] = dotenv_values(".env")
    motor = create_engine(url=Config["DATABASE_URL"])
    SQLModel.metadata.create_all(motor)
