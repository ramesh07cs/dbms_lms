# app/models/db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g
from app.config import Config

def get_db():
    """
    Returns a PostgreSQL connection stored in Flask's g.
    Uses DATABASE_URL from Config for connection.
    Ensures RealDictCursor is used for dictionary-style rows.
    """
    if "db" not in g:
        try:
            g.db = psycopg2.connect(
                dsn=Config.DATABASE_URL,
                cursor_factory=RealDictCursor  # ✅ fetch returns dict
            )
        except Exception as e:
            print("Database connection error:", e)
            raise e
    return g.db  # ✅ return actual connection

def close_db(e=None):
    """
    Closes the PostgreSQL connection at the end of request.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()
