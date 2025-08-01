import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


# ToDo sprawdzić jak zachowa się timezone=True
class ModelNormal:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ModelSoftDelete(ModelNormal):
    deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=None, nullable=True)
