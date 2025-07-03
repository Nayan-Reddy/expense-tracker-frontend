import streamlit as st
from datetime import datetime
import requests

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def add_update_tab():
    st.markdown("## Add / Update Expenses")

    # --- Buttons Row ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Delete Demo Data"):
            res = requests.delete(f"{API_URL}/delete-demo-data")
            if res.status_code == 200:
                st.success("Demo data deleted successfully.")
            else:
                st.error("Failed to delete demo data.")
    with col2:
        if st.button("🔄 Reset Demo Data"):
            res = requests.post(f"{API_URL}/reset-demo-data")
            if res.status_code == 200:
                st.success("Demo data restored successfully.")
            else:
                st.error("Failed to reset demo data.")

    st.markdown("---")

    # --- Date Picker ---
    selected_date = st.date_input("Select Date", datetime.today())

    # --- Fetch existing data ---
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        response.raise_for_status()
        existing_expenses = response.json()
    except:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    # --- Category list ---
    categories = [
        "Education", "Shopping", "Healthcare", "Entertainment",
        "Groceries", "Utilities", "Transportation", "Miscellaneous"
    ]

    # --- Expense Input Form ---
    with st.form(key="expense_form"):
        st.subheader("Enter Your Expenses")
        expenses = []

        for i in range(5):
            st.markdown(f"**Expense {i+1}**")
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}")
            category_input = st.selectbox("Category", options=categories, index=categories.index(category), key=f"category_{i}")
            notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}")

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

            st.markdown("---")

        submit_button = st.form_submit_button("💾 Submit")
        if submit_button:
            filtered_expenses = [e for e in expenses if e["amount"] > 0]
            try:
                response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
                response.raise_for_status()
                st.success("Expenses updated successfully!")
            except:
                st.error("Failed to update expenses.")

    # --- Help Info Note (at bottom) ---
    st.markdown("""
    <div style='margin-top: 40px; padding: 10px; background-color: #f1f3f5; border-radius: 8px; font-size: 0.9rem;'>
        <b>ℹ️ Notes:</b>
        <ul>
            <li>This app includes <b>demo expense data</b> for exploring features.</li>
            <li>To add your own data, press <b>❌ Delete Demo Data</b>.</li>
            <li>You can bring demo data back anytime using <b>🔄 Reset Demo Data</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
