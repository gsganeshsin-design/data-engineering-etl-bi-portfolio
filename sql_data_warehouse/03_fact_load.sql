-- Sample sales fact load
INSERT INTO fact_sales (sale_id, customer_sk, sale_date, amount, source_system)
SELECT s.sale_id,
       d.customer_sk,
       s.sale_date,
       s.amount,
       'CRM'
FROM stg_sales s
JOIN dim_customer d
  ON s.customer_id = d.customer_id
 AND d.is_current = 'Y';
