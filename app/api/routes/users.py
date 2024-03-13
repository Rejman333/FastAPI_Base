from fastapi import APIRouter

from app.schemas.user import UserResponse, UserCreate
from app.crud.user import crud_user
from app.api.dependencies import DBSessionDep

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserResponse)
async def create_user(new_user: UserCreate, db_session: DBSessionDep):
    """
    Create new user
    """
    user = await crud_user.create(db_session, create_schema=new_user)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db_session: DBSessionDep):
    """
    Get any user details by id
    """
    user = await crud_user.get_model_by_id(db_session, id=user_id)
    return user
