from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_config
from mangum import Mangum
import uvicorn
import os

# Routers folder
from Routers import UserRouter, GeneratorRouter, MeasurementRouter


Config: dict = get_config()

app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://librevento.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the routers:
app.include_router(UserRouter.router)
app.include_router(GeneratorRouter.router)
app.include_router(MeasurementRouter.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)