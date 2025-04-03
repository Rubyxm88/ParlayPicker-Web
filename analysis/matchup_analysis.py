import sqlite3
from datetime import datetime

def get_matchup_score(db_path, batter_id, pitcher_id, stadium):
    """
    Returns a matchup score (0–100) based on:
    - Batter vs Pitcher historic performance
    - Batter vs Pitcher hand split
    - Park factor for HR, hits, etc.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Batter vs pitcher history
    cursor.execute("""
        SELECT at_bats, hits, home_runs
        FROM batter_vs_pitcher
        WHERE batter_id = ? AND pitcher_id = ?
    """, (batter_id, pitcher_id))
    result = cursor.fetchone()
    if result:
        ab, hits, hrs = result
        if ab > 0:
            hit_rate = hits / ab
            hr_rate = hrs / ab
        else:
            hit_rate = hr_rate = 0
    else:
        hit_rate = hr_rate = 0

    # Batter split vs pitcher hand
    cursor.execute("""
        SELECT pitcher_hand FROM players
        WHERE player_id = ?
    """, (pitcher_id,))
    pitcher_hand = cursor.fetchone()
    if pitcher_hand:
        pitcher_hand = pitcher_hand[0]

        cursor.execute("""
            SELECT AVG(HR), AVG(Hits)
            FROM player_logs
            WHERE player_id = ? AND pitcher_hand = ?
        """, (batter_id, pitcher_hand))
        split_hr, split_hits = cursor.fetchone()
    else:
        split_hr = split_hits = 0

    # Park factor boost
    cursor.execute("""
        SELECT hr_factor, hits_factor
        FROM park_factors
        WHERE stadium = ?
    """, (stadium,))
    row = cursor.fetchone()
    hr_boost = row[0] if row else 1.0
    hits_boost = row[1] if row else 1.0

    # Weighted average score (simplified logic)
    score = (
        (hit_rate * 30) +
        (hr_rate * 50) +
        (split_hr or 0) * 10 +
        (split_hits or 0) * 5 +
        (hr_boost - 1.0) * 25 +
        (hits_boost - 1.0) * 10
    )

    conn.close()
    return round(min(max(score, 0), 100), 2)  # Clamp between 0–100
