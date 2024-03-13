from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.models_base import ModelSoftDelete
from app.core.db import Base


class User(ModelSoftDelete, Base):
    email: Mapped[str] = mapped_column((String(160)), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __init__(self, **kwargs):
        if "password" in kwargs:
            kwargs["hashed_password"] = kwargs.pop("password")

        super().__init__(**kwargs)
