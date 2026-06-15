from dagster import Definitions
from .assets import (
    meltano_ingestion,
    dbt_run,
    dbt_test
)

defs = Definitions(
    assets=[
        meltano_ingestion,
        dbt_run,
        dbt_test
    ]
)