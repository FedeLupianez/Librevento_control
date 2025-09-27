from sshtunnel import SSHTunnelForwarder
from sqlmodel import Session, create_engine
import random
import Tablas
import datetime
import os
from dotenv import dotenv_values

config = dotenv_values("school.env")
ssh_host = config["SSH_HOST"]
ssh_port = 22
ssh_user = config["SSH_USER"]
ssh_password = config["SSH_PASSWORD"]

REMOTE_BIND_ADDRESS = ("127.0.0.1", 3306)

server_host = "localhost"
server_port = 3306
server_user = config["USER"]
server_password = config["PASSWORD"]
server_db = config["DATABASE"]


def progress_bar(current: int, total: int):
    progress = (current * 100) / total
    print(f"Progress: {progress:.2f}%", end="\r")
    actual = "[" + ("|" * int(progress)) + " " * (100 - int(progress)) + "]"
    print(actual)


print(f"Attempting connection with: {ssh_user}@{ssh_host} | pwd: {ssh_password}")
with SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=REMOTE_BIND_ADDRESS,
    local_bind_address=("127.0.0.1", 0),
) as tunnel:
    try:
        engine = create_engine(
            f"mysql+pymysql://{server_user}:{server_password}@{server_host}:{tunnel.local_bind_port}/{server_db}",
            echo=True,
        )

        current_date = datetime.datetime.now()
        monday_date = current_date - datetime.timedelta(days=current_date.weekday())
        sunday_date = current_date + datetime.timedelta((7 - current_date.weekday()))

        generators_count = 3

        with Session(engine) as session:
            for i in range(generators_count):
                for j in range(7):
                    date = monday_date + datetime.timedelta(days=j)
                    for m in range(24):
                        temp_table = Tablas.MEDICION(
                            id_generador=i + 1,
                            voltaje=random.randint(1, 11),
                            consumo=random.randint(1, 10),
                            velocidad=random.randint(1, 90),
                            direccion_viento=random.randint(0, 361),
                            humedad=random.randint(1, 100),
                            temperatura=random.randint(1, 100),
                            fecha=date,
                            hora=datetime.time(m, 0, 0),
                        )
                        session.add(temp_table)
                        os.system("clear")
                        print(f"Generator: {i} | date: {date} | time: {m}")
                        total = (i + 1) * 7 * 24
                        current = (i + 1) * (j + 1) * (m + 1)
                        progress_bar(current, total)
            session.commit()

    except Exception as e:
        print(e)
