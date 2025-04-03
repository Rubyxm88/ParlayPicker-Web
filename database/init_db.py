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

    conn.commit()
    conn.close()
