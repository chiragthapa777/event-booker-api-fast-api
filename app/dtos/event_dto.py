from typing import Optional, List
from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import Field, field_validator, validator
from app.dtos.base_dto import BaseDto
from app.dtos.ticket_dto import TicketInputDto, TicketRead


class EventCategoryDto(BaseDto):
    id: uuid.UUID
    name: str


class FileRefDto(BaseDto):
    id: uuid.UUID
    file_path: str | None = None
    link: str | None = None


class EventCreateDto(BaseDto):
    name: str = Field(..., max_length=255)
    date: datetime
    venue: Optional[str] = None
    lng: Optional[Decimal] = None
    lat: Optional[Decimal] = None
    description: Optional[str] = None
    terms_and_condition: Optional[str] = None
    category_ids: Optional[List[str]] = None
    event_layout_photo_id: Optional[str] = None
    event_banner_photo_id: Optional[str] = None
    event_photo_id: Optional[str] = None
    tickets: Optional[List[TicketInputDto]] = None

    @field_validator(
        "event_layout_photo_id",
        "event_banner_photo_id",
        "event_photo_id",
        mode="before",
    )
    @classmethod
    def validate_uuid(cls, v):
        if v is None:
            return v
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError("Must be a valid UUID string")
        return v

    @field_validator("category_ids", mode="before")
    @classmethod
    def validate_category_ids(cls, v):
        if v is None:
            return v

        for item in v:
            try:
                uuid.UUID(item)
            except ValueError:
                raise ValueError("Each category_id must be a valid UUID string")
        return v


class EventUpdateDto(BaseDto):
    name: Optional[str] = None
    date: Optional[datetime] = None
    venue: Optional[str] = None
    lng: Optional[Decimal] = None
    lat: Optional[Decimal] = None
    description: Optional[str] = None
    terms_and_condition: Optional[str] = None
    category_ids: Optional[List[str]] = None
    event_layout_photo_id: Optional[str] = None
    event_banner_photo_id: Optional[str] = None
    event_photo_id: Optional[str] = None
    tickets: Optional[List[TicketInputDto]] = None

    @field_validator(
        "event_layout_photo_id",
        "event_banner_photo_id",
        "event_photo_id",
        mode="before",
    )
    @classmethod
    def validate_uuid(cls, v):
        if v is None:
            return v
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError("Must be a valid UUID string")
        return v

    @field_validator("category_ids", mode="before")
    @classmethod
    def validate_category_ids(cls, v):
        if v is None:
            return v

        for item in v:
            try:
                uuid.UUID(item)
            except ValueError:
                raise ValueError("Each category_id must be a valid UUID string")


class EventRead(BaseDto):
    id: uuid.UUID
    name: str
    date: datetime
    venue: Optional[str] = None
    lng: Optional[Decimal] = None
    lat: Optional[Decimal] = None
    description: Optional[str] = None
    terms_and_condition: Optional[str] = None
    status: Optional[str] = None
    categories: Optional[list[EventCategoryDto]] = None
    event_layout_photo: Optional[FileRefDto] = None
    event_banner_photo: Optional[FileRefDto] = None
    event_photo: Optional[FileRefDto] = None
    tickets: Optional[List[TicketRead]] = None
    created_at: Optional[datetime] = None
