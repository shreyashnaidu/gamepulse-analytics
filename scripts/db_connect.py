import psycopg2
<<<<<<< HEAD
from psycopg2.extras import RealDictCursor

=======
>>>>>>> 1477db6

def get_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        database="gamepulse",
        user="postgres",
        password="0805",
<<<<<<< HEAD
        port="5432",
        cursor_factory=RealDictCursor
=======
        port="5432"
>>>>>>> 1477db6
    )