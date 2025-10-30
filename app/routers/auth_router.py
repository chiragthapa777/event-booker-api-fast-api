from typing import Annotated
from fastapi import Body
from fastapi.routing import APIRouter
from app.dependencies.auth_dep import AuthDeps
from app.dependencies.session_dep import SessionDep
from app.dtos.auth_dto import LoginRequestDto, LoginResponseDto, RegisterRequestDto
from app.core.response import success_response
from app.dtos.response_dto import AppResponse
from app.dtos.user_dto import AppUserRead
from app.enums.role_enum import UserRole
from app.models.app_user_model import AppUser
from app.services import auth_service

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
)


@router.post("/register", response_model=AppResponse[AppUserRead])
def register(
    body: Annotated[
        RegisterRequestDto,
        Body(),
    ],
    session: SessionDep,
):
    data = auth_service.register_user(body, session)
    return success_response(
        data=data, code=200, message="New user created successfully"
    )


@router.post("/login", response_model=AppResponse[LoginResponseDto])
def login(body: Annotated[LoginRequestDto, Body()], session: SessionDep):
    data = auth_service.login_user(body, session)
    return success_response(data=data, message="New user created successfully")


@router.get("/me", response_model=AppResponse[AppUser])
def me(user: AuthDeps):
    return success_response(data=AppUserRead.model_validate(user))
