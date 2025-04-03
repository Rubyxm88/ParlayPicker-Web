-- Player information (batters and pitchers)
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    name TEXT,
    team TEXT,
    position TEXT,
    is_pitcher INTEGER
);

-- Games table
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY,
    game_date TEXT,
    home_team TEXT,
    away_team TEXT,
    venue TEXT,
    status TEXT,
    home_score INTEGER,
    away_score INTEGER
);

-- Player game logs (box score-style performance)
CREATE TABLE IF NOT EXISTS player_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    game_id INTEGER,
    team TEXT,
    opponent TEXT,
    is_home INTEGER,
    at_bats INTEGER,
    hits INTEGER,
    home_runs INTEGER,
    rbis INTEGER,
    strikeouts INTEGER,
    walks INTEGER,
    result TEXT,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Betting lines for props
CREATE TABLE IF NOT EXISTS betting_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    game_id INTEGER,
    stat_type TEXT,         -- 'HR', 'Hits', 'RBI', 'Ks', etc
    sportsbook TEXT,        -- 'DraftKings', etc
    line REAL,              -- e.g., 0.5, 1.5
    over_odds INTEGER,
    under_odds INTEGER,
    retrieved_at TEXT,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
);

-- Calculated trend data for players
CREATE TABLE IF NOT EXISTS player_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    stat_type TEXT,
    season_avg REAL,
    last_10_avg REAL,
    last_3_avg REAL,
    trend_direction TEXT,      -- 'hot', 'cold', 'steady'
    trend_strength REAL,       -- % change from baseline
    updated_at TEXT,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
