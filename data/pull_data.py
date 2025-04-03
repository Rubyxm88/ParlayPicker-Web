import requests
import pandas as pd
import datetime
from pybaseball import statcast, fangraphs_leaders

# --- DraftKings Props (via OpticOdds or similar service) ---
def fetch_draftkings_props():
    """
    Fetch player prop lines from DraftKings via a third-party API (e.g., OpticOdds).
    Replace `your_opticodds_api_key` with your actual key and confirm the endpoint.
    """
    api_key = 'your_opticodds_api_key'
    url = 'https://api.opticodds.com/sportsbooks/draftkings/props'
    headers = {'Authorization': f'Bearer {api_key}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching DraftKings props: {e}")
        return []

    props = []
    now = datetime.datetime.now()
    for item in data.get('props', []):
        props.append({
            "player": item.get("player_name"),
            "team": item.get("team_abbreviation"),
            "category": item.get("prop_category"),
            "line": item.get("prop_line"),
            "odds_over": item.get("odds_over"),
            "odds_under": item.get("odds_under"),
            "timestamp": now
        })

    return props


# --- Baseball Savant Statcast Data ---
def fetch_statcast_data(start_date, end_date):
    """
    Fetch historical Statcast data using pybaseball for a given date range.
    """
    try:
        data = statcast(start_dt=start_date, end_dt=end_date)
        return data[["player_name", "game_date", "events", "description", "launch_speed", "launch_angle"]]
    except Exception as e:
        print(f"Error fetching Statcast data: {e}")
        return pd.DataFrame()


# --- FanGraphs Advanced Stats ---
def fetch_fangraphs_stats():
    """
    Fetch advanced batting stats from FanGraphs leaderboard via pybaseball.
    """
    try:
        data = fangraphs_leaders(leaderboard='bat', season=2024, stats=['Barrel%', 'HardHit%', 'K%'], qual=100)
        return data[["Name", "Barrel%", "HardHit%", "K%"]].rename(columns={"Name": "player"})
    except Exception as e:
        print(f"Error fetching FanGraphs stats: {e}")
        return pd.DataFrame()
