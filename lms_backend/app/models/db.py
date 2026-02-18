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
        # Ensure a DATABASE_URL is configured before attempting connection
        if not Config.DATABASE_URL:
            raise RuntimeError(
                "DATABASE_URL is not configured. Set DATABASE_URL in your environment or .env file."
            )
        try:
            g.db = psycopg2.connect(
                dsn=Config.DATABASE_URL,
                cursor_factory=RealDictCursor
            )
        except Exception as e:
            print("Database connection error:", e)
            raise e
    return g.db

def close_db(e=None):
    """
    Closes the PostgreSQL connection at the end of request.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()
