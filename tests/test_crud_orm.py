"""
Tests for ORM CRUD operations.
"""
import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from src.db.engine import get_engine, get_session_maker
from src.db.models import Base, CovidReport
from src.db.crud_orm import create_report, get_reports, update_report, delete_report, bulk_insert

@pytest.fixture
def db_session():
    """Fixture to provide a clean in-memory database session for each test."""
    engine = get_engine(":memory:")
    Base.metadata.create_all(engine)
    SessionLocal = get_session_maker(engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_create_report(db_session: Session):
    """Test creating a single report."""
    report_data = {
        "sno": 1,
        "observation_date": datetime(2020, 1, 22),
        "province_state": "Anhui",
        "country_region": "Mainland China",
        "last_update": datetime(2020, 1, 22, 17, 0),
        "confirmed": 1,
        "deaths": 0,
        "recovered": 0
    }
    
    report_id = create_report(db_session, report_data)
    assert report_id == 1
    
    # Verify it's in the DB
    report = db_session.query(CovidReport).filter_by(sno=1).first()
    assert report is not None
    assert report.country_region == "Mainland China"

def test_get_reports_filters(db_session: Session):
    """Test retrieving reports with filters."""
    # Seed data
    r1 = CovidReport(sno=1, country_region="China", observation_date=datetime(2020, 1, 1))
    r2 = CovidReport(sno=2, country_region="US", observation_date=datetime(2020, 1, 2))
    db_session.add_all([r1, r2])
    db_session.commit()
    
    # Filter by country
    results = get_reports(db_session, country="China")
    assert len(results) == 1
    assert results[0].country_region == "China"
    
    # Filter by date range
    results = get_reports(db_session, start_date=datetime(2020, 1, 2))
    assert len(results) == 1
    assert results[0].sno == 2

def test_update_report(db_session: Session):
    """Test updating an existing report."""
    r1 = CovidReport(sno=1, country_region="China", confirmed=10)
    db_session.add(r1)
    db_session.commit()
    
    success = update_report(db_session, 1, {"confirmed": 20})
    assert success is True
    
    db_session.refresh(r1)
    assert r1.confirmed == 20

def test_update_missing_report_returns_false(db_session: Session):
    """Test updating a non-existent report."""
    success = update_report(db_session, 999, {"confirmed": 20})
    assert success is False

def test_delete_report(db_session: Session):
    """Test deleting a report."""
    r1 = CovidReport(sno=1, country_region="China")
    db_session.add(r1)
    db_session.commit()
    
    success = delete_report(db_session, 1)
    assert success is True
    
    assert db_session.query(CovidReport).filter_by(sno=1).first() is None

def test_bulk_insert(db_session: Session):
    """Test inserting multiple records at once."""
    records = [
        {"sno": 1, "country_region": "A", "observation_date": datetime(2020, 1, 1)},
        {"sno": 2, "country_region": "B", "observation_date": datetime(2020, 1, 1)},
    ]
    
    count = bulk_insert(db_session, records)
    assert count == 2
    
    assert db_session.query(CovidReport).count() == 2
