import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def init_db():
    try:
        # Prefer using the application's Config if available
        try:
            from app.config import Config
            database_url = Config.DATABASE_URL
        except Exception:
            database_url = os.getenv("DATABASE_URL")

        if database_url:
            conn = psycopg2.connect(dsn=database_url)
        else:
            host = os.getenv("DB_HOST")
            database = os.getenv("DB_NAME")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            port = os.getenv("DB_PORT") or "5432"

            missing = [name for name, val in (("DB_HOST", host), ("DB_NAME", database), ("DB_USER", user), ("DB_PASSWORD", password)) if not val]
            if missing:
                print("Missing required database environment variables:", ", ".join(missing))
                print("Provide a `DATABASE_URL` (recommended) or set DB_HOST/DB_NAME/DB_USER/DB_PASSWORD.")
                print("Example: DATABASE_URL=postgresql://user:pass@host:5432/dbname")
                sys.exit(1)

            conn = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port,
            )

        # Load schema relative to this file so script works from any cwd
        base_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(base_dir, "database", "schema.sql")
        if not os.path.exists(schema_path):
            # Fallback to repository-relative path
            schema_path = os.path.join(os.path.dirname(base_dir), "database", "schema.sql")

        if not os.path.exists(schema_path):
            print("Could not find database/schema.sql. Checked:", schema_path)
            sys.exit(1)

        with open(schema_path, "r") as f:
            sql = f.read()

        with conn.cursor() as cur:
            cur.execute(sql)

        conn.commit()
        conn.close()

        print("✅ Tables created successfully!")

    except Exception as e:
        print("Failed to initialize database:", e)
        sys.exit(1)


if __name__ == "__main__":
    init_db()
