

from sqlmodel import select
from app.core.database import get_session, setup_db
from app.models.category_model import Category


setup_db("postgresql://postgres:postgres@localhost:5432/event-booker")

session = get_session()

c1 = Category(name="Live Concert")

session.add(c1)
session.commit()
session.refresh(c1)

c1.description="This category is for description"

session.add(c1)
session.commit()


cats = session.exec(select(Category)).all()

print(cats)
