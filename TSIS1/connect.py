import psycopg2
from config import params

def get_connection():
    conn = psycopg2.connect(**params)
    conn.set_client_encoding('UTF8')
    return conn

def create_tables():
    pass