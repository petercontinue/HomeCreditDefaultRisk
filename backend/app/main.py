from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.db.session import init_db
from app.services.ml_runtime import ml_runtime


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    ml_runtime.load()
    yield


settings = get_settings()
app = FastAPI(
    title="Home Credit Default Risk API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {
        "name": "Home Credit Default Risk API",
        "docs": "/docs",
        "health": "/api/health",
    }
