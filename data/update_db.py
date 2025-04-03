import pandas as pd
from data.pull_data import fetch_draftkings_props, fetch_statcast_data, fetch_fangraphs_stats
from database.connection import get_db_connection
from datetime import datetime, timedelta

def update_props_table():
    conn = get_db_connection()
    props = fetch_draftkings_props()

    for prop in props:
        conn.execute("""
            INSERT OR REPLACE INTO player_props (player, team, category, line, odds_over, odds_under, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            prop["player"], prop["team"], prop["category"],
            prop["line"], prop["odds_over"], prop["odds_under"],
            prop["timestamp"]
        ))
    conn.commit()
    conn.close()


def update_statcast_table(start_days_ago=30):
    conn = get_db_connection()
    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=start_days_ago)

    df = fetch_statcast_data(start_date, end_date)

    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO game_logs (player, date, HR, Hits, RBI)
            VALUES (?, ?, ?, ?, ?)
        """, (
            row["player"], row["date"], row["HR"], row["Hits"], row["RBI"]
        ))
    conn.commit()
    conn.close()


def update_fangraphs_table():
    conn = get_db_connection()
    df = fetch_fangraphs_stats()

    for _, row in df.iterrows():
        conn.execute("""
            INSERT OR REPLACE INTO advanced_stats (player, BarrelPct, HardHitPct, KPct)
            VALUES (?, ?, ?, ?)
        """, (
            row["player"], row["Barrel%"], row["HardHit%"], row["K%"]
        ))
    conn.commit()
    conn.close()
