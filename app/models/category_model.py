from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    __tablename__ = "category"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    name: str = Field(..., max_length=255, sa_column_kwargs={"unique": True})
    description: Optional[str] = None
