# app/models/user_queries.py

def create_user(conn, name, email, password_hash, role_id):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (name, email, password, role_id)
            VALUES (%s, %s, %s, %s)
            RETURNING user_id
        """, (name, email, password_hash, role_id))
        return cur.fetchone()[0]


def get_user_by_email(conn, email):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT user_id, name, email, password, role_id, status
            FROM users
            WHERE email = %s
        """, (email,))
        return cur.fetchone()


def get_user_by_id(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT user_id, name, email, role_id, status
            FROM users
            WHERE user_id = %s
        """, (user_id,))
        return cur.fetchone()


def update_user_status(conn, user_id, status, approved_by=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE users
            SET status = %s,
                approved_by = %s,
                approved_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (status, approved_by, user_id))
