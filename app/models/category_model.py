from datetime import datetime, timezone
from typing import List, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel

from app.models.event_category_model import EventCategory
from app.models.event_model import Event


class Category(SQLModel, table=True):
    __tablename__ = "category"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    name: str = Field(..., max_length=255, sa_column_kwargs={"unique": True})
    description: Optional[str] = None

    # Many-to-many: category <-> event
    events: List["Event"] = Relationship(
        back_populates="categories",
        link_model=EventCategory,
        sa_relationship_kwargs={"lazy": "noload"},
    )