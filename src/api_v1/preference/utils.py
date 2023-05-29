from datetime import date

from .schema import IntervalEnum
from .crud import (
    get_preference,
    get_sum_of_orders,
)


async def get_order_limit(db, added: float = 0.0): # pragma: no cover
    preference = await get_preference(db)

    if preference:
        for limit in preference["spending_limits"]:
            constraint = limit["value"] + added + 2

            match limit["interval"]:
                case IntervalEnum.daily.value:
                    constraint = await get_sum_of_orders(
                        date.today().strftime("%Y-%m-%d"), db
                    )

                case IntervalEnum.monthly.value:
                    constraint = await get_sum_of_orders(
                        date.today().strftime("%Y-%m-01"), db
                    )

                case IntervalEnum.annual.value:
                    constraint = await get_sum_of_orders(
                        date.today().strftime("%Y-01-01"), db
                    )

            if limit["value"] < constraint + added:                
                return True, limit

    return False, {}
