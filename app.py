import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime, timedelta

# Function to fetch team ID and abbreviation
def get_team_info(team_name):
    teams = statsapi.get('teams', {'sportIds': 1})['teams']
    for team in teams:
        if team_name.lower() == team['name'].lower():
            return team['id'], team['abbreviation']
    return None, None

# Function to fetch upcoming game details
def get_next_game(team_id):
    now = datetime.now().date()
    schedule = statsapi.schedule(start_date=now, end_date=now + timedelta(days=7), team=team_id)
    if schedule:
        game = schedule[0]
        return {
            'game_time': game['game_datetime'],
            'home': game['home_name'],
            'away': game['away_name'],
            'game_id': game['game_id']
        }
    return None

# Function to fetch probable pitchers
def get_probable_pitchers(game_id):
    boxscore = statsapi.boxscore_data(game_id)
    pitchers = {'home': 'TBD', 'away': 'TBD'}
    for team in ['home', 'away']:
        try:
            pitchers[team] = boxscore['teamInfo'][team]['probablePitcher']['fullName']
        except KeyError:
            continue
    return pitchers

# Function to fetch team lineup
def get_team_lineup(game_id, team_type):
    lineup = []
    try:
        game_data = statsapi.get('game', {'gamePk': game_id})
        for player in game_data['gameData']['players'].values():
            if player['parentTeamId'] == game_data['gameData']['teams'][team_type]['id'] and player['gameStatus']['isStarter']:
                lineup.append(player['fullName'])
    except KeyError:
        pass
    return lineup

# Function to calculate player trends and expected value (EV)
def calculate_player_ev(player_name, stat_type):
    # Placeholder function: Implement your logic to calculate trends and EV based on historical data
    # For example, analyze past performance against similar pitchers, recent form, etc.
    return {
        'line': 'o/u 0.5',
        'trend': 'Steady',
        'ev': '+5%',
        'suggestion': 'Over'
    }

# Streamlit UI
st.title("MLB Matchup Analysis")

team_name = st.selectbox("Select a team:", [team['name'] for team in statsapi.get('teams', {'sportIds': 1})['teams']])

if team_name:
    team_id, team_abbr = get_team_info(team_name)
    if team_id:
        game = get_next_game(team_id)
        if game:
            st.subheader(f"Upcoming Game: {game['away']} at {game['home']}")
            st.write(f"Game Time: {game['game_time']}")

            # Display team logos
            home_logo = f"https://www.mlbstatic.com/team-logos/{get_team_info(game['home'])[0]}.svg"
            away_logo = f"https://www.mlbstatic.com/team-logos/{get_team_info(game['away'])[0]}.svg"
            st.image([away_logo, home_logo], width=150)

            pitchers = get_probable_pitchers(game['game_id'])
            st.write(f"Probable Pitchers: {game['away']} - {pitchers['away']}, {game['home']} - {pitchers['home']}")

            # Display lineups and player props
            for team, lineup in [('away', get_team_lineup(game['game_id'], 'away')), ('home', get_team_lineup(game['game_id'], 'home'))]:
                st.subheader(f"{game[team]} Lineup")
                df = pd.DataFrame(columns=['Player', 'HR Line', 'HR Trend', 'HR EV', 'HR Suggestion',
                                           'Hits Line', 'Hits Trend', 'Hits EV', 'Hits Suggestion',
                                           'RBI Line', 'RBI Trend', 'RBI EV', 'RBI Suggestion'])
                for player in lineup:
                    hr_ev = calculate_player_ev(player, 'home_runs')
                    hits_ev = calculate_player_ev(player, 'hits')
                    rbi_ev = calculate_player_ev(player, 'rbi')
                    df = df.append({
                        'Player': player,
                        'HR Line': hr_ev['line'], 'HR Trend': hr_ev['trend'], 'HR EV': hr_ev['ev'], 'HR Suggestion': hr_ev['suggestion'],
                        'Hits Line': hits_ev['line'], 'Hits Trend': hits_ev['trend'], 'Hits EV': hits_ev['ev'], 'Hits Suggestion': hits_ev['suggestion'],
                        'RBI Line': rbi_ev['line'], 'RBI Trend': rbi_ev['trend'], 'RBI EV': rbi_ev['ev'], 'RBI Suggestion': rbi_ev['suggestion']
                    }, ignore_index=True)
                st.dataframe(df)

        else:
            st.write("No upcoming games found.")
    else:
        st.write("Team not found.")
