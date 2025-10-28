from typing import Any, Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class PaginationData(BaseModel, Generic[T]):
    list: List[T]
    total_page: int
    total: int
