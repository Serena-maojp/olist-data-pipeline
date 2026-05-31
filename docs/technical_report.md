# Technical Report: Olist E-Commerce Data Pipeline

> **Project:** Brazilian E-Commerce Analytics Pipeline
> **Dataset:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download)

---

## Table of Contents

1. [Data Ingestion](#1-data-ingestion)
2. [Data Warehouse Design](#2-data-warehouse-design) *(lizhou)*
3. [ELT Pipeline](#3-elt-pipeline) *(Balkis)*
4. [Data Quality Testing](#4-data-quality-testing) *(qiuxuan)*
5. [Data Analysis with Python](#5-data-analysis-with-python) *(Maegala)*
6. [Pipeline Orchestration](#6-pipeline-orchestration) *(Optional)*
7. [Architecture Overview](#7-architecture-overview)

---

## 1. Data Ingestion

**Owner:** Member 1
**Tool:** [Meltano](https://meltano.com/) v3.x
**Destination:** Google BigQuery (`olist_raw` dataset)

### 1.1 Objective

The goal of this stage is to extract raw CSV data from the Olist Kaggle dataset and load it into Google BigQuery without any transformation. This establishes a stable raw layer that all downstream pipeline stages can build upon.

### 1.2 Tool Selection: Meltano

Meltano was chosen over a custom Python script because it handles schema inference, batch uploading, and incremental state management out of the box — reducing boilerplate code and making the pipeline easier to maintain and reproduce across team members.

### 1.3 Plugin Configuration

Two Meltano plugins were used:

- **Extractor — `tap-spreadsheets-anywhere`:** Reads CSV files from local paths, automatically inferring schemas from column headers.
- **Loader — `target-bigquery`:** Writes extracted records into BigQuery tables, with each CSV mapping to one table in the `olist_raw` dataset.

### 1.4 Tables Loaded

All 8 tables were successfully loaded into `olist-assignment-497915.olist_raw`:

| Table | Description | Approx. Row Count |
|---|---|---|
| `orders` | Core order records with status and timestamps | ~99,000 |
| `customers` | Customer location and unique identifiers | ~99,000 |
| `order_items` | Line items per order (product, seller, price) | ~112,000 |
| `order_payments` | Payment method and value per order | ~103,000 |
| `order_reviews` | Customer review scores and comments | ~100,000 |
| `products` | Product metadata and category names (Portuguese) | ~33,000 |
| `sellers` | Seller location information | ~3,000 |
| `category_translation` | Portuguese → English category name mapping | ~71 |

**Total records loaded: ~550,785**

### 1.5 Raw Data Observations

Preliminary exploratory analysis (`notebooks/00_eda_raw_data.ipynb`) revealed the following, which downstream stages should account for:

- Timestamp columns are loaded as `STRING` type in BigQuery — these must be cast to `TIMESTAMP` in staging models.
- `order_reviews`: `review_comment_title` and `review_comment_message` contain a high proportion of NULLs (expected, as these are optional fields).
- `products`: approximately 1.6% of rows have a NULL `product_category_name`.
- `order_payments`: multiple rows per `order_id` are expected (one row per payment installment). Aggregation must be handled carefully to avoid fan-out in the fact table.
- `order_items`: the primary key is a composite of `order_id` + `order_item_id`, not `order_id` alone.
- Orders span from **September 2016 to October 2018**, with volume peaking in **late 2017 through mid-2018**.

### 1.6 Design Decision

Following the ELT pattern, raw data is loaded into BigQuery before any transformation. This preserves the original source data, allows transformations to be re-run without re-ingesting, and provides a clear audit trail for data lineage.

---

*Sections 2–7 to be completed by others*