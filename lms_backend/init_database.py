import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def init_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    with open("database/schema.sql", "r") as f:
        sql = f.read()

    with conn.cursor() as cur:
        cur.execute(sql)

    conn.commit()
    conn.close()

    print("✅ Tables created successfully!")

if __name__ == "__main__":
    init_db()
