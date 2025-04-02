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
    schedule = statsapi.schedule(team=team_id)
    return schedule[0] if schedule else None

def get_logo_url(abbr):
    return f"https://a.espncdn.com/i/teamlogos/mlb/500/{abbr.lower()}.png"

def dummy_ev(prop):
    return {
        "line": "o/u 0.5" if prop != "Hits" else "o/u 1.5",
        "trend": "🔥" if prop == "HR" else "Steady",
        "ev": "+12%" if prop == "HR" else "+8%",
        "suggestion": "OVER"
    }

def get_lineups(game_id):
    boxscore = statsapi.boxscore_data(game_id)
    away = boxscore['away']['players']
    home = boxscore['home']['players']

    def extract_players(players):
        lineup = []
        for pid, pdata in players.items():
            if 'battingOrder' in pdata:
                lineup.append((int(pdata['battingOrder']), pdata['person']['fullName']))
        return [p[1] for p in sorted(lineup)]

    return extract_players(away), extract_players(home)

def get_pitcher_name(game, team_type):
    try:
        return game[f'{team_type}_probable_pitcher']['fullName']
    except:
        return "TBD"

def build_batter_table(names):
    data = []
    for i, player in enumerate(names):
        row = {"Pos": i + 1, "Player": player}
        for prop in ["HR", "Hits", "RBI"]:
            ev = dummy_ev(prop)
            row[f"{prop} Line"] = ev['line']
            row[f"{prop} Trend"] = ev['trend']
            row[f"{prop} EV"] = ev['ev']
            row[f"{prop} Suggest"] = ev['suggestion']
        data.append(row)
    return pd.DataFrame(data)

def build_pitcher_table(team, pitcher):
    ev = dummy_ev("K")
    return pd.DataFrame([{
        "Pitcher": pitcher,
        "Team": team,
        "K Line": "o/u 5.5",
        "K Trend": "Steady",
        "K EV": ev['ev'],
        "Suggestion": ev['suggestion']
    }])

# ------------------------------
# Streamlit UI
# ------------------------------

st.set_page_config(page_title="MLB Parlay Picker", layout="wide")
st.title("⚾ Parlay Picker: MLB Matchups & Props")

team_choice = st.selectbox("Select a team:", list(TEAM_ABBR.keys()))

team_id = get_team_id(team_choice)
game = get_next_game(team_id)

if game:
    home_team = game['home_name']
    away_team = game['away_name']
    home_abbr = TEAM_ABBR.get(home_team, "NYY")
    away_abbr = TEAM_ABBR.get(away_team, "BOS")
    game_time = game['game_datetime']
    venue = game.get("venue", {}).get("name", "Unknown Venue")

    st.subheader(f"{away_team} @ {home_team} — {datetime.fromisoformat(game_time).strftime('%A, %B %d @ %I:%M %p')}")
    st.write(f"Venue: {venue}")

    col1, col2 = st.columns(2)
    with col1:
        st.image(get_logo_url(away_abbr), width=120)
    with col2:
        st.image(get_logo_url(home_abbr), width=120)

    # Pitchers
    away_pitcher = get_pitcher_name(game, "away")
    home_pitcher = get_pitcher_name(game, "home")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{away_team} Pitcher")
        st.dataframe(build_pitcher_table(away_team, away_pitcher), hide_index=True)
    with col2:
        st.subheader(f"{home_team} Pitcher")
        st.dataframe(build_pitcher_table(home_team, home_pitcher), hide_index=True)

    # Lineups
    away_lineup, home_lineup = get_lineups(game["game_id"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"{away_team} Lineup")
        st.dataframe(build_batter_table(away_lineup), hide_index=True)
    with col2:
        st.subheader(f"{home_team} Lineup")
        st.dataframe(build_batter_table(home_lineup), hide_index=True)

else:
    st.warning("No upcoming game found.")
