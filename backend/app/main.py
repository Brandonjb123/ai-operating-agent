from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth
from app.api import organization
from app.api import role
from app.api import membership
from app.api import agent
from app.api import memory
from app.api import knowledge
from app.api import workflow 
from app.api import execution

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Operating Agent Platform",
)

# ==========================================
# CORS Configuration (Phase 12.2)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend development origin
    allow_credentials=False,                  # V1 pakai localStorage, bukan cookie
    allow_methods=["*"],
    allow_headers=["*"],
)


# Daftarkan router autentikasi
app.include_router(auth.router)
app.include_router(organization.router)
app.include_router(role.router)
app.include_router(membership.router)
app.include_router(agent.router)    
app.include_router(memory.router)
app.include_router(knowledge.router)
app.include_router(workflow.router)
app.include_router(execution.router)

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