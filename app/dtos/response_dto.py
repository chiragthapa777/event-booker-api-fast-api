from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic import BaseModel, Field

T = TypeVar("T")

class AppResponse(BaseModel, Generic[T]):
    success: bool = Field(default=False)
    data: T = Field(default=None)
    message: str = Field(default="")
