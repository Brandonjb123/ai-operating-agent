from fastapi import FastAPI

from app.core.config import settings
from app.api import auth
from app.api import organization

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Operating Agent Platform",
)

# Daftarkan router autentikasi
app.include_router(auth.router)
app.include_router(organization.router)

@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "status": "running",
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
    }