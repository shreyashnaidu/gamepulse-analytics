import psycopg2
from psycopg2.extras import RealDictCursor


def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        database="gamepulse",
        user="postgres",
        password="0805",
        port="5432",
        cursor_factory=RealDictCursor
    )