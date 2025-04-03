import streamlit as st
from data.cache import get_last_update_time, write_cache, is_cache_stale
from data.update_db import update_all
from datetime import datetime

def show_refresh_button():
    st.markdown("### 🔄 Data Refresh")

    last_updated = get_last_update_time()
    if last_updated:
        st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %I:%M %p')}")
    else:
        st.caption("No data pulled yet.")

    if st.button("🔃 Refresh Now"):
        with st.spinner("Pulling fresh data..."):
            update_all()
            write_cache()
            st.success("✅ Data updated!")
