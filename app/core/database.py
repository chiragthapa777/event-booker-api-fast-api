from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlmodel import Session

engine: Optional[Engine] = None


def setup_db(db_url: str, echo_query: bool = False) -> None:
    global engine
    engine = create_engine(url=db_url, echo=echo_query)


def close_db():
    engine.dispose()

def get_session():
    with Session(engine) as session:
        yield session

