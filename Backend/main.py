from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_config

# Carpeta de Routers
from Routers import UsuarioRouter, GeneradorRouter, MedicionRouter


Config: dict = get_config()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5173/login",
        "http://localhost:5173/signup",
        "http://localhost:5173/voltaje",
        "http://localhost:5173/consumo",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=Config["SECRET_KEY"])

# Agrego los routers :
app.include_router(UsuarioRouter.router)
app.include_router(GeneradorRouter.router)
app.include_router(MedicionRouter.router)
