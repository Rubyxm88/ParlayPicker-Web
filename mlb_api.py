from datetime import datetime, timedelta
import statsapi
from requests.exceptions import HTTPError

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
    abbr = TEAM_ABBR.get(team_name)
    if not abbr:
        return None

    today = datetime.today().date()

    if mode == "next":
        start_date = today
        end_date = today + timedelta(days=7)
    else:
        start_date = today - timedelta(days=7)
        end_date = today

    try:
        games = statsapi.schedule(
            team=abbr,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
    except HTTPError as e:
        print(f"⚠️ statsapi.schedule() failed for {abbr}: {e}")
        return None

    # Get first non-final (next game) or last final (last game)
    if mode == "next":
        for game in games:
            if game['status'] not in ('Final', 'Postponed'):
                return simplify_game(game)
    else:
        for game in reversed(games):
            if game['status'] == 'Final':
                return simplify_game(game)

    return None


def simplify_game(game):
    return {
        "home_name": game["home_name"],
        "away_name": game["away_name"],
        "home_abbr": TEAM_ABBR.get(game["home_name"], ""),
        "away_abbr": TEAM_ABBR.get(game["away_name"], ""),
        "game_date": game["game_datetime"],
        "venue_name": game.get("venue", "Unknown Venue")
    }


def get_team_lineup(game, team_abbr):
    # Placeholder for actual lineup integration
    return [f"Player {i+1}" for i in range(9)]
