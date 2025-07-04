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

        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload)

            # If no data, fallback to demo session
            if response.status_code == 200:
                data = response.json()
                if not data or sum(row["total"] for row in data.values()) == 0:
                    # Fallback to demo
                    st.session_state.session_id = "demo"
                    st.info("No personal data found. Switched to Demo Analytics.")
                    st.experimental_rerun()
            else:
                st.error("Failed to fetch analytics.")
                return

            df = pd.DataFrame({
                "Category": list(data.keys()),
                "Total": [data[cat]["total"] for cat in data],
                "Percentage": [data[cat]["percentage"] for cat in data]
            })

            df_sorted = df.sort_values(by="Percentage", ascending=False)
            st.title("Expense Breakdown By Category")
            st.bar_chart(df_sorted.set_index("Category")["Percentage"], use_container_width=True)

            df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
            df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)
            st.table(df_sorted)

        except Exception:
            st.error("Error communicating with the backend.")
