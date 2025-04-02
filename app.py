import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime, timedelta

# --- Utility functions ---

def get_team_id_abbr(team_name):
    for team in statsapi.get('teams', {'sportIds': 1})['teams']:
        if team_name.lower() in team['name'].lower():
            return team['id'], team['abbreviation']
    return None, None

def get_next_game(team_id):
    today = datetime.now().date()
    schedule = statsapi.schedule(start_date=today, end_date=today + timedelta(days=7), team=team_id)
    return schedule[0] if schedule else None

def get_probable_pitchers(game_id):
    box = statsapi.boxscore_data(game_id)
    pitchers = {"home": "TBD", "away": "TBD"}
    for side in ["home", "away"]:
        try:
            pitchers[side] = box["teamInfo"][side]["probablePitcher"]["fullName"]
        except KeyError:
            pass
    return pitchers

def get_logo_url(abbr):
    return f"https://a.espncdn.com/i/teamlogos/mlb/500/{abbr.lower()}.png"

def color_gradient(ev_percent):
    try:
        value = int(ev_percent.replace('%', '').replace('+', '').replace('-', ''))
    except:
        return "white"
    if "–" in ev_percent or "-" in ev_percent:
        return "#ff4d4d"  # red
    elif value >= 80:
        return "#00ff00"  # strong green
    elif value >= 60:
        return "#66ff66"  # medium green
    elif value >= 50:
        return "#b3ffb3"  # light green
    else:
        return "white"

def dummy_ev(prop):
    return {
        "line": "o/u 0.5" if prop != "Hits" else "o/u 1.5",
        "trend": "🔥" if prop == "HR" else "Steady",
        "ev": "+12%" if prop == "HR" else "+5%",
        "suggestion": "OVER"
    }

def build_pitcher_table(pitcher_name, team_name):
    return pd.DataFrame([{
        "Pitcher": pitcher_name,
        "Team": team_name,
        "K Line": "o/u 5.5",
        "K Trend": "Steady",
        "K EV": "+8%",
        "Suggestion": "OVER"
    }])

def build_batter_table(team_name):
    data = []
    for i in range(9):
        row = {
            "Pos": i + 1,
            "Player": f"Player {i + 1}"
        }
        for prop in ["HR", "Hits", "RBI"]:
            ev_data = dummy_ev(prop)
            row[f"{prop} Line"] = ev_data['line']
            row[f"{prop} Trend"] = ev_data['trend']
            row[f"{prop} EV"] = ev_data['ev']
            row[f"{prop} Suggest"] = ev_data['suggestion']
        data.append(row)
    return pd.DataFrame(data)


# --- Streamlit Layout ---

st.set_page_config(page_title="MLB Parlay Picker", layout="wide")
st.title("⚾ Parlay Picker: MLB Matchups & Props")

# Sidebar
TEAMS = [t['name'] for t in statsapi.get('teams', {'sportIds': 1})['teams']]
selected_team = st.sidebar.selectbox("Select Your Team", TEAMS)

# Game Info
team_id, team_abbr = get_team_id_abbr(selected_team)
game = get_next_game(team_id)

if game:
    home_team = game["home_name"]
    away_team = game["away_name"]
    home_id, home_abbr = get_team_id_abbr(home_team)
    away_id, away_abbr = get_team_id_abbr(away_team)
    game_time = game["game_datetime"]

    st.subheader(f"{away_team} @ {home_team} — {datetime.fromisoformat(game_time).strftime('%A, %B %d @ %I:%M %p')}")
    st.write(f"Venue: {game['venue']}")
    st.image([get_logo_url(away_abbr), get_logo_url(home_abbr)], width=150)

    # Pitchers
    pitchers = get_probable_pitchers(game["game_id"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{away_team} Pitcher")
        st.dataframe(build_pitcher_table(pitchers['away'], away_team), use_container_width=True)
        st.subheader(f"{away_team} Lineup")
        st.dataframe(build_batter_table(away_team), use_container_width=True)

    with col2:
        st.subheader(f"{home_team} Pitcher")
        st.dataframe(build_pitcher_table(pitchers['home'], home_team), use_container_width=True)
        st.subheader(f"{home_team} Lineup")
        st.dataframe(build_batter_table(home_team), use_container_width=True)
else:
    st.warning("No upcoming game found for this team.")
