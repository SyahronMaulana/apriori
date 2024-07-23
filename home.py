import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from io import BytesIO

def load_transaction_data():
    if not os.path.isfile("data-transaksi2.csv"):
        st.error("data-transaksi2.csv file not found!")
        return pd.DataFrame(columns=["date_time", "Transaction", "Item"])
    else:
        df = pd.read_csv("data-transaksi2.csv")
    return df

def show_home_page():
    st.title("Home")

    # Display monthly sales chart for the last 5 months
    st.subheader("Monthly Sales Chart (Last 5 Months)")

    # Load transaction data
    df = load_transaction_data()
    
    # Convert `date_time` to datetime
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    
    if df.empty:
        st.write("No transaction data available.")
        return

    # Get the latest date in the data
    latest_date = df['date_time'].max()
    if pd.isna(latest_date):
        st.write("Invalid date data.")
        return

    # Calculate the start date for 5 months ago
    start_date = latest_date - pd.DateOffset(months=5)
    end_date = latest_date

    # Filter data for the last 5 months
    df = df[(df['date_time'] >= start_date) & (df['date_time'] <= end_date)]
    
    # Extract year and month from `date_time`
    df['YearMonth'] = df['date_time'].dt.to_period('M')
    
    # Group by YearMonth and count transactions
    monthly_sales = df.groupby('YearMonth').size().reset_index(name='Sales')

    # Generate a list of all months within the last 5 months
    all_months = pd.period_range(start=start_date.to_period('M'), end=latest_date.to_period('M'), freq='M')
    all_months = all_months.to_frame(index=False, name='YearMonth')
    
    # Merge with monthly sales to ensure all months are shown
    monthly_sales_full = pd.merge(all_months, monthly_sales, on='YearMonth', how='left').fillna(0)
    
    # Create a plot
    plt.figure(figsize=(12, 6))
    plt.bar(monthly_sales_full['YearMonth'].astype(str), monthly_sales_full['Sales'], color='skyblue')
    plt.title('Monthly Sales (Last 5 Months)')
    plt.xlabel('Month')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    
    # Convert plot to BytesIO and display in Streamlit
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf, caption='Monthly Sales Chart (Last 5 Months)')
    buf.close()
