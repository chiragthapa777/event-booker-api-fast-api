

from typing import List

from sqlmodel import Session


class PaginationOption:
    def __init__(
        self,
        page: int = 1,
        limit: int = 20,
        search: str = "",
        sorting: str = "desc",
        sorting_col: str = "created_at",
    ):
        self.page = page
        self.limit = limit
        self.search = search
        self.sorting = sorting
        self.sorting_col = sorting_col

    def get_offset(self) -> int:
        return (self.page - 1) * self.limit
    
