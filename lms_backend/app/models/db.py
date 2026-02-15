import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g
from app.config import Config


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            cursor_factory=RealDictCursor
        )
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
