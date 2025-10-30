from typing import Optional
import uuid
from app.dtos.base_dto import BaseDto


class FileRead(BaseDto):
    id: uuid.UUID
    file_path: str
    type: Optional[str]
    size: Optional[int]
    link: Optional[str]
