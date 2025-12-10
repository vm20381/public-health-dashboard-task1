"""
Integration test for the database initialization process.
Verifies that data from the CSV makes it all the way into the database.
"""
import pytest
from pathlib import Path
from sqlalchemy import text
from src.db.engine import get_engine
from src.db.models import Base

# We'll use the actual init_db logic but point it to a test DB
from src.data_access import load_csv
from src.cleaning import clean_covid_df, to_records
from src.db.crud_orm import bulk_insert
from sqlalchemy.orm import sessionmaker

def test_init_db_process(tmp_path):
    """
    Simulate the full init_db.py process:
    Load CSV -> Clean -> Create DB -> Insert -> Verify
    """
    # 1. Setup paths
    # Create a tiny dummy CSV to test the pipeline without loading the huge real file
    csv_path = tmp_path / "dummy_data.csv"
    csv_path.write_text(
        "SNo,ObservationDate,Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered\n"
        "1,01/22/2020,Anhui,Mainland China,1/22/2020 17:00,1.0,0.0,0.0\n"
        "2,01/22/2020,Beijing,Mainland China,1/22/2020 17:00,14.0,0.0,0.0\n"
    )
    
    db_path = tmp_path / "test_covid.db"
    
    # 2. Run the pipeline logic (mimicking init_db.py)
    df_raw = load_csv(str(csv_path))
    df_clean = clean_covid_df(df_raw)
    records = to_records(df_clean)
    
    engine = get_engine(str(db_path))
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        count = bulk_insert(session, records)
        assert count == 2
    finally:
        session.close()
        
    # 3. Verify data is actually in the DB file
    # Re-connect to the file to prove persistence
    engine_check = get_engine(str(db_path))
    with engine_check.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM covid_reports")).scalar()
        assert result == 2
        
        row = conn.execute(text("SELECT country_region, confirmed FROM covid_reports WHERE sno=2")).mappings().first()
        assert row["country_region"] == "Mainland China"
        assert row["confirmed"] == 14
