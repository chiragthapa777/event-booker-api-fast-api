from datetime import datetime, date
import re
from typing import Optional
import uuid
from pydantic import Field, field_validator

from app.dtos.base_dto import BaseDto
from app.dtos.file_dto import FileRead
from app.enums.gender_enum import GenderEnum


class AppUserRead(BaseDto):
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



class ProfileUpdateRequestDto(BaseDto):
    full_name: Optional[str] = Field(
        title="Full Name",
        example="John Rai",
        max_length=255,
        min_length=3,
        description="The user's full name. Minimum 3 and maximum 255 characters.",
    )

    dob: Optional[date] = Field(
        title="Date of Birth",
        example="2001-09-06",
        description="Date of birth in YYYY-MM-DD format.",
    )

    gender: Optional[GenderEnum] = Field(
        title="Gender",
        example="male",
        description="Gender of the user. Allowed values: male, female, other.",
    )

    phone_number: Optional[str] = Field(
        default=None,
        title="Phone Number",
        example="9810338577",
        max_length=15,
        description="Valid phone number (digits only, 7–15 characters).",
    )

    profile_id: Optional[uuid.UUID] = Field(
        default=None,
        title="Profile ID",
        example="6f8c9d62-46a9-4c1a-9a53-b92f1e5b9a42",
        description="Unique profile identifier (UUID).",
    )


    # --- Custom Validators ---
    @field_validator("phone_number")
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.fullmatch(r"^\d{7,15}$", v):
            raise ValueError(
                "Phone number must contain only digits and be between 7–15 characters long."
            )
        return v

    @field_validator("dob")
    def validate_dob(cls, v):
        if v and v > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return v

    @field_validator("full_name")
    def validate_full_name(cls, v):
        if v and not re.match(r"^[A-Za-z\s\.\-']+$", v):
            raise ValueError(
                "Full name can only contain letters, spaces, periods, hyphens, and apostrophes."
            )
        return v
