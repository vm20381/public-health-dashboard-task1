"""
Cleaning module - standardises, validates, and converts raw COVID-19 CSV data.
"""

from __future__ import annotations

from typing import Any
import pandas as pd

REQUIRED_RAW_COLUMNS = [
    "SNo",
    "ObservationDate",
    "Province/State",
    "Country/Region",
    "Last Update",
    "Confirmed",
    "Deaths",
    "Recovered",
]

RENAME_MAP = {
    "SNo": "sno",
    "ObservationDate": "observation_date",
    "Province/State": "province_state",
    "Country/Region": "country_region",
    "Last Update": "last_update",
    "Confirmed": "confirmed",
    "Deaths": "deaths",
    "Recovered": "recovered",
}

def validate_schema(df: pd.DataFrame) -> None:
    """Raise ValueError if required columns are missing."""
    missing = [c for c in REQUIRED_RAW_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename dataset columns to a consistent internal schema."""
    validate_schema(df)
    out = df.copy()
    out = out.rename(columns=RENAME_MAP)
    return out

def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert:
    - observation_date, last_update -> datetime
    - confirmed/deaths/recovered -> nullable Int64
    """
    out = df.copy()

    # Dates: handle mixed formats (01/22/2020) and (1/23/20 17:00)
    # format='mixed' allows pandas to infer different formats row-by-row
    out["observation_date"] = pd.to_datetime(out["observation_date"], errors="coerce", format="mixed")
    out["last_update"] = pd.to_datetime(out["last_update"], errors="coerce", format="mixed")

    # Counts: numeric -> nullable integer
    for col in ["confirmed", "deaths", "recovered"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").round(0).astype("Int64")

    # SNo: keep as int if possible
    out["sno"] = pd.to_numeric(out["sno"], errors="coerce").astype("Int64")

    return out

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values:
    - province_state: leave as None/NaN (will be NULL in DB)
    """
    out = df.copy()
    # Spec allows None or empty string. We choose None (NaN in pandas)
    # so we don't need to do anything here if we want NULLs.
    return out

def clean_covid_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    """End-to-end cleaning pipeline for the COVID dataset."""
    df = standardise_columns(raw_df)
    df = convert_types(df)
    df = handle_missing(df)
    return df

def to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Convert cleaned DataFrame to list[dict] (useful for bulk insert into DB).
    Keeps datetime values as pandas/py datetime objects (SQLAlchemy handles these).
    Converts pd.NA and NaN to None.
    """
    out = df.copy()
    # Convert to object and replace all pandas-specific missing values with None
    out = out.astype(object).where(pd.notnull(out), None)
    return out.to_dict(orient="records")
