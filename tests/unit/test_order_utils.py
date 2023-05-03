from datetime import datetime

from src.api_v1.orders.utils import get_month_date


def test_get_month_date_when_month_is_zero():
    timestamp = datetime(2023, 3, 31)
    result = get_month_date(timestamp, -3)

    assert result == datetime(2022, 12, 31, 0, 0)


def test_get_month_date_when_month_one_and_eleven():
    timestamp = datetime(2023, 3, 31)
    result = get_month_date(timestamp, -2)

    assert result == datetime(2023, 1, 31, 0, 0)
