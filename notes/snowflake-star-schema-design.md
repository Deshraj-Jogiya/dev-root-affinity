# Snowflake Star Schema Design

This note reviews the relational database schema design I implemented for a multi-branch sales data warehouse. We organize database tables into a classic Star Schema (complying with Ralph Kimball's dimensional modeling principles) to optimize query performance in Snowflake.

## The Design: Fact & Dimension Tables
- **Fact Table:** Stores quantitative measurements (prices, quantities sold, revenue) and foreign keys pointing to dimension tables.
- **Dimension Tables:** Stores descriptive attributes (product details, branch locations, dates) used to filter and group queries.

```sql
-- 1. Create Dimensions
CREATE OR REPLACE TABLE dim_products (
    product_id INT PRIMARY KEY,
    sku VARCHAR(50),
    product_name VARCHAR(150),
    category VARCHAR(100),
    unit_price DECIMAL(10, 2)
);

CREATE OR REPLACE TABLE dim_branches (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50)
);

CREATE OR REPLACE TABLE dim_calendar (
    date_key INT PRIMARY KEY, -- format YYYYMMDD
    full_date DATE,
    day_of_week VARCHAR(15),
    month VARCHAR(15),
    quarter INT,
    year INT
);

-- 2. Create Fact Table
CREATE OR REPLACE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_key INT FOREIGN KEY REFERENCES dim_calendar(date_key),
    product_id INT FOREIGN KEY REFERENCES dim_products(product_id),
    branch_id INT FOREIGN KEY REFERENCES dim_branches(branch_id),
    quantity_sold INT,
    gross_revenue DECIMAL(12, 2)
);
```

## Analytical Query Example
Snowflake's columnar architecture performs joins between small dimension tables and large fact tables very efficiently. Here is a query summarizing revenue by product category and year:

```sql
SELECT 
    p.category,
    c.year,
    SUM(f.quantity_sold) AS total_items_sold,
    SUM(f.gross_revenue) AS total_revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
JOIN dim_calendar c ON f.date_key = c.date_key
GROUP BY p.category, c.year
ORDER BY total_revenue DESC;
```

## Snowflake Key Performance Rules
1. **Micro-partitions:** Snowflake automatically clusters data based on data loading sequences. To maintain order, avoid updates and favor bulk loading.
2. **Columnar storage:** Queries should select *only* the columns needed rather than using `SELECT *`, reducing scan costs significantly.
