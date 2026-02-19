# app/models/audit_queries.py
from psycopg2.extras import RealDictCursor


def get_audit_logs(conn, limit=20, offset=0):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT *
            FROM audit_logs
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        return cur.fetchall()
