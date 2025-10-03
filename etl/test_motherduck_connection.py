import os

import duckdb

duckdb_db_name = os.getenv("MOTHERDUCK_DATABASE")
duckdb_token = os.getenv("MOTHERDUCK_TOKEN")
if not duckdb_db_name or not duckdb_token:
    raise ValueError(
        "MOTHERDUCK_DATABASE and MOTHERDUCK_TOKEN environment variables are required"
    )


def test_motherduck_connection():
    try:
        print(f"DuckDB version: {duckdb.__version__}")
        print("Attempting to connect to MotherDuck...")

        # Connect to MotherDuck
        con = duckdb.connect(f"md:{duckdb_db_name}")
        print("✅ Successfully connected to MotherDuck!")

        # Test a simple query
        result = con.execute("SELECT version()").fetchone()
        print(f"Database version: {result[0]}")

        # Close connection
        con.close()
        print("Connection closed successfully")

    except Exception as e:
        print(f"❌ Error connecting to MotherDuck: {e}")
        print(f"Error type: {type(e).__name__}")


if __name__ == "__main__":
    test_motherduck_connection()
