# olist-data-pipeline

Module 2 Assignment - ELT Pipeline with Olist Dataset

## Overview

This project implements an end-to-end ELT pipeline using:

* Meltano (Data Ingestion)
* Google BigQuery (Data Warehouse)
* dbt (Transformations & Data Quality Testing)
* Python & Pandas (Analytics)
* Dagster (Pipeline Orchestration)

## Project Structure

```text
olist-data-pipeline/
│
├── meltano-olist/      # Data ingestion
├── dbt_olist/          # Data warehouse & transformations
├── notebooks/          # Analytics notebooks
├── dagster-olist/      # Pipeline orchestration
├── docs/               # Technical documentation
├── slides/             # Presentation materials
├── environment.yml
└── README.md
```

# Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd olist-data-pipeline
```

## 2. Create Environment

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate olist
```

# Phase 1: Data Ingestion (Meltano)

## 3. Download Dataset

Download the Olist dataset from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## 4. Place Raw Files

Place all Olist CSV files into:

```text
meltano-olist/data/
```

Required files:

```text
olist_customers_dataset.csv
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

## 5. Configure Environment Variables

Inside the `meltano-olist` folder, run the below to create a .env file: 

```bash
cp .env.example .env
```

Update the following values:

* GCP Project ID
* Local data folder path
* Service Account JSON path

## 6. Run Meltano Ingestion

Navigate to the Meltano directory:

```bash
cd meltano-olist
```

Install plugins:

```bash
meltano install
```

Run ingestion:

```bash
meltano run tap-spreadsheets-anywhere target-bigquery
```

Verify that raw tables are created in:

```text
olist_raw
```

within Google BigQuery.

# Phase 2: Data Warehouse & Transformations (dbt)

## 7. Save JSON file for service authorization from GCP for your project, into a local folder, and copy the path to JSON file 

## 8. Configure dbt Profile

Create or update:

```text
~/.dbt/profiles.yml
```

Example configuration:

```yaml
olist_data_pipeline:   # name of data set, must match what is on the dbt_project.yml file 
  outputs:
    dev:
      dataset: olist_dwh # name of output dataset inside GCP 
      job_execution_timeout_seconds: 300 # default 
      job_retries: 1 # default 
      keyfile: /../<Service Auth file name>.json #copy paste file path from step 4 
      location: US # default
      method: service-account 
      priority: interactive # default 
      project: <enter name of project from GCP> # change to name of dataset
      threads: 4 # default 
      type: bigquery 
  target: dev # default 
```

## 9. Verify dbt Project Configuration

Ensure the following values match between:

* `dbt_project.yml`
* `profiles.yml`

```yaml
# Name your project! Project names should contain only lowercase characters
# and underscores. A good package name should reflect your organization's
# name or the intended use of these models
name: 'olist_data_pipeline'
version: '1.0.0'

# This setting configures which "profile" dbt uses for this project.
profile: 'olist_data_pipeline'

# These configurations specify where dbt should look for different types of files.
# The `model-paths` config, for example, states that models in this project can be
# found in the "models/" directory. You probably won't need to change these!
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:         # directories to be removed by `dbt clean`
  - "target"
  - "dbt_packages"

# Configuring models
# Full documentation: https://docs.getdbt.com/docs/configuring-models

# In this example config, we tell dbt to build all models in the example/
# directory as views. These settings can be overridden in the individual model
# files using the `{{ config(...) }}` macro.
models:
  olist_data_pipeline:
    # Config indicated by + and applies to all files under models/example/
    tables:
      +materialized: table or view 
```

## 10. Run dbt Models

Navigate to:

```bash
cd dbt_olist
```

Run the following commands:

```bash
dbt debug
```

```bash
dbt parse
```

```bash
dbt run
```

```bash
dbt test
```

All commands should complete successfully.

Expected output models:

### Staging Models

```text
stg_customers
stg_orders
stg_order_items
stg_payments
stg_products
stg_reviews
stg_sellers
```

### Intermediate Models

```text
int_order_payments
int_customer_orders
```

### Mart Models

```text
dim_customers
dim_products
dim_sellers
dim_date
fact_orders
fct_customer_rfm
```

# Phase 4: Pipeline Orchestration (Dagster)

Navigate to:

```bash
cd dagster-olist
```

Start Dagster:

```bash
dagster dev
```

Open the Dagster UI:

- follow the link available within terminal or 

```text
http://localhost:3000
```

Execute the orchestration pipeline
- click on each component 
- click on "Materialize asset" 

OR 

- click on "Materialize all" 

```text
Meltano Ingestion
        ↓
dbt Run
        ↓
dbt Test
```
