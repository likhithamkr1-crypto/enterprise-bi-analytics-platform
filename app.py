import streamlit as st
import duckdb
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Enterprise BI & Analytics Platform",
    page_icon="📊",
    layout="wide"
)

st.title("🚀 Enterprise BI & Automated Operations Data Hub")
st.markdown("A unified analytics workspace integrating Marketing RFM, Financial Risk, Operations, and SaaS Retention.")

# Database & Data Setup
@st.cache_resource
def init_db():
    con = duckdb.connect(database=':memory:')
    
    # 1. Marketing Data
    np.random.seed(42)
    customers = [f"CUST_{i:04d}" for i in range(1, 101)]
    rfm_data = pd.DataFrame({
        'customer_id': customers,
        'recency': np.random.randint(1, 365, size=100),
        'frequency': np.random.randint(1, 50, size=100),
        'monetary': np.random.uniform(50.0, 5000.0, size=100).round(2)
    })
    con.register('raw_rfm', rfm_data)
    con.execute("""
        CREATE TABLE mart_customer_rfm AS 
        SELECT customer_id, recency, frequency, monetary,
               CASE 
                   WHEN recency <= 30 AND frequency >= 20 THEN 'VIP'
                   WHEN recency <= 90 THEN 'Active'
                   ELSE 'At-Risk'
               END AS rfm_segment
        FROM raw_rfm
    """)

    # 2. Financial Fraud Data
    transactions = pd.DataFrame({
        'transaction_id': [f"TXN_{i:05d}" for i in range(1, 201)],
        'customer_id': np.random.choice(customers, 200),
        'amount': np.random.uniform(10.0, 2500.0, 200).round(2),
        'is_international': np.random.choice([0, 1], 200, p=[0.85, 0.15])
    })
    con.register('raw_txns', transactions)
    con.execute("""
        CREATE TABLE stg_transactions AS 
        SELECT transaction_id, customer_id, amount, is_international,
               CASE 
                   WHEN amount > 1000 AND is_international = 1 THEN 'High Risk'
                   WHEN amount > 500 THEN 'Medium Risk'
                   ELSE 'Low Risk'
               END AS risk_level
        FROM raw_txns
    """)
    
    return con

con = init_db()

# Sidebar Navigation
st.sidebar.header("Navigation & Filters")
domain = st.sidebar.radio("Select Domain:", ["Executive Overview", "Marketing RFM", "Financial Risk"])

if domain == "Executive Overview":
    st.header("📈 Executive Overview")
    col1, col2, col3 = st.columns(3)
    
    total_cust = con.execute("SELECT COUNT(*) FROM mart_customer_rfm").fetchone()[0]
    total_rev = con.execute("SELECT SUM(monetary) FROM mart_customer_rfm").fetchone()[0]
    high_risk = con.execute("SELECT COUNT(*) FROM stg_transactions WHERE risk_level = 'High Risk'").fetchone()[0]
    
    col1.metric("Total Active Customers", f"{total_cust}")
    col2.metric("Total Revenue", f"${total_rev:,.2f}")
    col3.metric("High Risk Transactions", f"{high_risk}")
    
    st.markdown("---")
    st.subheader("Customer Distribution by Segment")
    df_segments = con.execute("SELECT rfm_segment, COUNT(*) as count FROM mart_customer_rfm GROUP BY rfm_segment").df()
    st.bar_chart(df_segments.set_index('rfm_segment'))

elif domain == "Marketing RFM":
    st.header("🎯 Marketing & RFM Segmentation")
    segment_filter = st.sidebar.multiselect(
        "Filter Segment:", 
        ["VIP", "Active", "At-Risk"], 
        default=["VIP", "Active", "At-Risk"]
    )
    
    query = f"SELECT * FROM mart_customer_rfm WHERE rfm_segment IN ({','.join([repr(s) for s in segment_filter])})"
    df_rfm = con.execute(query).df()
    
    st.dataframe(df_rfm, use_container_width=True)

elif domain == "Financial Risk":
    st.header("🛡️ Financial Risk Analytics")
    risk_filter = st.sidebar.selectbox("Risk Level:", ["All", "High Risk", "Medium Risk", "Low Risk"])
    
    if risk_filter == "All":
        df_risk = con.execute("SELECT * FROM stg_transactions").df()
    else:
        df_risk = con.execute(f"SELECT * FROM stg_transactions WHERE risk_level = '{risk_filter}'").df()
        
    st.dataframe(df_risk, use_container_width=True)
