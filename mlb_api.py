import requests
from datetime import datetime, timedelta

def get_team_id(team_name):
    url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    response = requests.get(url).json()
    for team in response['teams']:
        if team_name.lower() in team['name'].lower():
            return team['id'], team['abbreviation']
    return None, None

def get_next_game(team_name):
    team_id, abbr = get_team_id(team_name)
    if not team_id:
        return None

    now = datetime.now().date()
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?teamId={team_id}&sportId=1&startDate={now}&endDate={now + timedelta(days=7)}"
    schedule = requests.get(schedule_url).json()
    if not schedule['dates']:
        return None

    game = schedule['dates'][0]['games'][0]
    game_info = {
        'game_time': game['gameDate'],
        'home': game['teams']['home']['team']['name'],
        'away': game['teams']['away']['team']['name'],
        'venue': game['venue']['name'],
        'game_id': game['gamePk']
    }
    return game_info

def get_probable_pitchers(game_id):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore"
    res = requests.get(url).json()
    pitchers = {'home': 'TBD', 'away': 'TBD'}
    for team in ['home', 'away']:
        try:
            info = res['teams'][team]['info']
            for i in info:
                if 'Starting Pitcher' in i['field']:
                    pitchers[team] = i['value']
        except:
            continue
    return pitchers
