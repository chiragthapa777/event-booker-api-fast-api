from typing import Optional, Dict
from datetime import datetime, timezone
from uuid import UUID 
from decimal import Decimal
import uuid
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class Payment(SQLModel, table=True):
    __tablename__ = "payment"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    user_id: Optional[UUID] = Field(default=None, foreign_key="app_user.id")
    booking_id: Optional[UUID] = Field(default=None, foreign_key="booking.id")
    amount: Decimal = Field(...)
    payment_detail: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
    transaction_id: Optional[str] = Field(default=None, sa_column=Column("transaction_id", unique=True))
    method: Optional[str] = None
