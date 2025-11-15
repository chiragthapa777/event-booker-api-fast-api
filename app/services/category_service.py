import math
from sqlmodel import select, Session
from sqlalchemy import func
from app.models.category_model import Category
from app.types.pagination_data import PaginationData
from app.utils.pagination_utils import PaginationOption
from app.dtos.category_dto import CategoryCreateDto, CategoryRead


def create(dto: CategoryCreateDto, session: Session) -> Category:
    new = Category(name=dto.name, description=dto.description)
    session.add(new)
    session.commit()
    session.refresh(new)
    return new


def find_all(session: Session):
    return session.exec(select(Category).order_by(Category.created_at.desc())).all()


def find_by_id(id: str, session: Session):
    return session.exec(select(Category).where(Category.id == id)).first()
