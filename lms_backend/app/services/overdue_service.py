def mark_overdue_borrows(conn):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE borrows
            SET borrow_status = 'OVERDUE'
            WHERE borrow_status = 'BORROWED'
              AND due_date < NOW()
        """)
    conn.commit()
