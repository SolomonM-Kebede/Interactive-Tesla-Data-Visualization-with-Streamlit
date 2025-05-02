

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")
st.title("📈 Tesla Revenue and Stock Price Analysis (2010–2025)")

# File uploaders
file_upload1 = st.file_uploader("📊 Upload Tesla Revenue CSV", type="csv")
file_upload2 = st.file_uploader("📈 Upload Tesla Stock CSV", type="csv")

if file_upload1 is not None and file_upload2 is not None:

    # Load data
    revenue_df = pd.read_csv(file_upload1)
    stock_df = pd.read_csv(file_upload2)

    # Previews
    st.subheader("Revenue Data Preview")
    st.dataframe(revenue_df.head())

    st.subheader("Stock Price Data Preview")
    st.dataframe(stock_df.head())

    # Rename for clarity
    revenue_df.columns = ['year', 'quarter', 'revenue_in_millions', 'report_date']
    stock_df.columns = ['idx', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'col8', 'col9']

    # Convert both date columns to datetime
    revenue_df['report_date'] = pd.to_datetime(revenue_df['report_date'], errors='coerce')
    stock_df['Date'] = pd.to_datetime(stock_df['Date'], errors='coerce', utc=True)

    # Remove timezone info from stock data (make it naive)
    stock_df['Date'] = stock_df['Date'].dt.tz_localize(None)

    # Sort both for merge_asof
    revenue_df = revenue_df.sort_values('report_date')
    stock_df = stock_df.sort_values('Date')

    # Merge using asof
    merged_df = pd.merge_asof(
        revenue_df,
        stock_df,
        left_on='report_date',
        right_on='Date',
        direction='nearest'
    )


    chart1 = alt.Chart(merged_df).mark_line(point=True).encode(
        x='report_date:T',
        y='revenue_in_millions:Q',
        tooltip=['report_date', 'revenue_in_millions']
    ).properties(title="Tesla Quarterly Revenue Over Time")

    chart2 = alt.Chart(merged_df).mark_circle(size=60).encode(
        x='revenue_in_millions:Q',
        y='Close:Q',
        tooltip=['report_date', 'revenue_in_millions', 'Close']
    ).properties(title="Tesla Revenue vs. Stock Close Price")

    st.altair_chart(chart1, use_container_width=True)
    st.altair_chart(chart2, use_container_width=True)
