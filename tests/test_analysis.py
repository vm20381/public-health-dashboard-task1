"""
Tests for the analysis module.
"""
import pytest
import pandas as pd
from datetime import datetime
from src.analysis import (
    filter_data,
    get_summary_stats,
    get_trend_over_time,
    get_top_countries
)

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for analysis tests."""
    data = {
        "observation_date": [
            datetime(2020, 1, 1), datetime(2020, 1, 1), 
            datetime(2020, 1, 2), datetime(2020, 1, 2)
        ],
        "country_region": ["China", "US", "China", "US"],
        "confirmed": [100, 50, 150, 70],
        "deaths": [10, 5, 15, 7],
        "recovered": [50, 20, 80, 30]
    }
    return pd.DataFrame(data)

def test_filter_data_by_country(sample_df):
    """Test filtering by country."""
    result = filter_data(sample_df, country="China")
    assert len(result) == 2
    assert all(result["country_region"] == "China")

def test_filter_data_by_date_range(sample_df):
    """Test filtering by date range."""
    start = datetime(2020, 1, 2)
    result = filter_data(sample_df, start_date=start)
    assert len(result) == 2
    assert result["observation_date"].min() >= start

def test_get_summary_stats(sample_df):
    """Test calculating summary statistics."""
    stats = get_summary_stats(sample_df)
    # Should take the latest date (Jan 2)
    # China: 150, US: 70 -> Total: 220
    assert stats["total_confirmed"] == 220
    # Deaths: 15 + 7 = 22
    assert stats["total_deaths"] == 22
    # Recovered: 80 + 30 = 110
    assert stats["total_recovered"] == 110

def test_get_trend_over_time(sample_df):
    """Test aggregating data by date."""
    trend = get_trend_over_time(sample_df)
    
    # Should have 2 rows (Jan 1 and Jan 2)
    assert len(trend) == 2
    
    # Check Jan 1 totals
    jan_1 = trend[trend["observation_date"] == datetime(2020, 1, 1)].iloc[0]
    assert jan_1["confirmed"] == 150  # 100 + 50

def test_get_top_countries(sample_df):
    """Test getting top countries by confirmed cases."""
    # Should use latest data (Jan 2)
    # China: 150, US: 70
    top = get_top_countries(sample_df, n=1)
    
    assert len(top) == 1
    assert top.iloc[0]["country_region"] == "China"
    assert top.iloc[0]["confirmed"] == 150
