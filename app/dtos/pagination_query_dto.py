from typing import Literal
from pydantic import BaseModel, Field


class PaginationQueryDto(BaseModel):
    search: str | None = Field(default=None)
    limit: int = Field(default=20, gt=0, le=100)
    page: int = Field(default=1, ge=0)
    order_by: str | None = Field(default=None)
    order_direction: Literal["desc", "asc"] = "desc"

