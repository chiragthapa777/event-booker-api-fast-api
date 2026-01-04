import math
from typing import Any
from uuid import uuid4
import uuid
from fastapi import UploadFile
from sqlalchemy import func, text
from sqlmodel import Session, and_, select

from app.core.aws import s3
from app.models.file_model import File
from app.types.errors import AppError
from app.types.pagination_data import PaginationData
from app.utils.pagination_utils import PaginationOption


def file_upload(session: Session, file: UploadFile, folder: str)->File:
    key = f"{folder}/{uuid4()}.{file.filename.split('.')[-1]}"
    s3.upload_file(file.file, key)
    newFile = File(
        file_path=key,
        size=file.size,
        type=file.content_type,
    )
    session.add(newFile)
    session.commit()
    session.refresh(newFile)
    return newFile

def pagination_find(
    pagination_options: PaginationOption, session: Session
) -> PaginationData:
    where_conditions = []
    params = {}

    if pagination_options.search:
        params["search"] = f"%{pagination_options.search}%"
        raw_where = text(
            "(file.file_path ILIKE :search "
        )
        where_conditions.append(raw_where)   

    # Base Query
    sq = select(File)
    
    # Filters
    if where_conditions:
        sq.where(and_(*where_conditions))

    # Sorting
    sort_col = pagination_options.sorting_col or "created_at"
    sort_asc = pagination_options.sorting == "asc"

    order_expr = File.created_at.asc() if sort_asc else File.created_at.desc()

    sq = sq.order_by(order_expr)

    data_list = session.exec(
        sq
        .limit(pagination_options.limit)
        .offset(pagination_options.get_offset()),
        params=params
    ).all()

    total = session.exec(select(func.count(File.id)).where(*where_conditions),params=params).one()
    total_page = math.ceil(total / pagination_options.limit)

    return PaginationData(list=data_list, total=total, total_page=total_page)

def find_by_id(id: str | uuid.UUID, session: Session) -> File | None:
    # Accept either a uuid.UUID or a string. If it's a string, validate/parse it
    if id is None:
        return None
    try:
        id_uuid = id if isinstance(id, uuid.UUID) else uuid.UUID(str(id))
    except Exception:
        # Provide a service-level error instead of raw ValueError from uuid
        raise AppError(message=f"invalid file id: {id}")

    data = session.exec(select(File).where(File.id == id_uuid)).first()
    return data

