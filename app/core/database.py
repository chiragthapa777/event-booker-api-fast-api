from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy import create_engine, Engine
from sqlmodel import Session
from sqlalchemy.orm import sessionmaker

engine: Optional[Engine] = None


def setup_db(db_url: str, echo_query: bool = False) -> None:
    global engine, SessionLocal
    engine = create_engine(url=db_url, echo=echo_query)


def close_db():
    engine.dispose()

def get_session():
    with Session(engine) as session:
        yield session

