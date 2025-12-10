import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add the project root to sys.path to allow imports from src
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from src.db.engine import get_engine
from src.dashboard_utils import load_data_from_db
from src.analysis import (
    filter_data,
    get_summary_stats,
    get_trend_over_time,
    get_top_countries
)

# Constants
DB_PATH = root_path / "covid_data.db"

@st.cache_data
def get_data():
    """
    Load data from the database. Cached to improve performance.
    """
    if not DB_PATH.exists():
        st.error(f"Database file not found at {DB_PATH}. Please run init_db.py first.")
        return pd.DataFrame()
        
    # Pass the path string to get_engine, which handles the sqlite:/// prefix
    engine = get_engine(str(DB_PATH))
    with engine.connect() as conn:
        df = load_data_from_db(conn)
    return df

def main():
    st.set_page_config(page_title="Public Health Dashboard", layout="wide")
    
    st.title("Public Health Dashboard")
    
    # Load data
    df = get_data()
    
    if df.empty:
        st.warning("No data available. Please check the database.")
        return

    # Calculate dataset stats
    min_date = df["observation_date"].min().date()
    max_date = df["observation_date"].max().date()
    n_countries = df["country_region"].nunique()

    st.markdown(f"""
    Welcome to the **COVID-19 Data Insights Dashboard**. 
    This tool visualizes the spread of the virus using data aggregated from various sources (including WHO and Johns Hopkins University).

    ### Dataset Overview
    - **Time Range:** {min_date} to {max_date}
    - **Geographic Coverage:** {n_countries} Countries/Regions
    - **Total Records:** {len(df):,}
    
    Use the **sidebar filters** on the left to narrow down the analysis by date or country.
    """)

    # Sidebar Filters
    st.sidebar.header("Filters")
    
    # Date Range Filter
    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
    
    # Country Filter
    countries = sorted(df["country_region"].unique())
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + countries)
    
    # Apply Filters
    filtered_df = filter_data(
        df, 
        country=selected_country if selected_country != "All" else None,
        start_date=pd.to_datetime(start_date),
        end_date=pd.to_datetime(end_date)
    )
    
    # Display Summary Stats
    st.header("Summary Statistics")
    stats = get_summary_stats(filtered_df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Confirmed", f"{stats['total_confirmed']:,}")
    col2.metric("Total Deaths", f"{stats['total_deaths']:,}")
    col3.metric("Total Recovered", f"{stats['total_recovered']:,}")
    
    # Display Trends
    st.header("Trends Over Time")
    trend_df = get_trend_over_time(filtered_df)
    st.line_chart(trend_df.set_index("observation_date")[["confirmed", "deaths", "recovered"]])
    
    # Display Top Countries (only if no specific country is selected)
    if selected_country == "All":
        st.header("Top 10 Countries by Confirmed Cases")
        top_countries = get_top_countries(filtered_df, n=10)
        st.bar_chart(top_countries.set_index("country_region")["confirmed"])
    
    # Show Raw Data
    if st.checkbox("Show Raw Data"):
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
