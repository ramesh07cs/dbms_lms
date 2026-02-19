# app/models/audit_queries.py

def get_audit_logs(conn, limit=20, offset=0):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM audit_logs
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        return cur.fetchall()
