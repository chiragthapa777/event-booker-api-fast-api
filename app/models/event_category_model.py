from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class EventCategory(SQLModel, table=True):
    __tablename__ = "event_category"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="event.id")
    category_id: UUID = Field(foreign_key="category.id")
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    # Note: SQLModel/SQLAlchemy unique constraints can be added with __table_args__ if needed
    # but for simplicity, the db migration should enforce UNIQUE (event_id, category_id)
