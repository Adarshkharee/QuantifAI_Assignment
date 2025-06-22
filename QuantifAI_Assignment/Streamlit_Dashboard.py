import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("ecommerce.db")

st.set_page_config(page_title="QuantifAI Dashboard", layout="wide")
st.title("E-Commerce Dashboard – QuantifAI Assessment")

customer_filter = st.text_input("Search by Customer ID")

orders = pd.read_sql("SELECT * FROM orders", conn)
customers = pd.read_sql("SELECT * FROM customers", conn)
products = pd.read_sql("SELECT * FROM products", conn)

if customer_filter:
    orders = orders[orders['customer_id'].astype(str).str.contains(customer_filter)]

total_sales = orders['amount'].sum() if 'amount' in orders.columns else 0
total_orders = orders.shape[0]
unique_customers = customers['customer_id'].nunique() if 'customer_id' in customers.columns else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Unique Customers", unique_customers)

if 'order_date' in orders.columns and 'amount' in orders.columns:
    st.subheader("Sales Over Time")
    orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
    sales_trend = orders.groupby('order_date')['amount'].sum().reset_index()
    st.line_chart(sales_trend.set_index('order_date'))

st.subheader("Orders Table Preview")
st.dataframe(orders.head())

conn.close()