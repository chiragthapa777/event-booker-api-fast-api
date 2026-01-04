import math
from typing import List, Optional
import uuid
from sqlalchemy import func, text, and_
from sqlmodel import Session, select, update
from app.models.event_model import Event
from app.models.event_category_model import EventCategory
from app.models.category_model import Category
from app.services import file_service
from app.types.pagination_data import PaginationData
from app.utils.pagination_utils import PaginationOption
from app.dtos.event_dto import (
    EventCreateDto,
    EventRead,
    EventUpdateDto,
)
from app.types.errors import AppError
from sqlalchemy.orm import joinedload, selectinload
from app.services import ticket_service
from app.dtos.ticket_dto import TicketRead


def _slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def create_event(admin_id: str, dto: EventCreateDto, session: Session) -> Event:
    # Validate files
    for file_field in [
        dto.event_layout_photo_id,
        dto.event_banner_photo_id,
        dto.event_photo_id,
    ]:
        if file_field:
            f = file_service.find_by_id(file_field, session)
            if not f:
                raise AppError(message="file not found")

    slug = _slugify(dto.name)
    # ensure unique slug
    exists = session.exec(select(Event).where(Event.slug == slug)).first()
    if exists:
        # make slug unique using timestamp-ish fallback
        slug = f"{slug}-{str(func.now())}"

    ev = Event(
        admin_id=admin_id,
        name=dto.name,
        slug=slug,
        date=dto.date,
        venue=dto.venue,
        lng=dto.lng,
        lat=dto.lat,
        description=dto.description,
        terms_and_condition=dto.terms_and_condition,
        event_layout_photo_id=dto.event_layout_photo_id,
        event_banner_photo_id=dto.event_banner_photo_id,
        event_photo_id=dto.event_photo_id,
    )
    session.add(ev)

    # categories
    if dto.category_ids:
        for cid in dto.category_ids:
            try:
                cid_uuid = uuid.UUID(cid)
            except Exception:
                raise AppError(message=f"invalid category id: {cid}")
            cat = session.exec(select(Category).where(Category.id == cid_uuid)).first()
            if not cat:
                raise AppError(message=f"category {cid} not found")
            ec = EventCategory(event_id=ev.id, category_id=cat.id)
            session.add(ec)

    # create tickets if provided
    if getattr(dto, "tickets", None):
        try:
            ticket_service.upsert_tickets_for_event(str(ev.id), dto.tickets, session)
        except Exception as e:
            # rollback created event on ticket failures to keep consistency
            session.exec(
                text("DELETE FROM event_category WHERE event_id = :event_id"),
                params={"event_id": str(ev.id)},
            )
            session.exec(
                text("DELETE FROM event WHERE id = :id"), params={"id": str(ev.id)}
            )
            raise AppError(e=str(e))
    session.commit()
    session.refresh(ev)
    return ev


def update_event(event_id: str, dto: EventUpdateDto, session: Session) -> Event:
    ev = session.exec(select(Event).where(Event.id == event_id)).first()
    if not ev:
        raise AppError(message="Event not found")

    update_data = dto.model_dump(exclude_unset=True)
    # validate files
    for fkey in ("event_layout_photo_id", "event_banner_photo_id", "event_photo_id"):
        if fkey in update_data and update_data[fkey] is not None:
            f = file_service.find_by_id(update_data[fkey], session)
            if not f:
                raise AppError(message="file not found")

    # update scalar fields
    session.exec(update(Event).where(Event.id == ev.id).values(update_data))

    # update categories if provided
    if "category_ids" in update_data:
        # delete existing event categories
        session.exec(
            "DELETE FROM event_category WHERE event_id = :event_id",
            params={"event_id": str(ev.id)},
        )
        if update_data["category_ids"]:
            for cid in update_data["category_ids"]:
                try:
                    cid_uuid = uuid.UUID(cid)
                except Exception:
                    raise AppError(message=f"invalid category id: {cid}")
                cat = session.exec(
                    select(Category).where(Category.id == cid_uuid)
                ).first()
                if not cat:
                    raise AppError(message=f"category {cid} not found")
                ec = EventCategory(event_id=ev.id, category_id=cid_uuid)
                session.add(ec)

    # handle tickets upsert if provided
    if "tickets" in update_data and update_data["tickets"] is not None:
        # use ticket_service to create/update tickets for this event
        ticket_service.upsert_tickets_for_event(
            str(ev.id), update_data["tickets"], session
        )

    session.commit(ev)
    session.refresh(ev)
    return ev


def delete_event(event_id: str, session: Session) -> None:
    ev = session.exec(select(Event).where(Event.id == event_id)).first()
    if not ev:
        raise AppError(message="Event not found")
    ev.status = "inactive"
    session.add(ev)
    session.commit()


def find_by_id(event_id: str, session: Session) -> Optional[Event]:
    return session.exec(
        select(Event)
        .options(
            joinedload(Event.event_banner_photo),
            joinedload(Event.event_layout_photo),
            joinedload(Event.event_photo),
            selectinload(Event.categories),
            selectinload(Event.tickets),
        )
        .where(Event.id == event_id)
    ).first()


def pagination_find(
    pagination_options: PaginationOption,
    session: Session,
    category_ids: Optional[List[str]] = None,
    status_in: Optional[List[str]] = None,
) -> PaginationData[EventRead]:
    where_conditions = []
    params = {}

    if pagination_options.search:
        params["search"] = f"%{pagination_options.search}%"
        where_conditions.append(
            text("(event.name ILIKE :search OR event.description ILIKE :search)")
        )

    if status_in:
        where_conditions.append(text("event.status = ANY(:status_in)"))
        params["status_in"] = status_in

    if category_ids:
        where_conditions.append(
            Event.id.in_(
                select(EventCategory.event_id).where(
                    EventCategory.category_id.in_(category_ids)
                )
            )
        )

    sq = select(Event)

    sq = sq.options(
        joinedload(Event.event_banner_photo),
        joinedload(Event.event_layout_photo),
        joinedload(Event.event_photo),  # for 1 to 1 or many to 1 joined good
        selectinload(
            Event.categories
        ),  # for 1 to many  and many to many selectinload is best
        selectinload(Event.tickets),
    )

    if where_conditions:
        sq = sq.where(and_(*where_conditions))

    # Sorting
    sort_col = pagination_options.sorting_col or "created_at"
    sort_asc = pagination_options.sorting == "asc"
    order_expr = (
        Event.name.asc()
        if sort_col == "name" and sort_asc
        else (
            Event.name.desc()
            if sort_col == "name"
            else Event.created_at.asc() if sort_asc else Event.created_at.desc()
        )
    )
    sq = sq.order_by(order_expr)

    # Execute main query
    data_list = session.exec(
        sq.limit(pagination_options.limit).offset(pagination_options.get_offset()),
        params=params,
    ).all()

    # Count total
    total = session.exec(
        select(func.count(Event.id)).where(*where_conditions), params=params
    ).one()
    total_page = (
        math.ceil(total / pagination_options.limit) if pagination_options.limit else 0
    )

    return PaginationData(
        list=[EventRead.model_validate(data) for data in data_list],
        total=total,
        total_page=total_page,
    )
