import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from monthly_analytics_ui import monthly_analytics_tab
import uuid

# Manage session
if "session_id" not in st.session_state:
    st.session_state["session_id"] = "demo"
if "user_session_id" not in st.session_state:
    st.session_state["user_session_id"] = None

st.title("Expense Tracking System")

if st.session_state["session_id"] == "demo":
    if st.button("👤 Start Using Your Own Tracker"):
        st.session_state["user_session_id"] = str(uuid.uuid4())
        st.session_state["session_id"] = st.session_state["user_session_id"]
        st.success("Switched to your own personal tracker session!")

else:
    if st.button("👁️ View Demo Data Again"):
        st.session_state["session_id"] = "demo"
        st.success("Now viewing demo data only. Your personal data is safe.")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics", "Monthly Analytics"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_analytics_tab()
