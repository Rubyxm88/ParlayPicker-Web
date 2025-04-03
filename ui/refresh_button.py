import streamlit as st
from data.cache import get_last_update_time, clear_cache
from data.update_db import update_all_data
from datetime import datetime

def refresh_data():
    st.markdown("### 🔄 Data Refresh")

    last_updated = get_last_update_time()
    if last_updated:
        st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %I:%M %p')}")
    else:
        st.caption("No data pulled yet.")

    if st.button("🔃 Refresh Now"):
        with st.spinner("Pulling fresh data..."):
            update_all_data()
            clear_cache()
            st.success("✅ Data updated!")

