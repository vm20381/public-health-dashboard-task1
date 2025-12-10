"""
Tests for dashboard utility functions.
"""
import pytest
import pandas as pd
from datetime import datetime
from src.db.engine import get_engine
from src.db.models import Base
from src.db.crud_sql import create_report_sql
from src.dashboard_utils import load_data_from_db

@pytest.fixture
def db_connection():
    """Fixture to provide a clean in-memory database connection."""
    engine = get_engine(":memory:")
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        yield conn

def test_load_data_from_db(db_connection):
    """Test loading data from the database into a DataFrame."""
    # Insert some sample data
    report1 = {
        "sno": 1,
        "observation_date": datetime(2020, 1, 22),
        "province_state": "Anhui",
        "country_region": "China",
        "last_update": datetime(2020, 1, 22, 17, 0, 0),
        "confirmed": 10,
        "deaths": 0,
        "recovered": 0
    }
    report2 = {
        "sno": 2,
        "observation_date": datetime(2020, 1, 23),
        "province_state": None,
        "country_region": "US",
        "last_update": datetime(2020, 1, 23, 17, 0, 0),
        "confirmed": 5,
        "deaths": 1,
        "recovered": 1
    }
    create_report_sql(db_connection, report1)
    create_report_sql(db_connection, report2)
    
    # Load data
    df = load_data_from_db(db_connection)
    
    # Verify DataFrame structure and content
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "country_region" in df.columns
    assert "confirmed" in df.columns
    
    # Check data types
    # observation_date should be datetime
    assert pd.api.types.is_datetime64_any_dtype(df["observation_date"])
    
    # Check values
    assert df[df["country_region"] == "China"]["confirmed"].iloc[0] == 10
