-- ============================================================================
-- Snowflake Kimball Star Schema Setup for Sales Analytics
-- Chronicle: B.Tech Graduation / ASU Master's Database Engineering Projects
-- ============================================================================

-- Create Warehouse & Database
CREATE WAREHOUSE OR REPLACE sales_analytics_wh 
    WITH WAREHOUSE_SIZE = 'XSMALL' 
    AUTO_SUSPEND = 300 
    AUTO_RESUME = TRUE;

CREATE DATABASE IF NOT EXISTS sales_dw;
USE DATABASE sales_dw;
CREATE SCHEMA IF NOT EXISTS core;
USE SCHEMA core;

-- 1. Create Dimension Tables

-- Customer Dimension
CREATE OR REPLACE TABLE dim_customers (
    customer_key INT AUTOINCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    country VARCHAR(100),
    signup_date DATE
);

-- Product Dimension
CREATE OR REPLACE TABLE dim_products (
    product_key INT AUTOINCREMENT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(150),
    category VARCHAR(100),
    unit_price DECIMAL(10, 2)
);

-- Date Dimension
CREATE OR REPLACE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    is_weekend BOOLEAN
);

-- 2. Create Fact Table
CREATE OR REPLACE TABLE fact_sales (
    sales_key INT AUTOINCREMENT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    customer_key INT REFERENCES dim_customers(customer_key),
    product_key INT REFERENCES dim_products(product_key),
    date_key INT REFERENCES dim_date(date_key),
    quantity INT,
    total_revenue DECIMAL(15, 2)
);

-- 3. Staging and Data Loading (using COPY INTO)
CREATE OR REPLACE STAGE sales_csv_stage
    FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1);

-- Note: The following COPY commands are illustrative of bulk loading pipeline runs
-- COPY INTO dim_customers (customer_id, first_name, last_name, email, country, signup_date)
-- FROM @sales_csv_stage/customers.csv;

-- 4. Analytical Sales Query
-- Finds top 5 revenue-generating product categories in Q4 2024
SELECT 
    p.category,
    SUM(f.quantity) as total_units_sold,
    SUM(f.total_revenue) as total_category_revenue
FROM fact_sales f
JOIN dim_products p ON f.product_key = p.product_key
JOIN dim_date d ON f.date_key = d.date_key
WHERE d.year = 2024 AND d.quarter = 4
GROUP BY p.category
ORDER BY total_category_revenue DESC
LIMIT 5;
