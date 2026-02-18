from psycopg2.extras import RealDictCursor

def create_borrow(conn, user_id, book_id, due_date):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            INSERT INTO borrows (user_id, book_id, due_date, borrow_status)
            VALUES (%s, %s, %s, 'ISSUED')
            RETURNING borrow_id
        """, (user_id, book_id, due_date))
        result = cur.fetchone()
        if not result:
            return None
        return result['borrow_id']
        


def get_active_borrow(conn, user_id, book_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT borrow_id, user_id, book_id, due_date, borrow_status
            FROM borrows
            WHERE user_id = %s
              AND book_id = %s
              AND borrow_status = 'ISSUED'
        """, (user_id, book_id))
        return cur.fetchone()


def return_book_record(conn, borrow_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            UPDATE borrows
            SET return_date = CURRENT_TIMESTAMP,
                borrow_status = 'RETURNED'
            WHERE borrow_id = %s
        """, (borrow_id,))
