import duckdb
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Enterprise BI & Operations Hub", layout="wide"
)

st.title("🚀 Omnichannel Business Intelligence & Operations Hub")
st.markdown(
    "Centralized analytics platform integrating Marketing, Operations, and Financial Risk telemetry."
)

# Initialize connection and run basic queries
@st.cache_resource
def load_data():
  con = duckdb.connect(database=":memory:")
  # Re-inject sample data for the app view
  con.execute("""
        CREATE TABLE fact_transactions AS SELECT * FROM (
            SELECT 'TXN_101' AS transaction_id, 'CUST_A' AS customer_id, TIMESTAMP '2026-09-01' AS order_date, 150.00 AS amount, 'Electronics' AS merchant_category, 0 AS is_international, 'Completed' AS order_status UNION ALL
            SELECT 'TXN_102', 'CUST_B', TIMESTAMP '2026-09-05', 45.50, 'Grocery', 0, 'Completed' UNION ALL
            SELECT 'TXN_103', 'CUST_A', TIMESTAMP '2026-09-15', 300.00, 'Electronics', 1, 'Completed' UNION ALL
            SELECT 'TXN_104', 'CUST_C', TIMESTAMP '2026-09-20', 80.00, 'Dining', 0, 'Completed' UNION ALL
            SELECT 'TXN_105', 'CUST_B', TIMESTAMP '2026-10-01', 210.00, 'Grocery', 0, 'Completed' UNION ALL
            SELECT 'TXN_106', 'CUST_A', TIMESTAMP '2026-10-10', 120.00, 'Luxury', 1, 'Completed'
        );
    """)
  rfm_df = con.execute("""
        WITH Snapshot AS (SELECT MAX(order_date) AS max_date FROM fact_transactions)
        SELECT customer_id, (SELECT max_date FROM Snapshot) - MAX(order_date) AS recency_days, 
               COUNT(DISTINCT transaction_id) AS frequency, ROUND(SUM(amount), 2) AS monetary 
        FROM fact_transactions WHERE order_status = 'Completed' GROUP BY customer_id;
    &quot;&quot;").df()
  return rfm_df


df_rfm = load_data()

# Sidebar Navigation
tab1, tab2 = st.tabs(
    ["📊 Executive Overview", "👥 Customer RFM Segmentation"]
)

with tab1:
  st.header("Platform High-Level Performance")
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Platform Revenue", f"${df_rfm['monetary'].sum():,.2f}")
  col2.metric("Total Active Customers", len(df_rfm))
  col3.metric("Average Customer Spend", f"${df_rfm['monetary'].mean():,.2f}")

  st.subheader("Recent Transaction Analytics")
  st.dataframe(df_rfm, use_container_width=True)

with tab2:
  st.header("Customer Behavioral Analysis")
  st.markdown("Detailed breakdown of customer recency, frequency, and spend.")
  st.bar_chart(df_rfm.set_index("customer_id")["monetary"])
