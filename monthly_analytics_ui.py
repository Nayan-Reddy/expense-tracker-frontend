import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def monthly_analytics_tab():
    if "session_id" not in st.session_state:
        st.warning("Session not initialized.")
        return

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2025, 1, 3), key="start_monthly")
    with col2:
        end_date = st.date_input("End Date", datetime.today(), key="end_monthly")

    if st.button("Get Monthly Analytics"):
        original_session = st.session_state.session_id
        is_demo_fallback = False

        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "session_id": original_session
        }

        try:
            response = requests.post(f"{API_URL}/analytics/monthly", json=payload)
            if response.status_code == 200 and response.json():
                result = response.json()
            else:
                # Fallback to demo session if no personal data
                payload["session_id"] = "demo"
                response = requests.post(f"{API_URL}/analytics/monthly", json=payload)
                if response.status_code == 200 and response.json():
                    result = response.json()
                    is_demo_fallback = True
                else:
                    st.info("No data found for selected range.")
                    return

            # ✅ Show demo message when needed
            if original_session == "demo" or is_demo_fallback:
                st.info("You are viewing demo data analytics.")

            df = pd.DataFrame(result)
            if df.empty:
                st.info("No data found.")
                return

            pivot = df.pivot(index="month", columns="category", values="total").fillna(0)
            st.title("Monthly Expense Summary")
            st.bar_chart(pivot)
            st.dataframe(pivot.style.format("{:.2f}"))

        except Exception:
            st.error("Error communicating with the backend.")
