import sqlite3
from datetime import datetime
import numpy as np

def calculate_trends(db_path, stat_type):
    """
    Calculates trends for all players based on stat_type (e.g., HR, Hits, RBI, Ks).
    Stores results in player_trends table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all unique players who have logs for this stat
    cursor.execute(f"""
        SELECT DISTINCT player_id FROM player_logs
        WHERE {stat_type} IS NOT NULL
    """)
    player_ids = [row[0] for row in cursor.fetchall()]

    for player_id in player_ids:
        cursor.execute(f"""
            SELECT {stat_type}
            FROM player_logs
            WHERE player_id = ?
            ORDER BY game_id DESC
            LIMIT 30
        """, (player_id,))
        values = [row[0] for row in cursor.fetchall() if row[0] is not None]

        if len(values) < 5:
            continue  # Not enough data

        season_avg = np.mean(values)
        last_10_avg = np.mean(values[:10])
        last_3_avg = np.mean(values[:3])

        # Compare last 3 to season average to determine trend
        pct_change = ((last_3_avg - season_avg) / season_avg) * 100
        if pct_change > 15:
            direction = "hot"
        elif pct_change < -15:
            direction = "cold"
        else:
            direction = "steady"

        # Upsert trend
        cursor.execute("""
            INSERT INTO player_trends (player_id, stat_type, season_avg, last_10_avg, last_3_avg, trend_direction, trend_strength, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(player_id, stat_type) DO UPDATE SET
                season_avg=excluded.season_avg,
                last_10_avg=excluded.last_10_avg,
                last_3_avg=excluded.last_3_avg,
                trend_direction=excluded.trend_direction,
                trend_strength=excluded.trend_strength,
                updated_at=excluded.updated_at
        """, (
            player_id,
            stat_type,
            round(season_avg, 3),
            round(last_10_avg, 3),
            round(last_3_avg, 3),
            direction,
            round(pct_change, 2),
            datetime.utcnow().isoformat()
        ))

    conn.commit()
    conn.close()
