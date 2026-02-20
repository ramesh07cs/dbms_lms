from psycopg2.extras import RealDictCursor


def get_approved_users_for_borrow(conn):
    """Returns approved students and teachers for admin issue dropdown."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT u.user_id, u.name, u.email, r.role_name
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            WHERE u.status = 'APPROVED' AND u.role_id IN (2, 3)
            ORDER BY u.name
        """)
        return cur.fetchall()


def get_students_for_borrow(conn):
    """Returns approved students only (for teacher issue dropdown)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT u.user_id, u.name, u.email, r.role_name
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            WHERE u.status = 'APPROVED' AND u.role_id = 3
            ORDER BY u.name
        """)
        return cur.fetchall()


def get_pending_users(conn):
    """Returns list of users with status PENDING."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT u.user_id, u.name, u.email, u.phone, u.role_id, u.status, u.created_at,
                   r.role_name
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            WHERE u.status = 'PENDING'
            ORDER BY u.created_at ASC
        """)
        return cur.fetchall()


def create_user(conn, name, email, password_hash, role_id, phone=None):
    """
    Inserts user into database and returns new user_id
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (name, email, password, role_id, phone)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING user_id
        """, (name, email, password_hash, role_id, phone))

        result = cur.fetchone()

        if result:
            return result["user_id"]
        return None


def get_user_by_email(conn, email):
    """
    Returns user dictionary by email
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT user_id, name, email, password, role_id, status
            FROM users
            WHERE email = %s
        """, (email,))
        return cur.fetchone()


def get_user_by_id(conn, user_id):
    """
    Returns user dictionary by user_id
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT user_id, name, email, phone, role_id, status
            FROM users
            WHERE user_id = %s
        """, (user_id,))
        return cur.fetchone()


def get_all_users(conn):
    """Returns all users with role name (for admin User Management)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT u.user_id, u.name, u.email, u.phone, u.status, u.created_at,
                   r.role_name, u.role_id
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            ORDER BY u.name
        """)
        return cur.fetchall()


def get_teachers_and_students(conn):
    """Returns teachers and students only (for teacher View Users)."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT u.user_id, u.name, u.email, u.phone, u.status,
                   r.role_name, u.role_id
            FROM users u
            JOIN roles r ON u.role_id = r.role_id
            WHERE u.role_id IN (2, 3)
            ORDER BY r.role_name, u.name
        """)
        return cur.fetchall()


def delete_user(conn, user_id):
    """Delete a user by id. Caller must ensure no critical dependencies."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))


def update_user_status(conn, user_id, status, approved_by=None):
    """
    Updates user approval status
    """
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE users
            SET status = %s,
                approved_by = %s,
                approved_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (status, approved_by, user_id))
