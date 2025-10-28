from datetime import datetime, timezone
from typing import Optional
import uuid
from pydantic import computed_field
from sqlmodel import Field, SQLModel

from app.core.aws import s3

class File(SQLModel, table=True):
    __tablename__ = "file"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

    file_path: str = Field(..., sa_column_kwargs={"nullable": False})
    type: Optional[str] = Field(...)
    size: Optional[int] =  Field(...)

    @computed_field
    @property
    def link(self) -> Optional[str]:
        if self.file_path:
            return s3.create_presigned_url(self.file_path)
        return ""
    
    class Config:
        orm_mode = True
