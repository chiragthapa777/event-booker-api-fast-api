from datetime import datetime
from typing import Optional, List
import uuid
from app.dtos.base_dto import BaseDto
from pydantic import Field


class CategoryCreateDto(BaseDto):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class CategoryRead(BaseDto):
    id: uuid.UUID
    name: str
    description: Optional[str]
    created_at: datetime
