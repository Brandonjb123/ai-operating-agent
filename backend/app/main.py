from fastapi import FastAPI

app = FastAPI(
    title="AI Operating Agent",
    version="0.1.0",
    description="Enterprise AI Operating Agent Platform"
)


@app.get("/")
def root():
    return {
        "project": "AI Operating Agent",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }