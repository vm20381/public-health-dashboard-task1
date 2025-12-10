"""
Tests for Raw SQL CRUD operations.
"""
import pytest
from datetime import datetime
from sqlalchemy import text

from src.db.engine import get_engine
from src.db.models import Base
from src.db.crud_sql import create_report_sql, get_reports_sql, update_report_sql, delete_report_sql

@pytest.fixture
def db_connection():
    """Fixture to provide a clean in-memory database connection for each test."""
    engine = get_engine(":memory:")
    Base.metadata.create_all(engine)
    
    with engine.connect() as conn:
        yield conn
        # No need to explicitly close as context manager handles it, 
        # but for in-memory DB, data is lost when connection closes if it's the only one.
        # However, engine keeps a pool.

def test_create_report_sql(db_connection):
    """Test creating a report using raw SQL."""
    report_data = {
        "sno": 1,
        "observation_date": datetime(2020, 1, 22),
        "province_state": "Anhui",
        "country_region": "China",
        "last_update": datetime(2020, 1, 22, 17, 0),
        "confirmed": 10,
        "deaths": 0,
        "recovered": 0
    }
    
    create_report_sql(db_connection, report_data)
    
    # Verify with raw SQL
    result = db_connection.execute(text("SELECT * FROM covid_reports WHERE sno = 1")).mappings().first()
    assert result is not None
    assert result["country_region"] == "China"
    assert result["confirmed"] == 10

def test_get_reports_sql(db_connection):
    """Test retrieving reports using raw SQL."""
    # Seed data
    db_connection.execute(
        text("INSERT INTO covid_reports (sno, country_region, observation_date, confirmed) VALUES (:sno, :country, :date, :conf)"),
        [
            {"sno": 1, "country": "China", "date": "2020-01-01 00:00:00", "conf": 100},
            {"sno": 2, "country": "US", "date": "2020-01-02 00:00:00", "conf": 200}
        ]
    )
    db_connection.commit()
    
    # Filter by country
    results = get_reports_sql(db_connection, country="China")
    assert len(results) == 1
    assert results[0]["country_region"] == "China"
    
    # Filter by date
    results = get_reports_sql(db_connection, start_date="2020-01-02")
    assert len(results) == 1
    assert results[0]["sno"] == 2

def test_update_report_sql(db_connection):
    """Test updating a report using raw SQL."""
    db_connection.execute(
        text("INSERT INTO covid_reports (sno, country_region, confirmed) VALUES (1, 'China', 10)")
    )
    db_connection.commit()
    
    success = update_report_sql(db_connection, 1, {"confirmed": 50})
    assert success is True
    
    result = db_connection.execute(text("SELECT confirmed FROM covid_reports WHERE sno = 1")).scalar()
    assert result == 50

def test_delete_report_sql(db_connection):
    """Test deleting a report using raw SQL."""
    db_connection.execute(
        text("INSERT INTO covid_reports (sno, country_region) VALUES (1, 'China')")
    )
    db_connection.commit()
    
    success = delete_report_sql(db_connection, 1)
    assert success is True
    
    result = db_connection.execute(text("SELECT * FROM covid_reports WHERE sno = 1")).first()
    assert result is None
