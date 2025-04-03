# app.py

import streamlit as st
from ui.hr_parlay import show_hr_parlay
from ui.team_parlay import show_team_parlay
from ui.refresh_button import show_refresh_button

st.set_page_config(
    page_title="MLB Parlay Picker",
    layout="wide",
)

st.title("⚾ Parlay Picker: MLB Player Prop Analyzer")

# Navigation tabs
tab = st.sidebar.radio("Navigation", ["HR Parlay Picker", "Team Parlay Picker"])

# Manual refresh with timestamp
show_refresh_button()

# Render selected tab
if tab == "HR Parlay Picker":
    show_hr_parlay()
elif tab == "Team Parlay Picker":
    show_team_parlay()
