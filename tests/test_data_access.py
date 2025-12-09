"""
Tests for data access module - CSV loading functionality.
"""
import pytest
import pandas as pd
from pathlib import Path

from src.data_access import load_csv


class TestLoadCSV:
    """Tests for the load_csv function."""

    def test_load_csv_returns_dataframe(self, tmp_path):
        """Test that load_csv returns a pandas DataFrame."""
        # Arrange
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("col1,col2\n1,2\n3,4\n")

        # Act
        result = load_csv(str(csv_file))

        # Assert
        assert isinstance(result, pd.DataFrame)

    def test_load_csv_not_empty(self, tmp_path):
        """Test that load_csv returns a non-empty DataFrame for valid CSV."""
        # Arrange
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("col1,col2\n1,2\n3,4\n")

        # Act
        result = load_csv(str(csv_file))

        # Assert
        assert not result.empty
        assert len(result) == 2

    def test_load_csv_missing_file_raises_error(self):
        """Test that load_csv raises FileNotFoundError for missing file."""
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            load_csv("nonexistent_file.csv")

    def test_load_csv_has_correct_columns(self, tmp_path):
        """Test that load_csv preserves CSV column names."""
        # Arrange
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age,city\nAlice,30,London\n")

        # Act
        result = load_csv(str(csv_file))

        # Assert
        assert list(result.columns) == ["name", "age", "city"]

    def test_load_csv_covid_dataset_required_columns(self):
        """Test that the COVID dataset has all required columns."""
        # Arrange
        dataset_path = Path(__file__).parent.parent / "Dataset" / "covid_19_data.csv"
        required_columns = [
            "SNo",
            "ObservationDate",
            "Province/State",
            "Country/Region",
            "Last Update",
            "Confirmed",
            "Deaths",
            "Recovered",
        ]

        # Skip if dataset doesn't exist (CI environment)
        if not dataset_path.exists():
            pytest.skip("COVID dataset not available")

        # Act
        result = load_csv(str(dataset_path))

        # Assert
        for col in required_columns:
            assert col in result.columns, f"Missing required column: {col}"

    def test_load_csv_covid_dataset_not_empty(self):
        """Test that the COVID dataset loads with data."""
        # Arrange
        dataset_path = Path(__file__).parent.parent / "Dataset" / "covid_19_data.csv"

        # Skip if dataset doesn't exist (CI environment)
        if not dataset_path.exists():
            pytest.skip("COVID dataset not available")

        # Act
        result = load_csv(str(dataset_path))

        # Assert
        assert not result.empty
        assert len(result) > 0
