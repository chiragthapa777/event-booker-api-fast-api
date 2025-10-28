from sqlmodel import Session
from app.core.config import get_config
from app.dtos.auth_dto import LoginRequestDto, LoginResponseDto, RegisterRequestDto
from app.dtos.user_dto import AppUserRead
from app.enums.role_enum import UserRole
from app.models.app_user_model import AppUser
from app.services import user_service
from app.types.errors import AppError
from app.utils.auth_utils import create_access_token
from app.utils.password_utils import hash_password, verify_password
from app.models import AppUser


def register_user(dto: RegisterRequestDto, session: Session) -> AppUserRead:
    user_found = user_service.find_by_email(dto.email, session)
    if user_found:
        raise AppError(message="Email already used")

    if dto.phone_number is not None:
        user_found = user_service.find_by_phone_number(dto.phone_number, session)
        if user_found:
            raise AppError(message="Phone number already used")

    hp = hash_password(dto.password)
    new_user = AppUser(
        full_name=dto.full_name,
        dob=dto.dob,
        password=hp,
        roles=UserRole.USER,
        email=dto.email,
        phone_number=dto.phone_number,
    )
    user_service.create(new_user, session)
    session.commit()
    return AppUserRead.model_validate(new_user)


def login_user(dto: LoginRequestDto, session: Session):
    user = None
    if dto.email:
        user = user_service.find_by_email(dto.email, session)
    elif dto.phone_number:
        user = user_service.find_by_phone_number(dto.phone_number, session)
    else:
        raise AppError(message="Phone number or email is required")

    if not user:
        raise AppError(message="Invalid credentials")

    if not verify_password(plain_password=dto.password, hashed_password=user.password):
        raise AppError(message="Invalid credentials")

    config = get_config()
    access_token = create_access_token(
        expires_in_minutes=24 * 60,
        user_id=user.id,
        secret_key=config.access_token_secret,
    )
    return LoginResponseDto(
        user=user_service.find_by_id(user.id, session), access_token=access_token
    )
