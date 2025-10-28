from http import HTTPStatus
from typing import Annotated
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    UploadFile,
)

from app.core.response import success_response
from app.dependencies.auth_dep import auth_with_any_role
from app.dependencies.session_dep import SessionDep
from app.dtos.pagination_query_dto import PaginationQueryDto
from app.dtos.response_dto import AppResponse
from app.enums.role_enum import UserRole
from app.models.file_model import File as FileModel
from app.services import file_service
from app.types.pagination_data import PaginationData
from app.utils.pagination_utils import PaginationOption


router = APIRouter(
    tags=["Files"],
    prefix="/file",
    dependencies=[Depends(auth_with_any_role([UserRole.USER, UserRole.ADMIN]))],
)

@router.get("/", response_model=AppResponse[PaginationData[FileModel]])
def find(session: SessionDep, query: Annotated[PaginationQueryDto, Query()]):
    data = file_service.pagination_find(
        PaginationOption(
            search=query.search,
            page=query.page,
            sorting=query.order_direction,
            sorting_col=query.order_by,
            limit=query.limit
        ),
        session,
    )
    return success_response(data=data, code=HTTPStatus.OK)

@router.post("/upload", response_model=AppResponse[FileModel])
def find(
    session: SessionDep,
    file: Annotated[UploadFile, File()],
    folder: Annotated[str, Form()],
):
    data = file_service.file_upload(session=session, file=file, folder=folder)
    return success_response(data=data, code=HTTPStatus.OK)
