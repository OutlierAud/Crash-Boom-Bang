import duckdb
import pandas as pd
from config import FILTERED_DATA_PATH


def load_data():

    """Load the filtered accident dataset."""

    return pd.read_csv(FILTERED_DATA_PATH)

def create_connection(df):

    """Create a DuckDB connection and register the DataFrame."""

    conn = duckdb.connect()

    conn.register("accidents", df)

    return conn

def print_summary(df):

    """Print a summary of the loaded dataset."""

    print(f"✅ Loaded {len(df):,} records.")

    print("✅ Columns:")

    for i, col in enumerate(df.columns, start=1):

        print(f"{i:2}. {col}")