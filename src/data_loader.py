"""Data loading and validation utilities for the Ethiopia FI forecast project."""

import pandas as pd
from pathlib import Path

# Compute the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def load_unified_data(file_path: str = None) -> pd.DataFrame:
    """
    Load the unified dataset (Excel format) and perform basic validation.
    Returns a DataFrame or raises an exception with a clear message.
    """
    if file_path is None:
        file_path = RAW_DIR / "ethiopia_fi_unified_data.xlsx"

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Unified data file not found at {file_path}. Please place it in data/raw/."
        ) from exc

    required_cols = ["record_type", "pillar", "indicator_code", "value_numeric", "observation_date"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    try:
        df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    except Exception as exc:
        raise ValueError("Could not parse 'observation_date' column.") from exc

    print(f"Loaded {len(df)} records from {file_path}")
    return df


def load_reference_codes(file_path: str = None) -> pd.DataFrame:
    """Load the reference codes dataset."""
    if file_path is None:
        file_path = RAW_DIR / "reference_codes.xlsx"
    try:
        ref = pd.read_excel(file_path)
        print(f"Loaded reference codes from {file_path}")
        return ref
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Reference codes file not found at {file_path}."
        ) from exc


def save_enriched_data(df: pd.DataFrame, file_path: str = None) -> None:
    """Save the enriched dataset to the processed folder."""
    if file_path is None:
        file_path = PROCESSED_DIR / "enriched_data.csv"
    df.to_csv(file_path, index=False)
    print(f"Enriched data saved to {file_path}")

def load_impact_links_from_excel(file_path: str = None) -> pd.DataFrame:
    """
    Load the impact_link records from the second sheet of the unified dataset.
    """
    if file_path is None:
        file_path = RAW_DIR / "ethiopia_fi_unified_data.xlsx"
    try:
        df = pd.read_excel(file_path, sheet_name=1)  # second sheet (0-indexed)
        print(f"Loaded {len(df)} impact_link records from sheet 2")
        return df
    except Exception as exc:
        print(f"Could not load impact_link sheet: {exc}")
        return pd.DataFrame()