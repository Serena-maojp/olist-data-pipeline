from pathlib import Path
import subprocess
from dagster import asset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MELTANO_DIR = PROJECT_ROOT / "meltano-olist"
DBT_DIR = PROJECT_ROOT / "dbt_olist"


@asset
def meltano_ingestion():
    subprocess.run(
        ["meltano", "run", "tap-spreadsheets-anywhere", "target-bigquery"],
        cwd=MELTANO_DIR,
        check=True,
    )


@asset(deps=[meltano_ingestion])
def dbt_run():
    subprocess.run(
        ["dbt", "run"],
        cwd=DBT_DIR,
        check=True,
    )


@asset(deps=[dbt_run])
def dbt_test():
    subprocess.run(
        ["dbt", "test"],
        cwd=DBT_DIR,
        check=True,
    )