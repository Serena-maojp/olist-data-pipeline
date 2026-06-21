import os
import subprocess
from pathlib import Path

from dagster import asset, AssetExecutionContext


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MELTANO_DIR = PROJECT_ROOT / "meltano-olist"
DBT_DIR = PROJECT_ROOT / "dbt_olist"


def run_command(command: list[str], cwd: Path, context: AssetExecutionContext):
    context.log.info(f"Running command: {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )

    if result.stdout:
        context.log.info(result.stdout)

    if result.stderr:
        context.log.warning(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(command)}")


@asset
def meltano_ingestion(context: AssetExecutionContext):
    """Extract and load raw Olist CSV files into BigQuery using Meltano."""
    run_command(["meltano", "run", "tap-spreadsheets-anywhere", "target-bigquery"], MELTANO_DIR, context)


@asset(deps=[meltano_ingestion])
def dbt_dependencies(context: AssetExecutionContext):
    """Install dbt package dependencies."""
    run_command(["dbt", "deps"], DBT_DIR, context)


@asset(deps=[dbt_dependencies])
def dbt_run(context: AssetExecutionContext):
    """Build dbt staging and mart models in BigQuery."""
    run_command(["dbt", "run"], DBT_DIR, context)


@asset(deps=[dbt_run])
def dbt_test(context: AssetExecutionContext):
    """Run dbt data quality tests."""
    run_command(["dbt", "test"], DBT_DIR, context)