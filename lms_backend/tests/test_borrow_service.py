from datetime import datetime, timedelta

from app.services.borrow_service import issue_book, return_borrowed_book


class DummyConn:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    # provide a minimal cursor context manager for compatibility if needed
    class _Cur:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def execute(self, *args, **kwargs):
            pass

        def fetchone(self):
            return None

    def cursor(self, *args, **kwargs):
        return DummyConn._Cur()


def test_issue_book_happy_path(monkeypatch):
    conn = DummyConn()

    # Monkeypatch dependencies
    monkeypatch.setattr('app.services.borrow_service.expire_overdue_reservations', lambda c: None)
    monkeypatch.setattr('app.services.borrow_service.get_book_by_id', lambda c, bid: {'book_id': bid, 'available_copies': 3})
    monkeypatch.setattr('app.services.borrow_service.get_active_borrow', lambda c, uid, bid: None)
    monkeypatch.setattr('app.services.borrow_service.update_book_copies', lambda c, bid, n: None)
    monkeypatch.setattr('app.services.borrow_service.create_borrow', lambda c, uid, bid, due: 101)
    monkeypatch.setattr('app.services.borrow_service.log_action', lambda *a, **k: None)

    borrow_id = issue_book(conn, user_id=10, book_id=5)

    assert borrow_id == 101
    assert conn.committed is True


def test_return_borrow_with_fine_and_auto_assign(monkeypatch):
    conn = DummyConn()

    # Setup active borrow returned by DAO
    past_due = datetime.utcnow() - timedelta(days=5)
    monkeypatch.setattr('app.services.borrow_service.get_active_borrow', lambda c, uid, bid: {'borrow_id': 200, 'due_date': past_due})
    monkeypatch.setattr('app.services.borrow_service.calculate_fine', lambda due, ret: 25)
    monkeypatch.setattr('app.services.borrow_service.return_book_record', lambda c, bid: None)
    monkeypatch.setattr('app.services.borrow_service.get_book_by_id', lambda c, bid: {'book_id': bid, 'available_copies': 2})
    monkeypatch.setattr('app.services.borrow_service.update_book_copies', lambda c, bid, n: None)
    monkeypatch.setattr('app.services.borrow_service.create_fine', lambda c, bid, uid, amt: 42)

    # Reservation exists and leads to auto-assign
    monkeypatch.setattr('app.services.borrow_service.get_oldest_active_reservation', lambda c, bid: {'reservation_id': 7, 'user_id': 55})
    monkeypatch.setattr('app.services.borrow_service.create_borrow', lambda c, uid, bid, due: 303)
    monkeypatch.setattr('app.services.borrow_service.mark_reservation_fulfilled', lambda c, rid: None)
    monkeypatch.setattr('app.services.borrow_service.log_action', lambda *a, **k: None)

    result = return_borrowed_book(conn, user_id=11, book_id=5)

    assert result['fine_amount'] == 25
    assert result['fine_id'] == 42
    assert result['auto_assigned_borrow_id'] == 303
    assert conn.committed is True
