import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import (
    FILTERED_DATA_PATH,
    MUNICIPAL_DATA_PATH,
)


def load_data(file_path):
    """Load the filtered accident dataset."""
    return pd.read_csv(file_path)

def create_connection():
    """Create a DuckDB connection."""
    conn = duckdb.connect()
    return conn

def register_table(conn, table_name, df):
    """Register a DataFrame as a DuckDB table."""
    conn.register(table_name, df)


def print_summary(df, dataset_name="Dataset", max_cols=None):
    print(f"\n✅ {dataset_name}: {len(df):,} records")
    print("-" * 40)

    # Print all columns if max_cols is None
    if max_cols is None:
        max_cols = len(df.columns)

    print(f"✅ Showing {max_cols} of {len(df.columns)} columns:")

    for i, col in enumerate(df.columns[:max_cols], start=1):
        print(f"{i:2}. {col}")
    if len(df.columns) > max_cols:
        print(f"... {len(df.columns) - max_cols} additional columns")