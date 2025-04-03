import requests
import pandas as pd
from datetime import datetime

def fetch_draftkings_props():
    """
    Simulated HR/Hits/RBI props with realistic structure for development/testing.
    """
    now = datetime.now().isoformat()

    return [
        {
            "player": "Aaron Judge",
            "team": "NYY",
            "category": "HR",
            "line": 0.5,
            "odds_over": -110,
            "odds_under": -110,
            "timestamp": now
        },
        {
            "player": "Aaron Judge",
            "team": "NYY",
            "category": "Hits",
            "line": 1.5,
            "odds_over": -105,
            "odds_under": -115,
            "timestamp": now
        },
        {
            "player": "Aaron Judge",
            "team": "NYY",
            "category": "RBI",
            "line": 0.5,
            "odds_over": +100,
            "odds_under": -120,
            "timestamp": now
        }
    ]

def fetch_statcast_data(start_date, end_date):
    """
    Simulated Statcast logs: player, date, HR, Hits, RBI
    """
    return pd.DataFrame([
        {"player": "Aaron Judge", "date": "2025-04-01", "HR": 1, "Hits": 2, "RBI": 1},
        {"player": "Aaron Judge", "date": "2025-04-02", "HR": 0, "Hits": 1, "RBI": 0},
        {"player": "Aaron Judge", "date": "2025-04-03", "HR": 2, "Hits": 3, "RBI": 3},
    ])

def fetch_fangraphs_stats():
    """
    Simulated advanced stats from FanGraphs.
    """
    return pd.DataFrame([
        {"player": "Aaron Judge", "Barrel%": 18.3, "HardHit%": 52.1, "K%": 24.8}
    ])
