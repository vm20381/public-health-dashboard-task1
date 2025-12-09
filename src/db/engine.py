"""
Database engine and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

def get_engine(db_path: str) -> Engine:
    """
    Create a SQLAlchemy engine for SQLite.
    
    Args:
        db_path: Path to the SQLite database file.
        
    Returns:
        Engine: SQLAlchemy engine instance.
    """
    # SQLite URL format: sqlite:///path/to/db
    # For relative paths, 3 slashes. For absolute, 4 slashes (on Unix) or specific handling on Windows.
    # We'll assume the user passes a valid path string, and we prepend sqlite:///
    
    # If db_path is ":memory:", use it directly
    if db_path == ":memory:":
        url = "sqlite:///:memory:"
    else:
        url = f"sqlite:///{db_path}"
        
    return create_engine(url, echo=False, future=True)

def get_session_maker(engine: Engine) -> sessionmaker:
    """
    Create a session factory for the given engine.
    
    Args:
        engine: SQLAlchemy engine.
        
    Returns:
        sessionmaker: Factory for creating new Session objects.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
