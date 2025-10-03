import json
import logging
import os
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configure logging to ensure Prefect capture
sys.path.append(str(Path(__file__).parent.parent))
from logging_config import configure_logging, get_logger

# Configure logging
configure_logging(level=logging.INFO, script_name="PostgresCopy")
logger = get_logger(__name__)

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
DUCKDB_TABLES = {
    "target.job_dashboard_base": "job_dashboard_base",
    "target.job_skills": "job_skills",
}

POSTGRES_URI = os.getenv("DATABASE_URL")
POSTGRES_SCHEMA = "target"  # Change if needed

duckdb_db_name = os.getenv("MOTHERDUCK_DATABASE")
duckdb_token = os.getenv("MOTHERDUCK_TOKEN")
if not duckdb_db_name or not duckdb_token:
    raise ValueError(
        "MOTHERDUCK_DATABASE and MOTHERDUCK_TOKEN environment variables are required"
    )


def copy_table(con, table_name, postgres_table):
    try:
        logger.info(f"Reading data from DuckDB table {table_name}...")
        df = con.execute(f"SELECT * FROM {table_name}").fetchdf()
        logger.info(f"Extracted {len(df)} rows from DuckDB table {table_name}")

        # Convert numpy arrays to JSON strings for PostgreSQL compatibility
        if "extracted_skills" in df.columns:
            logger.info("Converting extracted_skills arrays to JSON format...")
            df["extracted_skills"] = df["extracted_skills"].apply(
                lambda x: (
                    json.dumps(x.tolist())
                    if isinstance(x, np.ndarray)
                    else json.dumps(x) if pd.notna(x) else None
                )
            )
            logger.info("Successfully converted extracted_skills to JSON format.")

        if "apply_options" in df.columns:
            logger.info("Converting apply_options arrays to JSON format...")
            df["apply_options"] = df["apply_options"].apply(
                lambda x: (
                    json.dumps(x.tolist())
                    if isinstance(x, np.ndarray)
                    else json.dumps(x) if pd.notna(x) else None
                )
            )
            logger.info("Successfully converted apply_options to JSON format.")

        # Load to Postgres
        logger.info(
            f"Writing data to Postgres table {POSTGRES_SCHEMA}.{postgres_table} (overwrite mode)..."
        )
        engine = create_engine(POSTGRES_URI)
        df.to_sql(
            postgres_table,
            engine,
            if_exists="replace",
            index=False,
            schema=POSTGRES_SCHEMA,
        )
        logger.info(
            f"Successfully loaded data to Postgres table {POSTGRES_SCHEMA}.{postgres_table}"
        )

    except Exception as e:
        logger.error(f"Error processing table {table_name}: {str(e)}")
        raise


def main():
    try:
        # Connect to MotherDuck
        logger.info("Connecting to MotherDuck...")
        con = duckdb.connect(f"md:{duckdb_db_name}")

        # Process each table
        for duckdb_table, postgres_table in DUCKDB_TABLES.items():
            copy_table(con, duckdb_table, postgres_table)

        logger.info("All tables processed successfully!")

    except duckdb.Error as e:
        logger.error(f"DuckDB error: {e}")
    except SQLAlchemyError as e:
        logger.error(f"Postgres (SQLAlchemy) error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    main()
