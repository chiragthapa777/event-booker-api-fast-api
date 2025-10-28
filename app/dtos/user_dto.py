from datetime import datetime, date
from typing import Optional
import uuid
from pydantic import BaseModel

from app.dtos.file_dto import FileRead
from app.utils import dto_utils


class AppUserRead(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    email: str
    full_name: Optional[str]
    dob: Optional[date]
    roles: Optional[str]
    gender: Optional[str]
    phone_number: Optional[str]
    phone_verified_at: Optional[datetime]
    email_verified_at: Optional[datetime]
    profile: Optional[FileRead]

    model_config = dto_utils.default_db_model_config

class ProfileUpdateRequestDto(BaseModel):
    pass