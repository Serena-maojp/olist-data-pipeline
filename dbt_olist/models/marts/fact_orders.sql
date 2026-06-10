-- models/marts/fact_orders.sql

{{ config(materialized='table') }}

WITH staging_order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

staging_orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

staging_reviews AS (
    SELECT * FROM {{ ref('stg_order_reviews') }}
)

SELECT
    -- Primary Key
    i.order_item_id AS order_item_sk,    
    
    -- Foreign Keys connecting to your Dimensions
    i.order_id AS order_key,             
    i.product_id AS product_key,         
    i.seller_id AS seller_key,           
    o.customer_id AS customer_key,       
    
    -- Convert order timestamp into a clean YYYYMMDD date key for dim_date
    CAST(FORMAT_DATE('%Y%m%d', DATE(o.order_purchase_timestamp)) AS STRING) AS date_key,
    
    -- Measurable Facts
    i.price,
    i.freight_value,
    r.review_score

FROM staging_order_items i
LEFT JOIN staging_orders o 
    ON i.order_id = o.order_id
LEFT JOIN staging_reviews r 
    ON i.order_id = r.order_id