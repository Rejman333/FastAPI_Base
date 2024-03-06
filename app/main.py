import uvicorn
from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings

app = FastAPI(
    title=f"{settings.ENV.upper()}.{settings.TITLE}",
    docs_url="/" if settings.ENV == "dev" else None
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
