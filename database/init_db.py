from database.connection import get_db_connection

def initialize_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            game_id TEXT,
            team TEXT,
            opponent TEXT,
            venue TEXT,
            datetime TEXT,
            status TEXT,
            team_score INTEGER,
            opp_score INTEGER,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            line_hr REAL,
            line_hits REAL,
            line_rbi REAL,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            avg_hr REAL,
            avg_hits REAL,
            avg_rbi REAL,
            FOREIGN KEY(player_id) REFERENCES players(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS player_props (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            team TEXT,
            category TEXT,
            line REAL,
            odds_over REAL,
            odds_under REAL,
            timestamp TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            date TEXT,
            HR INTEGER,
            Hits INTEGER,
            RBI INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS advanced_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT,
            BarrelPct REAL,
            HardHitPct REAL,
            KPct REAL
        )
    """)



    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_tables()
