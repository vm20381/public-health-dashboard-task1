import pandas as pd
import pytest

from src.cleaning import (
    standardise_columns,
    validate_schema,
    convert_types,
    handle_missing,
    to_records,
    clean_covid_df,
)

RAW_COLUMNS = [
    "SNo",
    "ObservationDate",
    "Province/State",
    "Country/Region",
    "Last Update",
    "Confirmed",
    "Deaths",
    "Recovered",
]

def _sample_raw_df():
    return pd.DataFrame(
        {
            "SNo": [1, 2],
            "ObservationDate": ["01/22/2020", "01/23/2020"],
            "Province/State": ["Anhui", None],
            "Country/Region": ["Mainland China", "US"],
            "Last Update": ["1/22/2020 17:00", "1/23/20 17:00"],  # mixed year formats
            "Confirmed": [1.0, 14.0],
            "Deaths": [0.0, 1.0],
            "Recovered": [0.0, 2.0],
        }
    )

def test_validate_schema_passes_with_required_columns():
    df = _sample_raw_df()
    validate_schema(df)  # should not raise

def test_validate_schema_raises_when_missing_required_column():
    df = _sample_raw_df().drop(columns=["Recovered"])
    with pytest.raises(ValueError):
        validate_schema(df)

def test_standardise_columns_renames_to_snake_case():
    df = _sample_raw_df()
    out = standardise_columns(df)
    assert set(out.columns) == {
        "sno",
        "observation_date",
        "province_state",
        "country_region",
        "last_update",
        "confirmed",
        "deaths",
        "recovered",
    }

def test_convert_types_parses_dates_and_mixed_last_update_format():
    df = standardise_columns(_sample_raw_df())
    out = convert_types(df)

    assert pd.api.types.is_datetime64_any_dtype(out["observation_date"])
    assert pd.api.types.is_datetime64_any_dtype(out["last_update"])

    # Ensure last_update parsed for both formats (not NaT)
    assert out["last_update"].isna().sum() == 0

def test_convert_types_converts_counts_to_nullable_int():
    df = standardise_columns(_sample_raw_df())
    out = convert_types(df)

    expected_values = {"confirmed": 1, "deaths": 0, "recovered": 0}
    for col in ["confirmed", "deaths", "recovered"]:
        assert str(out[col].dtype) == "Int64"
        assert out[col].iloc[0] == expected_values[col]

def test_handle_missing_leaves_province_state_as_none():
    df = standardise_columns(_sample_raw_df())
    df = convert_types(df)
    out = handle_missing(df)

    # Should remain NaN/None
    assert pd.isna(out["province_state"].iloc[1])

def test_to_records_converts_na_to_none():
    df = clean_covid_df(_sample_raw_df())
    # Introduce a pd.NA in an Int64 column
    df.loc[0, "confirmed"] = pd.NA
    records = to_records(df)

    assert records[0]["confirmed"] is None
    assert records[1]["province_state"] is None # Was None in sample

def test_to_records_returns_list_of_dicts_with_expected_keys():
    df = clean_covid_df(_sample_raw_df())
    records = to_records(df)

    assert isinstance(records, list)
    assert isinstance(records[0], dict)
    assert set(records[0].keys()) == {
        "sno",
        "observation_date",
        "province_state",
        "country_region",
        "last_update",
        "confirmed",
        "deaths",
        "recovered",
    }

def test_clean_covid_df_end_to_end_schema_and_types():
    df = clean_covid_df(_sample_raw_df())

    assert "country_region" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["observation_date"])
    assert str(df["confirmed"].dtype) == "Int64"
