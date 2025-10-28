from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from decimal import Decimal
import uuid
from sqlmodel import Field, SQLModel

class Booking(SQLModel, table=True):
    __tablename__ = "booking"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    
    user_id: Optional[UUID] = Field(default=None, foreign_key="app_user.id")
    event_id: Optional[UUID] = Field(default=None, foreign_key="event.id")
    total: Decimal = Field(default=0)
    date: datetime = Field(default_factory=datetime.now(timezone.utc))
