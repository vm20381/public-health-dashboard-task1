"""
Utility functions for the Streamlit dashboard.
"""
import pandas as pd
from sqlalchemy.engine import Connection
from src.db.crud_sql import get_reports_sql

def load_data_from_db(conn: Connection) -> pd.DataFrame:
    """
    Load all COVID-19 reports from the database into a Pandas DataFrame.
    
    Args:
        conn: SQLAlchemy database connection.
        
    Returns:
        pd.DataFrame: DataFrame containing the report data.
    """
    # Fetch all reports
    reports = get_reports_sql(conn)
    
    if not reports:
        return pd.DataFrame()
        
    # Convert to DataFrame
    df = pd.DataFrame(reports)
    
    # Ensure observation_date is datetime
    if "observation_date" in df.columns:
        df["observation_date"] = pd.to_datetime(df["observation_date"])
        
    return df
