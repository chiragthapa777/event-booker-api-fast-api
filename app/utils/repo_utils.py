from sqlmodel import Session
from sqlalchemy.orm import SessionTransaction

def in_transaction(session : Session | SessionTransaction)->bool:
    return isinstance(session, SessionTransaction)