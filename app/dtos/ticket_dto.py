from datetime import datetime
from typing import Optional
from decimal import Decimal
import uuid
from app.dtos.base_dto import BaseDto
from pydantic import Field


class TicketCreateDto(BaseDto):
    event_id: str
    name: str = Field(..., max_length=255)
    price: Decimal = Field(default=0)
    total_qty: int = Field(default=0)


class TicketInputDto(BaseDto):
    """Nested ticket DTO for event create/update.

    - `id` optional: if present during update, ticket will be updated; otherwise created.
    - `event_id` is omitted for nested creation because event id is known by the parent.
    """
    id: Optional[str] = None
    name: str = Field(..., max_length=255)
    price: Decimal = Field(default=0)
    total_qty: int = Field(default=0)


class TicketRead(BaseDto):
    id: uuid.UUID
    event_id: uuid.UUID
    name: str
    price: Decimal
    total_qty: int
    total_booked: int
    created_at: Optional[datetime]
