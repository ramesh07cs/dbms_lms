def create_borrow(conn, user_id, book_id, due_date):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO borrows (user_id, book_id, due_date)
            VALUES (%s, %s, %s)
            RETURNING borrow_id
        """, (user_id, book_id, due_date))
        
        result = cur.fetchone()
        # FIX: Access by key 'borrow_id', NOT [0]
        borrow_id = result['borrow_id'] if result else None
        
        # IMPORTANT: You must commit to save the new record
        conn.commit()
        return borrow_id

def get_active_borrow(conn, user_id, book_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT borrow_id
            FROM borrows
            WHERE user_id = %s 
            AND book_id = %s 
            AND borrow_status = 'ISSUED'
        """, (user_id, book_id))
        # This returns a dictionary: {'borrow_id': <id>}
        return cur.fetchone()

def return_book(conn, borrow_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE borrows
            SET return_date = CURRENT_TIMESTAMP,
                borrow_status = 'RETURNED'
            WHERE borrow_id = %s
        """, (borrow_id,))
        # IMPORTANT: You must commit to save the update
        conn.commit()