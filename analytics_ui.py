import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"
SESSION_ID = "demo"

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 3))
    with col2:
        end_date = st.date_input("End Date", datetime.today())

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "session_id": SESSION_ID
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        if response.status_code == 200:
            response = response.json()
            data = {
                "Category": list(response.keys()),
                "Total": [response[cat]["total"] for cat in response],
                "Percentage": [response[cat]["percentage"] for cat in response]
            }

            df = pd.DataFrame(data).sort_values(by="Percentage", ascending=False)
            st.title("Expense Breakdown By Category")
            st.bar_chart(data=df.set_index("Category")['Percentage'], use_container_width=True)

            df["Total"] = df["Total"].map("{:.2f}".format)
            df["Percentage"] = df["Percentage"].map("{:.2f}".format)
            st.table(df)
        else:
            st.error("Failed to retrieve analytics.")
