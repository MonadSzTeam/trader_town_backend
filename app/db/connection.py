from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# Create sync engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True to see SQL queries in logs
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create sync session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    Dependency for getting database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
