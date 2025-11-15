from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    HTTPException,
    Path,
    Query,
)

from app.core.response import success_response
from app.dependencies.auth_dep import AuthDeps, AuthDepsOnly
from app.dependencies.session_dep import SessionDep
from app.dtos.pagination_query_dto import PaginationQueryDto
from app.dtos.response_dto import AppResponse
from app.dtos.user_dto import AppUserRead, ProfileUpdateRequestDto, VerifyCode
from app.models.app_user_model import AppUser
from app.services import user_service
from app.types.errors import AppError
from app.types.pagination_data import PaginationData
from app.utils.pagination_utils import PaginationOption


router = APIRouter(
    tags=["User"],
    prefix="/user",
    dependencies=[AuthDepsOnly],
)


@router.get("/", response_model=AppResponse[PaginationData[AppUserRead]])
def find(session: SessionDep, query: Annotated[PaginationQueryDto, Query()]):
    data = user_service.pagination_find(
        PaginationOption(
            search=query.search,
            page=query.page,
            sorting=query.order_direction,
            sorting_col=query.order_by,
            limit=query.limit,
        ),
        session,
    )
    return success_response(data=data, code=HTTPStatus.OK)

@router.get("/verify-email", response_model=AppResponse[str])
def verify_email(
    session: SessionDep,
    user: AuthDeps,
    background_tasks: BackgroundTasks,
):
    if user.email_verified_at != None:
        raise AppError(message="email already verified")
    user = user_service.send_email_validation_code(
        user=user, session=session, background_tasks=background_tasks
    )
    return success_response(data="code will be sent to your email shortly")


@router.post("/verify-email", response_model=AppResponse[str])
def verify_email(
    session: SessionDep,
    user: AuthDeps,
    body: Annotated[VerifyCode, Body()],
):
    if user.email_verified_at != None:
        raise AppError(message="email already verified")
    user_service.verify_email_validation_code(
        user=user, session=session, code=body.code
    )
    return success_response(data="email verified successfully")

@router.get("/{user_id}", response_model=AppResponse[AppUserRead])
def find(session: SessionDep, user_id: UUID = Path(..., description="User UUID")):
    user = user_service.find_by_id(user_id, session)
    if not user:
        raise HTTPException(detail="User not found", status_code=HTTPStatus.NOT_FOUND)
    return success_response(
        data=AppUserRead.model_validate(user), code=HTTPStatus.FOUND
    )


@router.patch("/update-profile", response_model=AppResponse[AppUserRead])
def update_profile(
    session: SessionDep,
    user: AuthDeps,
    body: Annotated[ProfileUpdateRequestDto, Body()],
):
    user = user_service.update_profile(user, body, session)
    return success_response(
        data=AppUserRead.model_validate(user), code=HTTPStatus.FOUND
    )



