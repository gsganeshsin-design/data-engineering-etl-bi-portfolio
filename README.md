# Ganesh Sivakumar - Data Engineering Portfolio

This repository showcases practical work samples aligned to ETL / ELT, SQL, Python, BI reporting, and data quality engineering.

## Projects

### 1. Python ETL Reconciliation
A Python-based ETL reconciliation utility that:
- reads source and target CSV extracts
- validates schema and required fields
- performs control-total reconciliation
- identifies mismatches and duplicate records
- writes exception reports and a summary report

**Skills shown:** Python, data validation, reconciliation, audit readiness, ETL controls.

### 2. SQL Data Warehouse Models
A set of SQL scripts that demonstrate:
- staging to dimension/fact loading
- SCD Type 2 customer dimension handling
- sales fact loading
- basic reconciliation queries

**Skills shown:** SQL, DWH, Star Schema, SCD2, ETL/ELT design.

### 3. BI Reporting Documentation
Business-facing documentation for KPI reporting and dashboard delivery.

**Skills shown:** requirements translation, KPI definition, reporting governance, stakeholder communication.

## Repository Structure

- `python_etl_reconciliation/` - Python ETL validation and reconciliation sample
- `sql_data_warehouse/` - SQL DWH scripts and sample schema
- `bi_reporting_docs/` - KPI and reporting documentation samples
- `sample_data/` - example CSV files for ETL reconciliation

## How to Run the Python Project

```bash
cd python_etl_reconciliation
python etl_reconciliation.py
```

Outputs will be created in the `output/` folder.

## Notes

This portfolio uses sample data and generic business scenarios so it can be shared publicly.
