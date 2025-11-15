from http import HTTPStatus
from typing import Annotated, Any, List
from uuid import UUID
from fastapi import APIRouter, Body, Path, Query

from app.core.response import success_response
from app.dependencies.session_dep import SessionDep
from app.dependencies.auth_dep import AuthDeps, AuthAdminOnlyDeps, AuthDepsOnly
from app.dtos.pagination_query_dto import EventQueryDto, PaginationQueryDto
from app.dtos.response_dto import AppResponse
from app.dtos.event_dto import EventCreateDto, EventRead, EventUpdateDto
from app.services import event_service
from app.utils.pagination_utils import PaginationOption
from app.types.pagination_data import PaginationData


router = APIRouter(tags=["Event"], prefix="/event")


@router.post("/", response_model=AppResponse[EventRead])
def create_event(
    session: SessionDep,
    admin: AuthAdminOnlyDeps,
    body: Annotated[EventCreateDto, Body()],
):
    ev = event_service.create_event(str(admin.id), body, session)
    return success_response(data=EventRead.model_validate(ev), code=HTTPStatus.CREATED)


@router.get("/", response_model=AppResponse[PaginationData[EventRead]])
def list_events(
    session: SessionDep,
    query: Annotated[EventQueryDto, Query()],
):
    data = event_service.pagination_find(
        PaginationOption(
            search=query.search,
            page=query.page,
            sorting=query.order_direction,
            sorting_col=query.order_by,
            limit=query.limit,
        ),
        session,
        category_ids=query.categoryIds.split(",") if query.categoryIds != "" else None,
        status_in=query.statuses.split(",") if query.statuses != "" else None,
    )
    return success_response(data=data, code=HTTPStatus.OK)


@router.get("/{event_id}", response_model=AppResponse[EventRead])
def get_event(session: SessionDep, event_id: UUID = Path(...)):
    ev = event_service.find_by_id(str(event_id), session)
    if not ev:
        return success_response(data=None, code=HTTPStatus.NOT_FOUND)
    return success_response(data=EventRead.model_validate(ev), code=HTTPStatus.OK)


@router.patch("/{event_id}", response_model=AppResponse[EventRead])
def update_event(
    session: SessionDep,
    admin: AuthAdminOnlyDeps,
    body: Annotated[EventUpdateDto, Body()],
    event_id: UUID = Path(...),
):
    ev = event_service.update_event(str(event_id), body, session)
    return success_response(data=EventRead.model_validate(ev), code=HTTPStatus.OK)


@router.delete("/{event_id}", response_model=AppResponse[Any])
def delete_event(
    session: SessionDep, admin: AuthAdminOnlyDeps, event_id: UUID = Path(...)
):
    event_service.delete_event(str(event_id), session)
    return success_response(data=True, code=HTTPStatus.OK)
