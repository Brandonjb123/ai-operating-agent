from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Operating Agent Platform",
)


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