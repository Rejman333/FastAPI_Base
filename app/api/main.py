from fastapi import APIRouter

from app.api.routes import utils, users

api_router = APIRouter()
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
