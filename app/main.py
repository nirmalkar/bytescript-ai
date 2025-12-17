from fastapi import FastAPI
from app.api import health

app = FastAPI(title="ByteScript AI")

app.include_router(health.router, prefix="/api")
