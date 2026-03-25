-- Sample SCD Type 2 logic for dim_customer
UPDATE dim_customer
SET effective_to = CURRENT_DATE - INTERVAL '1 day',
    is_current = 'N'
WHERE customer_id IN (
    SELECT s.customer_id
    FROM stg_customer s
    JOIN dim_customer d
      ON s.customer_id = d.customer_id
     AND d.is_current = 'Y'
    WHERE COALESCE(s.segment, '') <> COALESCE(d.segment, '')
)
AND is_current = 'Y';

INSERT INTO dim_customer (
    customer_sk, customer_id, customer_name, segment, effective_from, effective_to, is_current
)
SELECT nextval('seq_customer_sk'),
       s.customer_id,
       s.customer_name,
       s.segment,
       CURRENT_DATE,
       DATE '9999-12-31',
       'Y'
FROM stg_customer s
LEFT JOIN dim_customer d
  ON s.customer_id = d.customer_id
 AND d.is_current = 'Y'
WHERE d.customer_id IS NULL
   OR COALESCE(s.segment, '') <> COALESCE(d.segment, '');
