from dagster import Definitions, define_asset_job, ScheduleDefinition

from dagster_olist.assets import (
    meltano_ingestion,
    dbt_dependencies,
    dbt_run,
    dbt_test,
)


olist_pipeline_job = define_asset_job(
    name="olist_pipeline_job",
    selection=[
        "meltano_ingestion",
        "dbt_dependencies",
        "dbt_run",
        "dbt_test",
    ],
)

daily_olist_schedule = ScheduleDefinition(
    job=olist_pipeline_job,
    cron_schedule="0 9 * * *",
)

defs = Definitions(
    assets=[
        meltano_ingestion,
        dbt_dependencies,
        dbt_run,
        dbt_test,
    ],
    jobs=[olist_pipeline_job],
    schedules=[daily_olist_schedule],
)