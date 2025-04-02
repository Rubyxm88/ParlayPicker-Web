import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime

# ------------------------------
# Helpers
# ------------------------------

TEAM_ABBR = {
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

def get_team_id(name):
    for team in statsapi.get('teams', {'sportIds': 1})['teams']:
        if name.lower() in team['name'].lower():
            return team['id']
    return None

def get_next_game(team_id):
    schedule = statsapi.schedule(team=team_id, start_date=None, end_date=None)
    if schedule:
        return schedule[0]
    return None

def get_logo_url(abbr):
    return f"https://a.espncdn.com/i/teamlogos/mlb/500/{abbr.lower()}.png"

def dummy_ev(prop):
    return {
        "line": "o/u 0.5" if prop != "Hits" else "o/u 1.5",
        "trend": "🔥" if prop == "HR" else "Steady",
        "ev": "+12%" if prop == "HR" else "+8%",
        "suggestion": "OVER"
    }

def build_batter_table(team_name):
    data = []
    for i in range(9):
        row = {
            "Pos": i + 1,
            "Player": f"Player {i + 1}"
        }
        for prop in ["HR", "Hits", "RBI"]:
            ev = dummy_ev(prop)
            row[f"{prop} Line"] = ev['line']
            row[f"{prop} Trend"] = ev['trend']
            row[f"{prop} EV"] = ev['ev']
            row[f"{prop} Suggest"] = ev['suggestion']
        data.append(row)
    return pd.DataFrame(data)

def build_pitcher_table(team_name):
    ev = dummy_ev("K")
    return pd.DataFrame([{
        "Pitcher": "TBD",
        "Team": team_name,
        "K Line": "o/u 5.5",
        "K Trend": "Steady",
        "K EV": "+8%",
        "Suggestion": "OVER"
    }])

# ------------------------------
# Streamlit App
# ------------------------------

st.set_page_config(page_title="MLB Parlay Picker", layout="wide")
st.title("⚾ Parlay Picker: MLB Matchups & Props")

team_choice = st.selectbox("Select a team:", list(TEAM_ABBR.keys()))

team_id = get_team_id(team_choice)
game = get_next_game(team_id)

if game:
    home_team = game.get("home_name", "Unknown")
    away_team = game.get("away_name", "Unknown")
    game_time = game.get("game_datetime", "")
    venue = game.get("venue", {}).get("name", "Unknown Venue")

    st.subheader(f"{away_team} @ {home_team} — {datetime.fromisoformat(game_time).strftime('%A, %B %d @ %I:%M %p')}")
    st.write(f"Venue: {venue}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(get_logo_url(TEAM_ABBR.get(away_team, 'NYY')), width=120)
    with col2:
        st.image(get_logo_url(TEAM_ABBR.get(home_team, 'BOS')), width=120)

    # Pitchers
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{away_team} Pitcher")
        st.dataframe(build_pitcher_table(away_team), hide_index=True)
    with col2:
        st.subheader(f"{home_team} Pitcher")
        st.dataframe(build_pitcher_table(home_team), hide_index=True)

    # Batters
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{away_team} Lineup")
        st.dataframe(build_batter_table(away_team), hide_index=True)
    with col2:
        st.subheader(f"{home_team} Lineup")
        st.dataframe(build_batter_table(home_team), hide_index=True)
else:
    st.warning("No upcoming game found.")
