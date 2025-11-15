from typing import List, Optional, Dict
from datetime import datetime, timezone
from uuid import UUID
from decimal import Decimal
import uuid
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

from app.enums.event_status import EventStatus
from app.models.event_category_model import EventCategory
from app.models.event_ticket_model import EventTicket
from app.models.file_model import File


class Event(SQLModel, table=True):
    __tablename__ = "event"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    admin_id: Optional[UUID] = Field(default=None, foreign_key="app_user.id")
    name: str = Field(..., max_length=255)
    slug: str = Field(..., sa_column=Column("slug", nullable=False, unique=True))
    seo_meta_data: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
    date: datetime = Field(...)
    venue: Optional[str] = None
    lng: Optional[Decimal] = None
    lat: Optional[Decimal] = None
    description: Optional[str] = None
    terms_and_condition: Optional[str] = None
    event_layout_photo_id: Optional[UUID] = Field(default=None, foreign_key="file.id")
    event_banner_photo_id: Optional[UUID] = Field(default=None, foreign_key="file.id")
    event_photo_id: Optional[UUID] = Field(default=None, foreign_key="file.id")
    status: Optional[EventStatus] = Field(
        default=EventStatus.DRAFT, foreign_key="file.id"
    )

    event_layout_photo: Optional[File] = Relationship(
        back_populates=None,
        sa_relationship_kwargs={
            "lazy": "noload",
            "foreign_keys": "[Event.event_layout_photo_id]",
        },
    )
    event_banner_photo: Optional[File] = Relationship(
        back_populates=None,
        sa_relationship_kwargs={
            "lazy": "noload",
            "foreign_keys": "[Event.event_banner_photo_id]",
        },
    )
    event_photo: Optional[File] = Relationship(
        back_populates=None,
        sa_relationship_kwargs={
            "lazy": "noload",
            "foreign_keys": "[Event.event_photo_id]",
        },
    )

    tickets: List["EventTicket"] = Relationship(
        back_populates="event", sa_relationship_kwargs={"lazy": "noload"}
    )

    categories: List["Category"] = Relationship(
        back_populates="events",
        link_model=EventCategory,
        sa_relationship_kwargs={"lazy": "noload"},
    )
