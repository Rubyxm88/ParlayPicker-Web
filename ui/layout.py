import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def team_logo_url(team_abbr):
    return f"https://a.espncdn.com/i/teamlogos/mlb/500/{team_abbr.lower()}.png"

def render_scorecard(home_team, away_team, home_score=None, away_score=None):
    """
    Displays side-by-side team logos and score like a scoreboard.
    """
    col1, col2, col3 = st.columns([1.5, 1, 1.5])

    with col1:
        st.image(team_logo_url(away_team), width=80)
        st.markdown(f"### {away_team}")
        if away_score is not None:
            st.markdown(f"**Score: {away_score}**")

    with col2:
        st.markdown("### @")

    with col3:
        st.image(team_logo_url(home_team), width=80)
        st.markdown(f"### {home_team}")
        if home_score is not None:
            st.markdown(f"**Score: {home_score}**")

def color_ev(ev):
    """
    Return color based on confidence level.
    """
    if ev >= 0.15:
        return "🟢"
    elif ev >= 0.05:
        return "🟡"
    else:
        return "🔴"
