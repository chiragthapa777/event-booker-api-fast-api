from datetime import datetime, timezone
import uuid
from sqlmodel import SQLModel, Field

class Token(SQLModel, table=True):
    __tablename__ = "token"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=None)

    code : int
    resource_type: str
    resource_id: str
