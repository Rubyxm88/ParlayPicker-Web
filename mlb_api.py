# mlb_api.py
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

def get_game(team_name, mode="next"):
    """Get next or last game for given team name."""
    abbr = TEAM_ABBR.get(team_name)
    if not abbr:
        return None

    today = datetime.now().date()

    if mode == "next":
        future = today + timedelta(days=7)
        games = statsapi.schedule(team=abbr, start_date=str(today), end_date=str(future))
        for game in games:
            if game['status'] not in ['Final', 'Postponed']:
                return game
    else:
        past = today - timedelta(days=7)
        games = statsapi.schedule(team=abbr, start_date=str(past), end_date=str(today))
        for game in reversed(games):
            if game['status'] in ['Final']:
                return game
    return None

def get_team_lineup(game, team_abbr):
    """Return dummy lineup until real lineup API integration."""
    return [f"Player {i+1}" for i in range(9)]
