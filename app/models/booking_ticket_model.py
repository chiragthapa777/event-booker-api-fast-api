from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4
import uuid
from sqlmodel import SQLModel, Field



class BookingTicket(SQLModel, table=True):
    __tablename__ = "booking_ticket"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    booking_id: Optional[uuid.UUID] = Field(default=None, foreign_key="booking.id")
    event_ticket_id: Optional[uuid.UUID] = Field(default=None, foreign_key="event_ticket.id")
