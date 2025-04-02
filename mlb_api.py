# mlb_api.py

from datetime import datetime, timedelta
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
        print(f"[DEBUG] Invalid team: {team_name}")
        return None

    today = datetime.utcnow().date()  # Use UTC to avoid timezone issues
    future = today + timedelta(days=7)

    print(f"[DEBUG] Checking schedule for {team_name} (ID: {team_id}) from {today} to {future}")

    schedule = statsapi.schedule(team=team_id, start_date=str(today), end_date=str(future))

    print(f"[DEBUG] Schedule returned {len(schedule)} games")

    for game in schedule:
        print(f"[DEBUG] Game found: {game['game_date']} vs {game['opponent_name']} - Status: {game['status']}")
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
