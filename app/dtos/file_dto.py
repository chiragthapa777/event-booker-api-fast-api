from typing import Optional
import uuid
from pydantic import BaseModel
from app.utils.dto_utils import default_db_model_config


class FileRead(BaseModel):
    id: uuid.UUID
    file_path: str
    type: Optional[str]
    size: Optional[int]
    link: Optional[str]

    model_config = default_db_model_config
