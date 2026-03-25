-- Sample star schema objects
CREATE TABLE dim_customer (
    customer_sk      INTEGER PRIMARY KEY,
    customer_id      VARCHAR(20) NOT NULL,
    customer_name    VARCHAR(100),
    segment          VARCHAR(50),
    effective_from   DATE,
    effective_to     DATE,
    is_current       CHAR(1)
);

CREATE TABLE fact_sales (
    sale_id          INTEGER PRIMARY KEY,
    customer_sk      INTEGER,
    sale_date        DATE,
    amount           DECIMAL(18,2),
    source_system    VARCHAR(30)
);
