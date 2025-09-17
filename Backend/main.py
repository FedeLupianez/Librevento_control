from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_config
from mangum import Mangum

# Carpeta de Routers
from Routers import UsuarioRouter, GeneradorRouter, MedicionRouter


Config: dict = get_config()

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=Config["SECRET_KEY"])

# Agrego los routers :
app.include_router(UsuarioRouter.router)
app.include_router(GeneradorRouter.router)
app.include_router(MedicionRouter.router)
