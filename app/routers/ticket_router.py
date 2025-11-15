from http import HTTPStatus
from typing import Annotated, Any, List
from uuid import UUID
from fastapi import APIRouter, Body, Path

from app.core.response import success_response
from app.dependencies.session_dep import SessionDep
from app.dependencies.auth_dep import AuthAdminOnlyDeps
from app.dtos.ticket_dto import TicketCreateDto, TicketRead
from app.dtos.response_dto import AppResponse
from app.services import ticket_service


router = APIRouter(tags=["Ticket"], prefix="/ticket")


@router.post("/", response_model=AppResponse[TicketRead])
def create_ticket(session: SessionDep, admin: AuthAdminOnlyDeps, body: Annotated[TicketCreateDto, Body()]):
    t = ticket_service.create_ticket(body, session)
    return success_response(data=TicketRead.model_validate(t), code=HTTPStatus.CREATED)


@router.get("/event/{event_id}", response_model=AppResponse[List[TicketRead]])
def tickets_by_event(session: SessionDep, event_id: UUID = Path(...)):
    tickets = ticket_service.find_by_event(str(event_id), session)
    return success_response(data=[TicketRead.model_validate(t) for t in tickets], code=HTTPStatus.OK)


@router.get("/{id}", response_model=AppResponse[TicketRead])
def get_ticket(session: SessionDep, id: UUID = Path(...)):
    t = ticket_service.find_by_id(str(id), session)
    if not t:
        return success_response(data=None, code=HTTPStatus.NOT_FOUND)
    return success_response(data=TicketRead.model_validate(t), code=HTTPStatus.OK)
