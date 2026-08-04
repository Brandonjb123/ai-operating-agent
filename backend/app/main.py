from fastapi import FastAPI

from app.core.config import settings
from app.api import auth
from app.api import organization
from app.api import role
from app.api import membership
from app.api import agent

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Operating Agent Platform",
)

# Daftarkan router autentikasi
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(role.router)
app.include_router(membership.router)
app.include_router(agent.router)

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