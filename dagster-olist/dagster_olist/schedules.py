from dagster import ScheduleDefinition
from dagster import define_asset_job

daily_pipeline = define_asset_job(
    "daily_pipeline"
)

daily_schedule = ScheduleDefinition(
    job=daily_pipeline,
    cron_schedule="0 9 * * *"
)