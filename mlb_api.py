# mlb_api.py

import statsapi

def get_next_game(team_abbr):
    schedule = statsapi.schedule(team=team_abbr, start_date=None, end_date=None)
    if not schedule:
        return None
    return schedule[0]  # Return next game

def get_team_lineup(game, team_abbr):
    # Dummy fallback until we pull actual MLB lineups
    return [f"Player {i+1}" for i in range(9)]
