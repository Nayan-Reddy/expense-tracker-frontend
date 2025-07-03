import streamlit as st
from datetime import datetime
import requests

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def add_update_tab():
    st.subheader("Manage Your Expenses")

    # Toggle for mobile-friendly layout
    is_mobile_view = st.toggle("📱 Mobile Friendly View", value=False)

    selected_date = st.date_input("Enter Date", datetime.today(), label_visibility="collapsed")

    # Auto-switch to personal session if user is editing demo
    if st.session_state["session_id"] == "demo" and st.session_state.get("user_session_id"):
        st.session_state["session_id"] = st.session_state["user_session_id"]
        st.success("Switched back to your personal session for editing!")

    # Load existing expenses
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}?session_id={st.session_state.session_id}")
        existing_expenses = response.json() if response.status_code == 200 else []
        if response.status_code != 200:
            st.error("Failed to retrieve expenses")
    except:
        st.error("Backend not responding.")
        existing_expenses = []

    categories = ["Education", "Shopping", "Healthcare", "Entertainment", "Groceries", "Utilities", "Transportation", "Miscellaneous"]

    with st.form(key="expense_form"):
        st.markdown("### Enter Your Expenses")
        if not is_mobile_view:
            col1, col2, col3 = st.columns(3)
            with col1: st.text("Amount")
            with col2: st.text("Category")
            with col3: st.text("Notes")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            if is_mobile_view:
                st.markdown(f"#### Entry {i+1}")
                amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}")
                category_input = st.selectbox("Category", categories, index=categories.index(category), key=f"category_{i}")
                notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")
                with col2:
                    category_input = st.selectbox("Category", categories, index=categories.index(category), key=f"category_{i}", label_visibility="collapsed")
                with col3:
                    notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Save Expenses")
        if submit_button:
            if st.session_state["session_id"] == "demo" and st.session_state.get("user_session_id"):
                st.session_state["session_id"] = st.session_state["user_session_id"]
                st.success("Switched to your personal session.")
            filtered_expenses = [e for e in expenses if e["amount"] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}?session_id={st.session_state.session_id}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

    st.markdown("""---  
> **ℹ️ Note:**  
> - You're currently using: `**{}**` session  
> - Switch above between **Demo View** and your **Private Tracker** anytime  
""".format("Demo" if st.session_state["session_id"] == "demo" else "Personal"))
