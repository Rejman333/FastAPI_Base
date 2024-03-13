from typing import TypeVar, Generic, List
import datetime

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from app.core.db import Base

from app.core.exceptions import SoftDeleteError

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)
ListResponseSchemaType = TypeVar("ListResponseSchemaType", bound=BaseModel)


class CRUDAsyncBase(Generic[
                        ModelType,
                        CreateSchemaType,
                        UpdateSchemaType,
                        ResponseSchemaType,
                        ListResponseSchemaType,
                    ]):
    def __init__(
            self,
            model_class: type[ModelType],
            response_schema_class: type[ResponseSchemaType],
            list_response_class: type[ListResponseSchemaType],
    ) -> None:
        self.model_class = model_class
        self.response_schema_class = response_schema_class
        self.list_response_class = list_response_class

    # ToDo Test This
    async def create(self, db: AsyncSession, *, create_schema: CreateSchemaType) -> ModelType:
        model = self.model_class(**create_schema)
        db.add(model)
        await db.flush()
        await db.refresh(model)

        return model

    # ToDo Check how committing works here, maybe it is not requaired
    async def create_from_list(self, db: AsyncSession, create_schemas: List[CreateSchemaType]) -> List[ModelType]:
        models = [
            self.model_class(**jsonable_encoder(create_schema, by_alias=False))
            for create_schema in create_schemas
        ]
        db.add_all(models)
        await db.flush()
        await db.commit()

        return models

    async def get_model_by_id(self, db: AsyncSession, *, id: int, include_deleted: bool = False) -> ModelType | None:
        stmt = (
            select(self.model_class)
            .where(self.model_class.id == id)
            .execution_options(include_deleted=include_deleted))
        return (await db.execute(stmt)).scalars().first()

    async def get_model_by_filter(self):
        raise NotImplementedError

    async def update(self, db: AsyncSession, *, model: ModelType, update_schema: UpdateSchemaType) -> ModelType:
        db_obj_dict = jsonable_encoder(model)
        update_dict = update_schema.model_dump(
            exclude_unset=True,
        )

        for field in db_obj_dict:
            if field in update_dict:
                setattr(model, field, update_dict[field])

        db.add(model)
        await db.flush()
        await db.refresh(model)
        return model

    # ToDo Test if i have to add data to AttributeError, Test how custom exception work and correct if needed
    async def delete(self, db: AsyncSession, *, model: ModelType):
        """Soft Delete"""
        if not hasattr(model, "deleted_at"):
            # Raise an exception
            raise AttributeError()
        if model.deleted_at:
            # Raise an exception
            raise SoftDeleteError()

        model.deleted_at = datetime.datetime.now(tz=datetime.timezone.utc)
        db.add(model)
        await db.flush()
        await db.refresh(model)
        return model

    # ToDo Test This
    async def delete_permanently(self, db: AsyncSession, *, model: ModelType) -> None:
        """Hard Delete"""
        await db.delete(model)
        await db.flush()
