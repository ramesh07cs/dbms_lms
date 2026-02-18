import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # ==========================
    # Secret Keys
    # ==========================
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-super-secret-key")

    # ==========================
    # JWT Configuration
    # ==========================
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # default 1 hour
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30))  # default 30 days
    )

    # ==========================
    # Database
    # ==========================
    # Do not provide a non-Postgres default. Require users to set DATABASE_URL
    # in their environment (e.g., in a .env file). This avoids passing invalid
    # DSNs to psycopg2 when the app expects PostgreSQL.
    DATABASE_URL = os.getenv("DATABASE_URL")
