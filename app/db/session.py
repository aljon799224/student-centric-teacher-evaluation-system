"""Session."""

from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from app.core.config import settings


load_dotenv()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)  # pragma: no cover
else:
    # Connect the database if exists
    engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency callable for DB
def get_db() -> Generator:
    """Yield a new database session."""
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
