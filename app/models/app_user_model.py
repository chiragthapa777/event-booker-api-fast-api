from typing import Optional
from datetime import datetime, date, timezone
import uuid
from sqlmodel import Field, Relationship, SQLModel

from app.models.file_model import File


class AppUser(SQLModel, table=True):
    __tablename__ = "app_user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    password: str = Field(..., exclude=True)
    email: str = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    dob: Optional[date] = None
    roles: str = Field(default=None)
    gender: Optional[str] = None
    phone_number: Optional[str] = Field(default=None)
    phone_verified_at: Optional[datetime] = None
    email_verified_at: Optional[datetime] = None
    profile_id: Optional[uuid.UUID] = Field(default=None, foreign_key="file.id")

    # relations
    profile: Optional[File] = Relationship(
        back_populates=None, sa_relationship_kwargs={"lazy": "noload"} # no eager loading and no lazy loading, unless explicitly added in query
    )
