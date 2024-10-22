from decouple import config
from fastapi import Query
from sqlmodel import Session, create_engine

engine = create_engine(config("DATABASE_URL"), credentials_path=config("GOOGLE_APPLICATION_CREDENTIALS"), echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def pagination(page: int = Query(1, ge=1), size: int = Query(5, ge=5)):
    offset = (page - 1) * size if page > 1 else 0
    return (page, size, offset)
