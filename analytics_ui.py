import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def analytics_tab():
    session_id = st.session_state.session_id if st.session_state.get("user_entered_data") else "demo"

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 3))
    with col2:
        end_date = st.date_input("End Date", datetime.today())

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "session_id": session_id
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        if response.status_code != 200:
            st.error("Failed to fetch analytics.")
            return

        data = response.json()
        df = pd.DataFrame({
            "Category": list(data.keys()),
            "Total": [data[cat]["total"] for cat in data],
            "Percentage": [data[cat]["percentage"] for cat in data]
        }).sort_values(by="Percentage", ascending=False)

        st.title("Expense Breakdown By Category")
        st.bar_chart(data=df.set_index("Category")["Percentage"], use_container_width=True)
        df["Total"] = df["Total"].map("{:.2f}".format)
        df["Percentage"] = df["Percentage"].map("{:.2f}".format)
        st.table(df)
