import streamlit as st
from datetime import datetime
import requests
import uuid

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def add_update_tab():
    st.subheader("Manage Your Expenses")

    # Mobile layout toggle
    is_mobile_view = st.toggle("📱 Mobile Friendly View", value=False)

    # Reset demo data button only
    if st.button("🔄 Reset Demo Data"):
        res = requests.post(f"{API_URL}/reset-demo-data")
        if res.status_code == 200:
            st.success("Demo data restored successfully.")
        else:
            st.error("Failed to reset demo data.")

    # Date selector and fetch
    selected_date = st.date_input("Enter Date", datetime.today(), label_visibility="collapsed")
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}?session_id={st.session_state.session_id}")
        existing_expenses = response.json() if response.status_code == 200 else []
    except:
        st.error("Could not connect to backend.")
        existing_expenses = []

    categories = [
        "Education", "Shopping", "Healthcare", "Entertainment",
        "Groceries", "Utilities", "Transportation", "Miscellaneous"
    ]

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
                category_input = st.selectbox("Category", options=categories, index=categories.index(category), key=f"category_{i}")
                notes_input = st.text_area("Notes", value=notes, key=f"notes_{i}", height=60)
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")
                with col2:
                    category_input = st.selectbox("Category", options=categories, index=categories.index(category), key=f"category_{i}", label_visibility="collapsed")
                with col3:
                    notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Save Expenses")
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            if st.session_state.session_id == "demo":
                st.session_state.session_id = str(uuid.uuid4())
            response = requests.post(f"{API_URL}/expenses/{selected_date}?session_id={st.session_state.session_id}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

    st.markdown("---")
    st.markdown(f"""  
        > **ℹ️ Note:**  
        > - This app has **Demo Data Entries** and shows **Demo data analytics** initially.  
        > - Preview **Demo Data Analytics** for feature insight prior to entering your own data.  
        > - Once you enter your own expenses, analytics will reflect your personal data only.  
        > - To go back to demo data view, click **🔄 Reset Demo Data**.
    """)
