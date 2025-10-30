import math
from typing import Any
from sqlalchemy import func, text
from sqlmodel import Session, and_, select, update
from app.dtos.user_dto import AppUserRead, ProfileUpdateRequestDto
from app.models.app_user_model import AppUser
from app.services import file_service
from app.types.errors import AppError
from app.types.pagination_data import PaginationData
from app.utils.pagination_utils import PaginationOption
from sqlalchemy.orm import joinedload


def create(user: AppUser, session: Session):
    session.add(user)


def find_by_email(email: str, session: Session) -> AppUser | None:
    return session.exec(select(AppUser).where(AppUser.email == email)).first()


def find_by_id(id: str, session: Session) -> AppUser | None:
    data = session.exec(
        select(AppUser).options(joinedload(AppUser.profile)).where(AppUser.id == id)
    ).first()
    return data


def find_by_phone_number(phone_number: str, session: Session) -> AppUser | None:
    return session.exec(
        select(AppUser).where(AppUser.phone_number == phone_number)
    ).first()


def update_profile(user: AppUser, updateDto: ProfileUpdateRequestDto, session: Session)->AppUser:
    update_dict = updateDto.model_dump(exclude_unset=True)
    if 'phone_number' in update_dict:
        update_dict['phone_verified_at']=None
    if 'profile_id' in update_dict and update_dict['profile_id'] is not None:
        profile = file_service.find_by_id(update_dict["profile_id"],session)
        if not profile:
            raise AppError(message="profile photo not found")
    session.exec(update(AppUser).where(AppUser.id == user.id).values(update_dict))
    session.commit()
    session.refresh(user)
    return user


def pagination_find(
    pagination_options: PaginationOption, session: Session
) -> PaginationData[AppUserRead]:
    where_conditions = []
    params = {}

    if pagination_options.search:
        params["search"] = f"%{pagination_options.search}%"
        raw_where = text(
            "(app_user.full_name ILIKE :search "
            "OR app_user.email ILIKE :search "
            "OR app_user.phone_number ILIKE :search)"
        )
        where_conditions.append(raw_where)

    # Base Query
    sq = select(AppUser)

    # Joins
    sq.options(joinedload(AppUser.profile))

    # Filters
    if where_conditions:
        sq.where(and_(*where_conditions))

    # Sorting
    sort_col = pagination_options.sorting_col or "created_at"
    sort_asc = pagination_options.sorting == "asc"

    if sort_col == "full_name":
        order_expr = AppUser.full_name.asc() if sort_asc else AppUser.full_name.desc()
    elif sort_col == "email":
        order_expr = AppUser.email.asc() if sort_asc else AppUser.email.desc()
    else:
        order_expr = AppUser.created_at.asc() if sort_asc else AppUser.created_at.desc()

    sq = sq.order_by(order_expr)

    data_list = session.exec(
        sq.limit(pagination_options.limit).offset(pagination_options.get_offset()),
        params=params,
    ).all()

    total = session.exec(
        select(func.count(AppUser.id)).where(*where_conditions), params=params
    ).one()
    total_page = math.ceil(total / pagination_options.limit)

    return PaginationData(
        list=[AppUserRead.model_validate(data) for data in data_list],
        total=total,
        total_page=total_page,
    )
