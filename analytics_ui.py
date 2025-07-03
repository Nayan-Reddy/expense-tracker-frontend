import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def analytics_tab():
    if "session_id" not in st.session_state:
        st.warning("Session not initialized.")
        return

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 3))
    with col2:
        end_date = st.date_input("End Date", datetime.today())

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "session_id": st.session_state.session_id
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        if response.status_code != 200:
            st.error("Failed to fetch analytics.")
            return

        response = response.json()
        df = pd.DataFrame({
            "Category": list(response.keys()),
            "Total": [response[c]["total"] for c in response],
            "Percentage": [response[c]["percentage"] for c in response]
        }).sort_values("Percentage", ascending=False)

        st.title("Expense Breakdown By Category")
        st.bar_chart(df.set_index("Category")["Percentage"], use_container_width=True)

        df["Total"] = df["Total"].map("{:.2f}".format)
        df["Percentage"] = df["Percentage"].map("{:.2f}".format)
        st.table(df)
