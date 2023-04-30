import calendar
from datetime import datetime
from typing import List
from .crud import find_pending_orders_in


def get_month_date(date: datetime, delta: int) -> datetime:
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


async def refresh_local_orders(order_list: List, db): 
    found_orders = await find_pending_orders_in(
        key="reference_code", values=order_list, db=db
    )

    if found_orders is None: # pragma: no cover
       return 

    # refresh each pending individual
