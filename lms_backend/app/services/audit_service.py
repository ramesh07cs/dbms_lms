def log_action(conn, user_id, action, table_name=None, record_id=None, description=None):
    """
    Insert audit log entry.
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, action, table_name, record_id, description))
