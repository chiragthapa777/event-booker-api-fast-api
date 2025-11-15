from http import HTTPStatus
from typing import Annotated, Any, List
from fastapi import APIRouter, Body

from app.core.response import success_response
from app.dependencies.session_dep import SessionDep
from app.dependencies.auth_dep import AuthAdminOnlyDeps
from app.dtos.category_dto import CategoryCreateDto, CategoryRead
from app.dtos.response_dto import AppResponse
from app.services import category_service


router = APIRouter(tags=["Category"], prefix="/category")


@router.get("/", response_model=AppResponse[List[CategoryRead]])
def list_categories(session: SessionDep):
    cats = category_service.find_all(session)
    return success_response(data=[CategoryRead.model_validate(c) for c in cats], code=HTTPStatus.OK)


@router.post("/", response_model=AppResponse[CategoryRead])
def create_category(session: SessionDep, admin: AuthAdminOnlyDeps, body: Annotated[CategoryCreateDto, Body()]):
    new = category_service.create(body, session)
    return success_response(data=CategoryRead.model_validate(new), code=HTTPStatus.CREATED)
