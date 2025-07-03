import streamlit as st
from datetime import datetime
import requests

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"

def add_update_tab():
    # Layout toggle
    layout = st.radio("Choose layout", ["Mobile", "Desktop"], horizontal=True)

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
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        if layout == "Desktop":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text("Amount")
            with col2:
                st.text("Category")
            with col3:
                st.text("Notes")
        else:
            st.text("Amount")
            st.text("Category")
            st.text("Notes")

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

            if layout == "Desktop":
                col1, col2, col3 = st.columns(3)
                with col1:
                    amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")
                with col2:
                    category_input = st.selectbox("Category", categories, index=categories.index(category), key=f"category_{i}", label_visibility="collapsed")
                with col3:
                    notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")
            else:
                amount_input = st.number_input("Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}")
                category_input = st.selectbox("Category", categories, index=categories.index(category), key=f"category_{i}")
                notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Submit")
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

    # Notes section at the bottom
    st.markdown("""
    ---
    > **ℹ️ Notes:**
    > - This app includes **demo expense data** to showcase features in analytics tabs.  
    > - To enter your own data, click **🗑️ Delete Demo Data** above. This will erase all demo entries.  
    > - After deleting, add your own data and view analytics based on that.  
    > - You can bring back the demo data anytime by clicking **🔁 Reset Demo Data**.
    > - Access demo data analytics by selecting the tabs above and clicking 'Get' to visualize results.
    """)
