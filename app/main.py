import uvicorn
from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings

from app.core.db import sessionmanager

from contextlib import asynccontextmanager
from app.models import user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # This creates the DB
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)

    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(
    title=f"{settings.ENV.upper()}.{settings.TITLE}",
    docs_url="/" if settings.ENV == "dev" else None,
    lifespan=lifespan if settings.ENV == "dev" else None
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
