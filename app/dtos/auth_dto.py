from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator, model_validator
from datetime import date
from typing import Optional
from app.constants.regex_const import PASSWORD_REGEX
from app.dtos.base_dto import BaseDto
from app.dtos.user_dto import AppUserRead

class RegisterRequestDto(BaseDto):
    full_name: str = Field(
        title="Full Name",
        example="John Rai",
        max_length=255,
        min_length=3
    )

    email: EmailStr = Field(
        title="Email Address",
        example="john@example.com",
        max_length=255
    )

    password: str = Field(
        title="Password",
        example="Test@123",
        min_length=8,
        max_length=30,
        pattern=PASSWORD_REGEX
    )

    dob: date = Field(
        title="Date of Birth",
        example="2001-09-06",
    )

    phone_number: Optional[str] = Field(
        default=None,
        title="Phone Number",
        example="9810338577",
        max_length=15,
    )

    @field_validator("email", mode="before")
    def normalize_email(cls, v):
        return v.strip().lower()
    
    
class LoginRequestDto(BaseDto):
    email: Optional[EmailStr] = Field(
        default=None,
        title="Email Address",
        example="john@example.com",
        max_length=255
    )

    password: str = Field(
        title="Password",
        example="Test@123",
        min_length=8,
        max_length=30,
        pattern=PASSWORD_REGEX
    )

    phone_number: Optional[str] = Field(
        default=None,
        title="Phone Number",
        example="9810338577",
        max_length=15,
    )

    @field_validator("email", mode="before")
    def normalize_email(cls, v):
        return v.strip().lower()
    
    @model_validator(mode="after")
    def check_email_or_phone(cls, values):
        if not values.email and not values.phone_number:
            raise ValidationError("Either email or phone_number must be provided")
        return values
    

    
class LoginResponseDto(BaseDto):
    user :AppUserRead
    access_token :str


