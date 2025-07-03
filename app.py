import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from monthly_analytics_ui import monthly_analytics_tab
import uuid

# Unique session ID per user
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "demo"
if "user_entered_data" not in st.session_state:
    st.session_state["user_entered_data"] = False  # Flag for switching between demo and user session

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics", "Monthly Analytics"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_analytics_tab()
