"""
Data access module - handles loading and exporting data.
"""
import pandas as pd
from pathlib import Path


def load_csv(path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        path: Path to the CSV file.

    Returns:
        pd.DataFrame: The loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return pd.read_csv(path)
