import streamlit as st
from datetime import datetime
import requests
import uuid

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def add_update_tab():
    st.subheader("Manage Your Expenses")

    is_mobile_view = st.toggle("📱 Mobile Friendly View", value=False)

    # Demo Data Control Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("❌ Delete Demo Data"):
            res = requests.delete(f"{API_URL}/delete-demo-data")
            if res.status_code == 200:
                st.success("Demo data deleted successfully.")
                # Enable session mode after deleting demo data
                st.session_state.session_id = str(uuid.uuid4())
                st.session_state.user_entered_data = False
            else:
                st.error("Failed to delete demo data.")
    with col2:
        if st.button("🔄 Reset Demo Data"):
            res = requests.post(f"{API_URL}/reset-demo-data")
            if res.status_code == 200:
                st.success("Demo data restored successfully.")
                st.session_state.session_id = "demo"
                st.session_state.user_entered_data = False
            else:
                st.error("Failed to reset demo data.")

    # Load existing expenses
    selected_date = st.date_input("Enter Date", datetime.today(), label_visibility="collapsed")
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}?session_id={st.session_state.session_id}")
        existing_expenses = response.json() if response.status_code == 200 else []
    except:
        st.error("Could not connect to backend.")
        existing_expenses = []

    categories = ["Education", "Shopping", "Healthcare", "Entertainment", "Groceries", "Utilities", "Transportation", "Miscellaneous"]

    with st.form("expense_form"):
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
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        if st.form_submit_button("Save Expenses"):
            filtered_expenses = [e for e in expenses if e["amount"] > 0]
            if st.session_state.session_id == "demo":
                st.session_state.session_id = str(uuid.uuid4())
            st.session_state.user_entered_data = True
            res = requests.post(f"{API_URL}/expenses/{selected_date}?session_id={st.session_state.session_id}", json=filtered_expenses)
            if res.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

    st.markdown("""---  
> **ℹ️ Note:**  
> - This app includes **Demo data** for analytics.  
> - Submitting without deleting demo data may mix your entries.  
> - Click **🗑️ Delete Demo Data** to start fresh.  
> - You can restore it anytime with **🔄 Reset Demo Data**.  
> - Your session data is isolated and private.""")
