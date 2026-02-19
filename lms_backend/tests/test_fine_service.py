from datetime import datetime, timedelta

from app.services.fine_service import calculate_fine


def test_no_fine_when_return_on_time():
    due = datetime(2026, 2, 10)
    returned = datetime(2026, 2, 10)
    assert calculate_fine(due, returned) == 0


def test_no_fine_when_return_before_due():
    due = datetime(2026, 2, 10)
    returned = datetime(2026, 2, 9)
    assert calculate_fine(due, returned) == 0


def test_fine_calculation_multiple_days():
    due = datetime(2026, 2, 10)
    returned = datetime(2026, 2, 13)
    # 3 days late * FINE_PER_DAY (5) = 15
    assert calculate_fine(due, returned) == 15
