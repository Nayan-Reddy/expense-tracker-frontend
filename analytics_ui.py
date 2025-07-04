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
        original_session = st.session_state.session_id
        is_demo_fallback = False

        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "session_id": original_session
        }

        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload)
            if response.status_code == 200 and response.json():
                data = response.json()
            else:
                # Fallback to demo session if no personal data
                payload["session_id"] = "demo"
                response = requests.post(f"{API_URL}/analytics/", json=payload)
                if response.status_code == 200 and response.json():
                    data = response.json()
                    is_demo_fallback = True
                else:
                    st.info("No data found for the selected range.")
                    return

            # ✅ Show demo message when needed
            if original_session == "demo" or is_demo_fallback:
                st.info("You are viewing demo data analytics.")

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
