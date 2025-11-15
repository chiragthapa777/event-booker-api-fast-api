from typing import Literal
from pydantic import Field

from app.dtos.base_dto import BaseDto


class PaginationQueryDto(BaseDto):
    search: str | None = Field(default=None)
    limit: int = Field(default=20, gt=0, le=100)
    page: int = Field(default=1, ge=0)
    order_by: str | None = Field(default=None)
    order_direction: Literal["desc", "asc"] = "desc"


class EventQueryDto(PaginationQueryDto):
    categoryIds: str | None = Field(default="", description="comma separated")
    statuses: str | None = Field(default="", description="comma separated")
