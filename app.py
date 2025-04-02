# app.py
import streamlit as st
from mlb_api import get_next_game, get_probable_pitchers
from datetime import datetime

st.set_page_config(page_title="Parlay Picker", layout="wide")

st.title("⚾ Parlay Picker: MLB Props & Matchups")

# Sidebar team selector
st.sidebar.header("Select Your Team")
TEAMS = [
    'Arizona Diamondbacks', 'Atlanta Braves', 'Baltimore Orioles', 'Boston Red Sox',
    'Chicago White Sox', 'Chicago Cubs', 'Cincinnati Reds', 'Cleveland Guardians',
    'Colorado Rockies', 'Detroit Tigers', 'Houston Astros', 'Kansas City Royals',
    'Los Angeles Angels', 'Los Angeles Dodgers', 'Miami Marlins', 'Milwaukee Brewers',
    'Minnesota Twins', 'New York Yankees', 'New York Mets', 'Oakland Athletics',
    'Philadelphia Phillies', 'Pittsburgh Pirates', 'San Diego Padres',
    'San Francisco Giants', 'Seattle Mariners', 'St. Louis Cardinals',
    'Tampa Bay Rays', 'Texas Rangers', 'Toronto Blue Jays', 'Washington Nationals'
]

selected_team = st.sidebar.selectbox("Team", TEAMS)

# Fetch and display game info
with st.spinner("Fetching next game info..."):
    game = get_next_game(selected_team)

if not game:
    st.error("No upcoming games found for this team.")
    st.stop()

# Format game time
game_dt = datetime.fromisoformat(game["game_time"].replace("Z", "+00:00"))
pretty_date = game_dt.strftime("%A, %B %d @ %I:%M %p")

# Game header
st.markdown(f"### {game['away']} @ {game['home']} — {pretty_date}")
st.markdown(f"**Venue:** {game['venue']}")

# Fetch probable pitchers
pitchers = get_probable_pitchers(game["game_id"])

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"🧢 {game['away']} Pitcher")
    st.write(pitchers['away'])

with col2:
    st.subheader(f"🧢 {game['home']} Pitcher")
    st.write(pitchers['home'])

# --- Placeholder: Lineup Fetch (to be replaced later with live data) ---
dummy_lineup = [f"Player {i+1}" for i in range(9)]

def build_lineup_table(team_name, players):
    """Display lineup with placeholder props."""
    st.markdown(f"#### {team_name} Lineup")
    st.table({
        "Pos": list(range(1, 10)),
        "Player": players,
        "HR Line": ["o/u 0.5"] * 9,
        "Trend": ["Steady"] * 9,
        "+EV": ["+5%"] * 9
    })

# --- Display both team lineups ---
col1, col2 = st.columns(2)

with col1:
    build_lineup_table(game['away'], dummy_lineup)

with col2:
    build_lineup_table(game['home'], dummy_lineup)
