from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI App", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Wanna Be Startin’ Somethin’ ? MKDF! need docs? check out /docs for swagger API docs :)"}

@app.get("/health")
async def health_check():
    if not app.state.ready:
        return {"status": "unhealthy", "reason": "Application is not ready"}
    if not app.state.alive:
        return {"status": "unhealthy", "reason": "Application is not alive"}
    from .core import database
    if not database.is_connected():
        return {"status": "unhealthy", "reason": "Database connection is not healthy"}
    return {"status": "healthy"}
