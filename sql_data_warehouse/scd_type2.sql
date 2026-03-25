-- SCD Type 2 Example

INSERT INTO dim_customer_hist (
    customer_id, name, start_date, end_date, is_active
)
SELECT 
    s.customer_id,
    s.name,
    CURRENT_DATE,
    NULL,
    'Y'
FROM staging_customer s
LEFT JOIN dim_customer_hist d
ON s.customer_id = d.customer_id
AND d.is_active = 'Y'
WHERE s.name <> d.name;
