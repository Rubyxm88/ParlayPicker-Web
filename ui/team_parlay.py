import streamlit as st
import pandas as pd
from database.connection import get_db_connection
from ui.layout import render_scorecard, color_ev, team_logo_url
from analysis.trends import get_player_trends
from analysis.expected_value import calculate_ev
from datetime import datetime

def show_team_parlay():
    st.header("🧢 Team Matchups & Props")

    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch today's games
    cur.execute("""
        SELECT DISTINCT game_id, team, opponent, venue, datetime, status, team_score, opp_score
        FROM games
        WHERE DATE(datetime) = DATE('now')
    """)
    games = cur.fetchall()

    if not games:
        st.info("No games scheduled today.")
        return

    for game_id, team, opp, venue, dt, status, team_score, opp_score in games:
        logo_url = team_logo_url(team)
        opp_logo = team_logo_url(opp)
        game_time = datetime.fromisoformat(dt).strftime('%I:%M %p')

        # Scorecard
        render_scorecard(
            team=team,
            team_score=team_score,
            opponent=opp,
            opponent_score=opp_score,
            time=game_time,
            venue=venue,
            status=status,
            team_logo=logo_url,
            opponent_logo=opp_logo
        )

        # Fetch player lines
        cur.execute("""
            SELECT p.name, l.line_hr, l.line_hits, l.line_rbi, t.avg_hr, t.avg_hits, t.avg_rbi
            FROM players p
            JOIN lines l ON p.id = l.player_id
            JOIN trends t ON p.id = t.player_id
            WHERE p.team = ?
        """, (team,))
        players = cur.fetchall()

        if players:
            data = []
            for name, hr_line, hits_line, rbi_line, avg_hr, avg_hits, avg_rbi in players:
                row = {
                    "Player": name
                }
                if hr_line:
                    ev = calculate_ev(avg_hr, hr_line)
                    row.update({
                        "HR Line": f"o/u {hr_line}",
                        "HR EV": f'{ev*100:.1f}%',
                        "HR Edge": color_ev(ev)
                    })
                if hits_line:
                    ev = calculate_ev(avg_hits, hits_line)
                    row.update({
                        "Hits Line": f"o/u {hits_line}",
                        "Hits EV": f'{ev*100:.1f}%',
                        "Hits Edge": color_ev(ev)
                    })
                if rbi_line:
                    ev = calculate_ev(avg_rbi, rbi_line)
                    row.update({
                        "RBI Line": f"o/u {rbi_line}",
                        "RBI EV": f'{ev*100:.1f}%',
                        "RBI Edge": color_ev(ev)
                    })

                data.append(row)

            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.write("No prop data found for this game.")
__all__ = ["show_team_parlay"]
