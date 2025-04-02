# mlb_api.py

import statsapi

TEAM_ABBR = {
    'Arizona Diamondbacks': 'ARI',
    'Atlanta Braves': 'ATL',
    'Baltimore Orioles': 'BAL',
    'Boston Red Sox': 'BOS',
    'Chicago White Sox': 'CWS',
    'Chicago Cubs': 'CHC',
    'Cincinnati Reds': 'CIN',
    'Cleveland Guardians': 'CLE',
    'Colorado Rockies': 'COL',
    'Detroit Tigers': 'DET',
    'Houston Astros': 'HOU',
    'Kansas City Royals': 'KC',
    'Los Angeles Angels': 'LAA',
    'Los Angeles Dodgers': 'LAD',
    'Miami Marlins': 'MIA',
    'Milwaukee Brewers': 'MIL',
    'Minnesota Twins': 'MIN',
    'New York Yankees': 'NYY',
    'New York Mets': 'NYM',
    'Oakland Athletics': 'OAK',
    'Philadelphia Phillies': 'PHI',
    'Pittsburgh Pirates': 'PIT',
    'San Diego Padres': 'SD',
    'San Francisco Giants': 'SF',
    'Seattle Mariners': 'SEA',
    'St. Louis Cardinals': 'STL',
    'Tampa Bay Rays': 'TB',
    'Texas Rangers': 'TEX',
    'Toronto Blue Jays': 'TOR',
    'Washington Nationals': 'WSH'
}


def get_next_game(team_name):
    """Get the next game for a team."""
    team_abbr = TEAM_ABBR.get(team_name)
    if not team_abbr:
        return None

    schedule = statsapi.schedule(team=team_abbr, start_date=None, end_date=None)
    if not schedule:
        return None

    return schedule[0]  # Return the first (next upcoming) game


def get_probable_pitchers(game):
    """Extract probable pitchers from the game dict."""
    away_pitcher = game.get('awayProbablePitcher', 'TBD')
    home_pitcher = game.get('homeProbablePitcher', 'TBD')
    return away_pitcher, home_pitcher


def get_team_lineup(game, team_abbr):
    """Return dummy lineup until real lineup API integration."""
    return [f"Player {i+1}" for i in range(9)]
