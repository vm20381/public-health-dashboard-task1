"""
Analysis module for processing and summarizing COVID-19 data.
"""
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime

def filter_data(
    df: pd.DataFrame, 
    country: Optional[str] = None, 
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """
    Filter the DataFrame based on country and date range.
    """
    out = df.copy()
    
    if country:
        out = out[out["country_region"] == country]
        
    if start_date:
        out = out[out["observation_date"] >= start_date]
        
    if end_date:
        out = out[out["observation_date"] <= end_date]
        
    return out

def _get_latest_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Helper to get the latest data for each region.
    """
    if df.empty:
        return df
        
    group_cols = ["country_region"]
    if "province_state" in df.columns:
        group_cols.append("province_state")
        
    # Sort by date descending and keep the first (latest) for each location
    return df.sort_values("observation_date", ascending=False).drop_duplicates(subset=group_cols)

def get_summary_stats(df: pd.DataFrame) -> Dict[str, int]:
    """
    Calculate total confirmed, deaths, and recovered cases.
    Uses the latest data for each region within the filtered range.
    """
    latest_df = _get_latest_data(df)
    
    return {
        "total_confirmed": int(latest_df["confirmed"].sum()),
        "total_deaths": int(latest_df["deaths"].sum()),
        "total_recovered": int(latest_df["recovered"].sum())
    }

def get_trend_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate data by observation_date to show trends over time.
    """
    return df.groupby("observation_date")[["confirmed", "deaths", "recovered"]].sum().reset_index()

def get_top_countries(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Get the top n countries by total confirmed cases.
    Uses the latest data for each region.
    """
    latest_df = _get_latest_data(df)
    
    # Group by country and sum
    grouped = latest_df.groupby("country_region")[["confirmed", "deaths", "recovered"]].sum().reset_index()
    
    # Sort by confirmed descending and take top n
    return grouped.sort_values("confirmed", ascending=False).head(n)
