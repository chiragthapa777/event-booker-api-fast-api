from sqlmodel import Session, select, update
from app.models.event_ticket_model import EventTicket
from app.types.errors import AppError
from typing import List, Optional


def create_ticket(event_id: str, dto, session: Session) -> EventTicket:
    """Create a single ticket for given event_id. dto has name, price, total_qty."""
    ticket = EventTicket(
        event_id=event_id,
        name=dto.name,
        price=dto.price,
        total_qty=dto.total_qty,
    )
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def update_ticket(ticket_id: str, dto, session: Session) -> EventTicket:
    t = session.exec(select(EventTicket).where(EventTicket.id == ticket_id)).first()
    if not t:
        raise AppError(message="Ticket not found")
    update_data = dto.model_dump(exclude_unset=True)
    session.exec(update(EventTicket).where(EventTicket.id == ticket_id).values(update_data))
    return t


def upsert_tickets_for_event(event_id: str, tickets: List, session: Session) -> List[EventTicket]:
    """Given a list of TicketInputDto-like objects, create or update tickets for an event.

    Behavior:
    - If an item has `id`, attempt to update that ticket.
    - If no `id`, create a new ticket linked to event_id.
    - Tickets not referenced are left untouched.
    """
    result = []
    for item in tickets:
        if getattr(item, "id", None):
            t = update_ticket(item.id, item, session)
            result.append(t)
        else:
            t = create_ticket(event_id, item, session)
            result.append(t)
    return result


def find_by_event(event_id: str, session: Session):
    return session.exec(select(EventTicket).where(EventTicket.event_id == event_id)).all()


def find_by_id(id: str, session: Session):
    return session.exec(select(EventTicket).where(EventTicket.id == id)).first()
