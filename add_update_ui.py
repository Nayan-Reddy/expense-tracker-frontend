import streamlit as st
from datetime import datetime
import requests

API_URL = "https://expense-tracker-backend-t4tx.onrender.com"




def add_update_tab():

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
        # st.write(existing_expenses)
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
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

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}",
                                               label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, index=categories.index(category),
                                              key=f"category_{i}", label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")

    st.markdown("""
        > **ℹ️ Note:**  
        > - This app includes **demo expense data** to showcase features in analytics tabs.  
        > - To enter your own data, click **🗑️ Delete Demo Data** below. This will erase all demo entries.  
        > - After deleting, add your own data and view analytics based on that.
        > - You can bring back the demo data anytime by clicking **🔁 Reset Demo Data**.  
        
        """)