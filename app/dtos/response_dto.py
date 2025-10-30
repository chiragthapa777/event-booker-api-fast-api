from typing import Generic, TypeVar
from pydantic import Field

from app.dtos.base_dto import BaseDto

T = TypeVar("T")

class AppResponse(BaseDto, Generic[T]):
    success: bool = Field(default=False)
    data: T = Field(default=None)
    message: str = Field(default="")
