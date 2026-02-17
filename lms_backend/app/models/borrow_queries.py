def create_borrow(conn, user_id, book_id, due_date):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO borrows (user_id, book_id, due_date)
            VALUES (%s, %s, %s)
            RETURNING borrow_id
        """, (user_id, book_id, due_date))

        result = cur.fetchone()
        return result['borrow_id'] if result else None


def get_active_borrow(conn, user_id, book_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT borrow_id
            FROM borrows
            WHERE user_id = %s 
            AND book_id = %s 
            AND borrow_status = 'ISSUED'
        """, (user_id, book_id))

        return cur.fetchone()


def return_book_record(conn, borrow_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE borrows
            SET return_date = CURRENT_TIMESTAMP,
                borrow_status = 'RETURNED'
            WHERE borrow_id = %s
        """, (borrow_id,))
