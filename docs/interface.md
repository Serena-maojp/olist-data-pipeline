# from jinping suggestion
_jinping suggest the table names, if need to change can discuss in the discord group

## BigQuery Configuration
- Project ID: olist-assignment-497915
- Raw Dataset: olist_raw
- DWH Dataset: olist_dwh

## Raw Table Names (jinping will deliver)
| Table                        | Source CSV                                      |
|------------------------------|-------------------------------------------------|
| olist_raw.orders             | olist_orders_dataset.csv                        |
| olist_raw.customers          | olist_customers_dataset.csv                     |
| olist_raw.products           | olist_products_dataset.csv                      |
| olist_raw.order_items        | olist_order_items_dataset.csv                   |
| olist_raw.order_payments     | olist_order_payments_dataset.csv                |
| olist_raw.order_reviews      | olist_order_reviews_dataset.csv                 |
| olist_raw.sellers            | olist_sellers_dataset.csv                       |
| olist_raw.category_translation | product_category_name_translation.csv         |

## Staging Table Names (lizhou or Balkis will deliver)
| Table                    | Source                    |
|--------------------------|---------------------------|
| olist_dwh.stg_orders     | olist_raw.orders          |
| olist_dwh.stg_customers  | olist_raw.customers       |
| olist_dwh.stg_products   | olist_raw.products        |
| olist_dwh.stg_order_items | olist_raw.order_items    |
| olist_dwh.stg_order_payments | olist_raw.order_payments |
| olist_dwh.stg_order_reviews  | olist_raw.order_reviews  |
| olist_dwh.stg_sellers    | olist_raw.sellers         |

## Marts Table Names (Balkis will deliver)
| Table                  | Type            |
|------------------------|-----------------|
| olist_dwh.fact_orders  | Fact table      |
| olist_dwh.dim_customers | Dimension table |
| olist_dwh.dim_products  | Dimension table |
| olist_dwh.dim_sellers   | Dimension table |
| olist_dwh.dim_date      | Dimension table |
