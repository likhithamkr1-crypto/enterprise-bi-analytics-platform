# 🚀 Omnichannel Business Intelligence & Automated Operations Data Hub

> A centralized enterprise analytics platform integrating Marketing, Operations, SaaS Retention, and Financial Risk telemetry into a unified relational data warehouse with an interactive web interface.

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Relational%20Warehouse-orange.svg)](https://duckdb.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Interactive%20App-red.svg)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-ETL%20Pipeline-brightgreen.svg)](https://pandas.pydata.org/)

---

## 📊 Executive Summary & Business Objective
Modern businesses silo their data across disparate systems—marketing tracks customer spend, operations tracks hospital throughput, product tracks SaaS churn, and finance tracks payment fraud. 
* **The Goal:** Build a centralized, automated data hub that ingests multi-domain telemetry, normalizes it via a star-schema warehouse, executes modular SQL transformations, and powers a live executive BI dashboard.
* **The Impact:** Enables executive leadership and departmental managers to explore cross-functional performance metrics in real time through a single pane of glass.

---

## 🏗️ System Architecture & Workflow
1. **Ingestion & Relational Storage:** Raw transaction, customer, and operational tables are ingested into an embedded `DuckDB` relational database instance (`enterprise_warehouse.db`).
2. **Modular SQL Transformation Marts:** Staging views and analytical data marts (`mart_customer_rfm`) clean records and aggregate metrics dynamically.
3. **Automated Analytics Execution Pipeline:** Python routines process advanced analytics (RFM segmentation, risk tiering, and operational metrics) simultaneously.
4. **Interactive BI Presentation:** A multi-page `Streamlit` web app serves live metrics and data visualizations directly to stakeholders.

---

## 💻 Core Code Snippet: Automated Pipeline Execution
```python
def run_enterprise_analytics_pipeline(connection):
    # Execute RFM Customer Tiering & Fraud Risk Scoring
    rfm_df = connection.execute("SELECT * FROM mart_customer_rfm;").df()
    rfm_df['Value_Tier'] = pd.qcut(rfm_df['monetary'], q=2, labels=['Standard Value', 'High Value'])
    
    fraud_query = """
    SELECT transaction_id, customer_id, amount, merchant_category, is_international,
    CASE 
        WHEN amount > 200 AND is_international = 1 THEN 'High Risk'
        ELSE 'Low Risk'
    END AS calculated_risk_tier
    FROM stg_transactions;
    """
    fraud_df = connection.execute(fraud_query).df()
    return rfm_df, fraud_df
enterprise-bi-analytics-platform/
├── notebooks/
│   └── enterprise_analytics_hub.ipynb   # Main end-to-end data notebook
├── app.py                               # Streamlit interactive BI dashboard
├── requirements.txt                     # Project dependencies
└── README.md                            # Comprehensive system documentation
