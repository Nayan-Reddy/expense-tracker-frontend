import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def monthly_analytics_tab():
    session_id = st.session_state['session_id']

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 3), key="start_monthly")
    with col2:
        end_date = st.date_input("End Date", datetime.today(), key="end_monthly")

    if st.button("Get Monthly Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "session_id": session_id
        }

        response = requests.post(f"{API_URL}/analytics/monthly", json=payload)
        if response.status_code == 200:
            result = response.json()
            df = pd.DataFrame(result)
            if not df.empty:
                pivot = df.pivot(index="month", columns="category", values="total").fillna(0)
                st.title("Monthly Expense Summary")
                st.bar_chart(pivot)
                st.dataframe(pivot.style.format("{:.2f}"))
            else:
                st.info("No data found for the selected date range.")
        else:
            st.error("Failed to fetch monthly analytics.")
