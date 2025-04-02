from datetime import datetime, timedelta
import statsapi
import pprint
pprint.pprint(game)
TEAM_ID = {
    'Arizona Diamondbacks': 109,
    'Atlanta Braves': 144,
    'Baltimore Orioles': 110,
    'Boston Red Sox': 111,
    'Chicago White Sox': 145,
    'Chicago Cubs': 112,
    'Cincinnati Reds': 113,
    'Cleveland Guardians': 114,
    'Colorado Rockies': 115,
    'Detroit Tigers': 116,
    'Houston Astros': 117,
    'Kansas City Royals': 118,
    'Los Angeles Angels': 108,
    'Los Angeles Dodgers': 119,
    'Miami Marlins': 146,
    'Milwaukee Brewers': 158,
    'Minnesota Twins': 142,
    'New York Yankees': 147,
    'New York Mets': 121,
    'Oakland Athletics': 133,
    'Philadelphia Phillies': 143,
    'Pittsburgh Pirates': 134,
    'San Diego Padres': 135,
    'San Francisco Giants': 137,
    'Seattle Mariners': 136,
    'St. Louis Cardinals': 138,
    'Tampa Bay Rays': 139,
    'Texas Rangers': 140,
    'Toronto Blue Jays': 141,
    'Washington Nationals': 120
}

def simplify_game(game):
    # Converts game dict into just what we need
    return statsapi.get("game", {"gamePk": game["game_id"]})

def get_game(team_name, mode="next"):
    team_id = TEAM_ID.get(team_name)
    if not team_id:
        print(f"❌ Invalid team: {team_name}")
        return None

    today = datetime.today().date()

    try:
        if mode == "next":
            start = today
            end = today + timedelta(days=10)
        else:
            start = today - timedelta(days=10)
            end = today

        games = statsapi.schedule(
            team=team_id,
            start_date=start.strftime('%Y-%m-%d'),
            end_date=end.strftime('%Y-%m-%d')
        )

        print(f"📊 {len(games)} games found for {team_name}")

        if mode == "next":
            for g in games:
                if g["status"] not in ("Postponed", "Cancelled"):
                    return statsapi.get("game", {"gamePk": g["game_id"]})
        else:
            for g in reversed(games):
                if g["status"] == "Final":
                    return statsapi.get("game", {"gamePk": g["game_id"]})

    except Exception as e:
        print(f"🔥 statsapi error: {e}")
        return None

    return None

def get_team_lineup(game_data, team_abbr):
    """
    Returns a dummy list of player names for now.
    In the future, you can replace this with real lineup extraction.
    """
    return [f"Player {i+1}" for i in range(9)]
