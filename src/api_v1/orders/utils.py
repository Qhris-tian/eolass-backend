import calendar
from datetime import datetime
from typing import Dict, List

from .crud import create_order_inventory, find_pending_orders_in, mark_order_as_complete


def get_month_date(date: datetime, delta: int) -> datetime:
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m:
        m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


async def refresh_local_orders(order_list: List, db, ezpin) -> None:
    reference_list = [order["reference_code"] for order in order_list]

    found_orders = await find_pending_orders_in(
        key="reference_code", values=reference_list, db=db
    )

    if len(found_orders) == 0:
        return

    for order in found_orders:  # pragma: no cover
        await synchronize_order(order, db, ezpin)


async def synchronize_order(order, db, ezpin) -> Dict:
    order_ezpin = ezpin.get_order(order["reference_code"])

    if order_ezpin["is_completed"] and order_ezpin["status"] == 1:
        cards = ezpin.get_order_cards(order["reference_code"])
        await create_order_inventory(order_ezpin, cards["results"], db)

        await mark_order_as_complete(order["reference_code"], db)

        return {"message": "Order inventory created."}

    return {"message": "Order is still in progress."}  # pragma: no cover
