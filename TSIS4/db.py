import psycopg2
from datetime import datetime

class Database:
    def __init__(self):
        # Укажи свои данные подключения
        self.conn = psycopg2.connect(
            dbname="snake_db",
            user="postgres",
            password="apple13",
            host="localhost"
        )
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        self.conn.commit()

    def get_or_create_player(self, username):
        self.cursor.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        return self.cursor.fetchone()[0]

    def save_session(self, player_id, score, level):
        self.cursor.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )
        self.conn.commit()

    def get_top_10(self):
        self.cursor.execute("""
            SELECT p.username, s.score, s.level_reached, s.played_at 
            FROM game_sessions s JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10
        """)
        return self.cursor.fetchall()

    def get_personal_best(self, player_id):
        self.cursor.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
        result = self.cursor.fetchone()[0]
        return result if result else 0