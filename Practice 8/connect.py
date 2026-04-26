import psycopg2
from config import params

def get_connection():
    return psycopg2.connect(**params)

def create_tables():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    phone VARCHAR(20) UNIQUE
                )
            """)
        conn.commit()