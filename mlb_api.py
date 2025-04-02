from datetime import datetime, timedelta
import statsapi

TEAM_ABBR = {
    'Arizona Diamondbacks': 'ARI', 'Atlanta Braves': 'ATL', 'Baltimore Orioles': 'BAL',
    'Boston Red Sox': 'BOS', 'Chicago White Sox': 'CWS', 'Chicago Cubs': 'CHC',
    'Cincinnati Reds': 'CIN', 'Cleveland Guardians': 'CLE', 'Colorado Rockies': 'COL',
    'Detroit Tigers': 'DET', 'Houston Astros': 'HOU', 'Kansas City Royals': 'KC',
    'Los Angeles Angels': 'LAA', 'Los Angeles Dodgers': 'LAD', 'Miami Marlins': 'MIA',
    'Milwaukee Brewers': 'MIL', 'Minnesota Twins': 'MIN', 'New York Yankees': 'NYY',
    'New York Mets': 'NYM', 'Oakland Athletics': 'OAK', 'Philadelphia Phillies': 'PHI',
    'Pittsburgh Pirates': 'PIT', 'San Diego Padres': 'SD', 'San Francisco Giants': 'SF',
    'Seattle Mariners': 'SEA', 'St. Louis Cardinals': 'STL', 'Tampa Bay Rays': 'TB',
    'Texas Rangers': 'TEX', 'Toronto Blue Jays': 'TOR', 'Washington Nationals': 'WSH'
}

# Map team name to team ID (from official MLB Stats API)
TEAM_IDS = {team['name']: team['id'] for team in statsapi.get('teams', {'sportIds': 1})['teams']}

def get_game(team_name, mode="next"):
    """Fetch full game data for next or last game using game_id."""
    team_id = TEAM_IDS.get(team_name)
    if not team_id:
        return None

    today = datetime.now().date()
    try:
        if mode == "next":
            future = today + timedelta(days=7)
            games = statsapi.schedule(team=team_id, start_date=str(today), end_date=str(future))
            for g in games:
                if g['status'] not in ['Final', 'Postponed']:
                    return statsapi.get("game", {"gamePk": g["game_id"]})
        else:
            past = today - timedelta(days=7)
            games = statsapi.schedule(team=team_id, start_date=str(past), end_date=str(today))
            for g in reversed(games):
                if g['status'] in ['Final']:
                    return statsapi.get("game", {"gamePk": g["game_id"]})
    except Exception as e:
        print("Error fetching game data:", e)
    return None


def get_team_lineup(game, team_abbr):
    """Return dummy lineup until real lineup API integration."""
    return [f"Player {i+1}" for i in range(9)]
