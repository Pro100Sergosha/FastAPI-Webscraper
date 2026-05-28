from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.DB_URL)


def create_db_and_tables():
    """
    Creates the database and all tables defined in SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Provides a database session generator.

    :yield: A SQLModel Session object.
    """
    with Session(engine) as session:
        yield session
