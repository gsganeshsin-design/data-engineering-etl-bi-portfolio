-- Row count reconciliation
SELECT 'stg_sales' AS layer_name, COUNT(*) AS row_count FROM stg_sales
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales;

-- Control total reconciliation
SELECT 'stg_sales' AS layer_name, SUM(amount) AS total_amount FROM stg_sales
UNION ALL
SELECT 'fact_sales', SUM(amount) FROM fact_sales;
