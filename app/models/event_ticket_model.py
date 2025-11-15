from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
from decimal import Decimal
import uuid
from sqlmodel import Relationship, SQLModel, Field




class EventTicket(SQLModel, table=True):
    __tablename__ = "event_ticket"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    event_id: Optional[UUID] = Field(default=None, foreign_key="event.id")
    name: str = Field(..., max_length=255)
    price: Decimal = Field(default=0)
    total_qty: int = Field(default=0)
    total_booked: int = Field(default=0)

    event: Optional["Event"] = Relationship(
        back_populates="tickets", sa_relationship_kwargs={"lazy": "noload"}
    )
