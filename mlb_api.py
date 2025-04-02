# mlb_api.py

from datetime import datetime, timedelta
import statsapi


TEAM_IDS = {
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


def get_next_game(team_name):
    """Get the next scheduled game for the team."""
    team_id = TEAM_IDS.get(team_name)
    if not team_id:
        return None

    today = datetime.now().date()
    future = today + timedelta(days=7)

    schedule = statsapi.schedule(team=team_id, start_date=str(today), end_date=str(future))

    for game in schedule:
        if game['status'] not in ('Final', 'Postponed'):
            return game

    return None




def get_probable_pitchers(game):
    """Extract probable pitchers from the game dict."""
    away_pitcher = game.get('awayProbablePitcher', 'TBD')
    home_pitcher = game.get('homeProbablePitcher', 'TBD')
    return away_pitcher, home_pitcher


def get_team_lineup(game, team_abbr):
    """Return dummy lineup until real lineup API integration."""
    return [f"Player {i+1}" for i in range(9)]
