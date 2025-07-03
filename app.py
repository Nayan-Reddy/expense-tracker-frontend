import streamlit as st
import uuid
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from monthly_analytics_ui import monthly_analytics_tab

st.title("Expense Tracking System")

# Generate unique session_id once per user session
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = str(uuid.uuid4())

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics", "Monthly Analytics"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_analytics_tab()
