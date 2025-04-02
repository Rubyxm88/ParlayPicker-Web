import streamlit as st
import pandas as pd
from datetime import datetime
from mlb_api import get_game, get_team_lineup

# Team abbreviation + logo map
TEAMS = {
    "Arizona Diamondbacks": "ARI", "Atlanta Braves": "ATL", "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS", "Chicago White Sox": "CWS", "Chicago Cubs": "CHC",
    "Cincinnati Reds": "CIN", "Cleveland Guardians": "CLE", "Colorado Rockies": "COL",
    "Detroit Tigers": "DET", "Houston Astros": "HOU", "Kansas City Royals": "KC",
    "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD", "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN", "New York Yankees": "NYY",
    "New York Mets": "NYM", "Oakland Athletics": "OAK", "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT", "San Diego Padres": "SD", "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL", "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX", "Toronto Blue Jays": "TOR", "Washington Nationals": "WSH"
}

st.set_page_config(page_title="MLB Parlay Picker", layout="wide")
st.title("⚾ Parlay Picker: MLB Matchups & Props")

# Team selection
team_name = st.selectbox("Select a team:", list(TEAMS.keys()))
mode = st.radio("Show:", ["Upcoming Game", "Last Game"], horizontal=True)
mode_key = "next" if mode == "Upcoming Game" else "last"

# Fetch game
game = get_game(team_name, mode_key)

if not game:
    st.error("No game found for selected mode.")
    st.stop()

# Extract info
home_team = game["home_name"]
away_team = game["away_name"]
home_abbr = TEAMS.get(home_team, "")
away_abbr = TEAMS.get(away_team, "")
game_time = game["game_datetime"]
venue = game.get("venue_name", "Unknown Venue")

st.subheader(f"{away_team} @ {home_team} — {pd.to_datetime(game_time).strftime('%A, %B %d @ %I:%M %p')}")
st.caption(f"Venue: {venue}")

# Team logos
col1, col2 = st.columns(2)
with col1:
    st.image(f"https://a.espncdn.com/i/teamlogos/mlb/500/{away_abbr.lower()}.png", width=120)
with col2:
    st.image(f"https://a.espncdn.com/i/teamlogos/mlb/500/{home_abbr.lower()}.png", width=120)

# Pitcher info placeholder
def build_pitcher_table(team_name):
    return pd.DataFrame([{
        "Pitcher": "TBD",
        "Team": team_name,
        "K Line": "o/u 5.5",
        "K Trend": "Steady",
        "K EV": "+8%",
        "Suggestion": "OVER"
    }])

# Display pitcher info
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{away_team} Pitcher")
    st.dataframe(build_pitcher_table(away_team), use_container_width=True)

with col2:
    st.subheader(f"{home_team} Pitcher")
    st.dataframe(build_pitcher_table(home_team), use_container_width=True)

# EV Logic
def dummy_ev(prop):
    return {
        "line": "o/u 0.5" if prop != "Hits" else "o/u 1.5",
        "trend": "🔥" if prop == "HR" else "Steady",
        "ev": "+12%",
        "suggestion": "OVER"
    }

# Build batter table
def build_batter_table(players):
    data = []
    for i, player in enumerate(players):
        row = {"Pos": i+1, "Player": player}
        for prop in ["HR", "Hits", "RBI"]:
            ev = dummy_ev(prop)
            row[f"{prop} Line"] = ev["line"]
            row[f"{prop} Trend"] = ev["trend"]
            row[f"{prop} EV"] = ev["ev"]
            row[f"{prop} Suggest"] = ev["suggestion"]
        data.append(row)
    return pd.DataFrame(data)

# Lineups (dummy for now)
away_lineup = get_team_lineup(game, away_abbr)
home_lineup = get_team_lineup(game, home_abbr)

# Display lineups
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"{away_team} Lineup")
    if away_lineup:
        st.dataframe(build_batter_table(away_lineup), use_container_width=True)
    else:
        st.write("empty")

with col2:
    st.subheader(f"{home_team} Lineup")
    if home_lineup:
        st.dataframe(build_batter_table(home_lineup), use_container_width=True)
    else:
        st.write("empty")
