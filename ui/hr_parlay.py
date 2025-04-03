import streamlit as st
import pandas as pd
from database.connection import get_db_connection
from ui.layout import render_scorecard, team_logo_url, color_ev
from analysis.expected_value import calculate_ev
from analysis.trends import get_player_trends

def display_hr_parlay():
    st.header("💣 HR Parlay Picker")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.name, p.team, g.opponent, g.venue, g.datetime, l.line_hr
        FROM players p
        JOIN games g ON p.id = g.player_id
        JOIN lines l ON p.id = l.player_id
        WHERE g.date = DATE('now')
        AND l.line_hr IS NOT NULL
    """)
    rows = cur.fetchall()

    if not rows:
        st.info("No HR props available for today.")
        return

    table = []
    for name, team, opponent, venue, dt, line in rows:
        trends = get_player_trends(name)
        ev = calculate_ev(trends["avg_hr"], line)
        row = {
            "Player": name,
            "Team": team,
            "Opp": opponent,
            "Venue": venue,
            "Line": f"o/u {line}",
            "Trend": f'{trends["3_game_hr"]} HR in last 3',
            "EV": f'{ev*100:.1f}%',
            "Edge": color_ev(ev)
        }
        table.append(row)

    df = pd.DataFrame(table)
    st.dataframe(df, use_container_width=True)
