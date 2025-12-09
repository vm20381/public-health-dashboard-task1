"""
Tests for database engine and session creation.
"""
import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from src.db.engine import get_engine, get_session_maker
from src.db.models import Base

def test_get_engine_creates_engine(tmp_path):
    """Test that get_engine returns a SQLAlchemy Engine."""
    db_path = tmp_path / "test.db"
    engine = get_engine(str(db_path))
    assert isinstance(engine, Engine)

def test_engine_can_connect(tmp_path):
    """Test that the engine can establish a connection."""
    db_path = tmp_path / "test.db"
    engine = get_engine(str(db_path))
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1

def test_get_session_maker_returns_session(tmp_path):
    """Test that the session maker creates valid sessions."""
    db_path = tmp_path / "test.db"
    engine = get_engine(str(db_path))
    SessionLocal = get_session_maker(engine)
    
    session = SessionLocal()
    assert isinstance(session, Session)
    session.close()

def test_create_tables(tmp_path):
    """Test that tables defined in models can be created."""
    db_path = tmp_path / "test.db"
    engine = get_engine(str(db_path))
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Verify table exists
    with engine.connect() as conn:
        # SQLite specific query to check for table existence
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='covid_reports'")).scalar()
        assert result == "covid_reports"
