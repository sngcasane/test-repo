"""Auth service entry point."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routes import router as auth_router
from .db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup: warm the Redis connection pool, verify DB connectivity
    async with engine.connect() as conn:
        await conn.execute("SELECT 1")
    yield
    # On shutdown: dispose the engine
    await engine.dispose()


app = FastAPI(
    title="Acme Auth Service",
    version=os.environ.get("SERVICE_VERSION", "dev"),
    lifespan=lifespan,
)

app.include_router(auth_router)
