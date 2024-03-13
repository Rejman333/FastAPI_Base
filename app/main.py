import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.core.config import settings

from app.core.db import sessionmanager

from contextlib import asynccontextmanager


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


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=f"{settings.ENV.upper()}.{settings.TITLE}",
    docs_url="/" if settings.ENV == "dev" else None,
    lifespan=lifespan if settings.ENV == "dev" else None,
    generate_unique_id_function=custom_generate_unique_id
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
