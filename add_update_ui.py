import streamlit as st
from datetime import datetime
import requests

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def add_update_tab():
    st.subheader("Manage Your Expenses")

    session_id = st.session_state['session_id']

    # Demo data buttons
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

    selected_date = st.date_input("Enter Date", datetime.today(), label_visibility="collapsed")

    response = requests.get(f"{API_URL}/expenses/{selected_date}", params={"session_id": session_id})
    existing_expenses = response.json() if response.status_code == 200 else []
    if response.status_code != 200:
        st.error("Failed to retrieve expenses")

    categories = ["Education", "Shopping", "Healthcare", "Entertainment", "Groceries", "Utilities", "Transportation", "Miscellaneous"]

    with st.form(key="expense_form"):
        st.markdown("### Enter Your Expenses")

        is_mobile_view = st.toggle("📱 Mobile Friendly View", value=False)

        expenses = []
        for i in range(5):
            amount = existing_expenses[i]['amount'] if i < len(existing_expenses) else 0.0
            category = existing_expenses[i]['category'] if i < len(existing_expenses) else "Shopping"
            notes = existing_expenses[i]['notes'] if i < len(existing_expenses) else ""

            if is_mobile_view:
                st.markdown(f"#### Entry {i+1}")
                amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}")
                category_input = st.selectbox("Category", options=categories, index=categories.index(category), key=f"category_{i}")
                notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}")
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
            response = requests.post(
                f"{API_URL}/expenses/{selected_date}",
                params={"session_id": session_id},
                json=filtered_expenses
            )
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

    st.markdown("""
    ---
    > **ℹ️ Note:**
    > - This app includes **Demo expense data** to showcase features in analytics tabs.  
    > - Submitting your data without deleting Demo data will mix your entries with it, making results inaccurate. 
    > - To enter your own data, click **🗑️ Delete Demo Data** above. This will erase all demo entries.  
    > - After deleting, add your data to view analytics specific to your entries. 
    > - You can bring back the demo data anytime by clicking **🔁 Reset Demo Data**.
    > - Access demo data analytics by selecting the tabs above and clicking 'Get analytics' to visualize results.
    """)
