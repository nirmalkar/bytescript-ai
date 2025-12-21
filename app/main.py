from fastapi import FastAPI
from app.api import health, chat

app = FastAPI(title="ByteScript AI")

# Include API routers
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
