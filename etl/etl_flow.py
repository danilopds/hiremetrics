"""
NOTE:
when switching between local, remote or docker postgres:
    you need to change the POSTGRES_URI in the copy_job_dashboard_base.py file
    and run dbt clean and dbt deps to refresh the dependencies

docker commands for reference:
docker exec -w /app/dbt saas_hiremetrics_etl dbt clean
docker exec -w /app/dbt saas_hiremetrics_etl dbt deps
docker exec saas_hiremetrics_etl dbt run --project-dir dbt --profiles-dir dbt
docker exec saas_hiremetrics_etl python scripts/copy_job_dashboard_base.py
docker exec saas_hiremetrics_etl python etl_flow.py
"""

import logging
import shutil
import subprocess
import sys
from pathlib import Path

# Configure logging
from logging_config import configure_logging, get_logger
from prefect import flow, task

configure_logging(level=logging.INFO, script_name="ETL")
logger = get_logger(__name__)

# Suppress verbose Prefect and HTTP logging
logging.getLogger("prefect.client").setLevel(logging.WARNING)
logging.getLogger("prefect.utilities").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("prefect.engine").setLevel(logging.WARNING)

# Configuration variables
BASE_DIR = Path(__file__).parent.resolve()
PYTHON_EXEC = sys.executable
DBT_EXEC = shutil.which("dbt")


def run_subprocess_with_logging(cmd, cwd, task_name):
    """Run subprocess with enhanced logging capture"""
    logger.info(f"🚀 Starting {task_name}...")
    logger.info(f"📁 Working directory: {cwd}")
    logger.info(f"🔧 Command: {' '.join(cmd)}")

    # Run subprocess without capturing output to avoid double logging
    # The subprocess scripts already use logging, so we don't need to capture and re-log
    result = subprocess.run(
        cmd,
        cwd=cwd,
        # Remove capture_output=True to let subprocess output go directly to console
        # capture_output=True,
        text=True,
        # encoding='utf-8'
    )

    # Only log errors if the subprocess failed
    if result.returncode != 0:
        error_msg = f"❌ {task_name} failed with return code {result.returncode}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info(f"✅ {task_name} completed successfully")
    return result


@task(retries=2, retry_delay_seconds=5)
def run_dbt_full_refresh():
    if not DBT_EXEC:
        error_msg = "dbt executable not found in PATH or venv."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    cmd = [
        DBT_EXEC,
        "run",
        "--full-refresh",
        "--project-dir",
        "dbt",
        "--profiles-dir",
        "dbt",
    ]
    run_subprocess_with_logging(cmd, str(BASE_DIR), "DBT Data Transformation")


@task(retries=2, retry_delay_seconds=5)
def run_dbt():
    if not DBT_EXEC:
        error_msg = "dbt executable not found in PATH or venv."
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    cmd = [DBT_EXEC, "run", "--project-dir", "dbt", "--profiles-dir", "dbt"]
    run_subprocess_with_logging(cmd, str(BASE_DIR), "DBT Data Transformation")


@task(retries=2, retry_delay_seconds=10)
def load_to_postgres():
    cmd = [PYTHON_EXEC, str(BASE_DIR / "scripts" / "copy_job_dashboard_base.py")]
    run_subprocess_with_logging(cmd, str(BASE_DIR), "Load to PostgreSQL")


@flow(name="ETL Pipeline Orchestration")
def etl_pipeline():
    logger.info("🔄 Starting ETL Pipeline Orchestration")

    # regular ETL flow
    run_dbt()
    load_to_postgres()

    # full refresh ETL flow
    # run_dbt_full_refresh()
    # load_to_postgres()

    logger.info("🎯 ETL Pipeline Orchestration completed")


if __name__ == "__main__":
    etl_pipeline()
