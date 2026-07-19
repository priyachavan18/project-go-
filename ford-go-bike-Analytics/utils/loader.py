from pathlib import Path

import pandas as pd
import streamlit as st

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "bike_data.parquet"


# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

@st.cache_data(show_spinner="Loading Ford GoBike dataset...")
def load_data():

    st.write("Project Root:", PROJECT_ROOT)
    st.write("Data File:", DATA_FILE)
    st.write("Exists:", DATA_FILE.exists())

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found:\n{DATA_FILE}")

    return pd.read_parquet(DATA_FILE)


# -------------------------------------------------------
# Validate Dataset
# -------------------------------------------------------

def validate_dataset(df: pd.DataFrame) -> None:

    required_columns = [
        "start_time",
        "end_time",
        "duration_sec",
        "trip_minutes",
        "hour",
        "weekday",
        "month_name",
        "season",
        "user_type",
        "member_gender",
        "age",
        "start_station_name",
        "end_station_name",
        "start_station_latitude",
        "start_station_longitude",
        "end_station_latitude",
        "end_station_longitude",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns:\n{missing}"
        )


# -------------------------------------------------------
# Dataset Summary
# -------------------------------------------------------

def dataset_summary(df: pd.DataFrame) -> dict:

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / 1024**2,
            2,
        ),
    }