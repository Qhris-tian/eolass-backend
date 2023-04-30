from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, status

from src.database import get_database

from src.plugins.ezpin import Ezpin

from .crud import (
    create_new_order,
    create_order_inventory,
    find_one_order_by,
    find_orders,
    mark_order_as_complete,
)
from .schema import CreateOrderRequest, Order, StatusEnum
from .utils import get_month_date, refresh_local_orders

router = APIRouter()


@router.post(
    "/",
    summary="Create an order.",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    request: CreateOrderRequest = Body(...),
    db=Depends(get_database),
    ezpin=Depends(Ezpin),
):
    """Create order for a product."""
    if request.price > 0 and request.quantity > 0:
        created_order = await create_new_order(request.dict(), db=db)

        return ezpin.create_order(created_order)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Price and quantity must be greater than zero",
    )


@router.get("/", summary="Get order history.")
def get_order_history(
    background_tasks: BackgroundTasks,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    limit: int = 10,
    offset: int = 0,
    ezpin=Depends(Ezpin),
    db=Depends(get_database)
):
    """Get order history."""
    if start_date is None:
        start_date = datetime.now()
    if end_date is None:
        end_date = get_month_date(datetime.now(), -1)  # Get last month datetime

    history = ezpin.get_order_history(
        start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )

    background_tasks.add_task(refresh_local_orders, history, db)

    return history


@router.get("/local", summary="Get local orders.")
async def get_local_orders(db=Depends(get_database)):
    data = await find_orders(db)

    return data


@router.get("/{reference_code}", summary="Get order details.")
def get_order(reference_code: UUID, ezpin=Depends(Ezpin)):
    """Get order details."""
    # Return order details from ezpin
    return ezpin.get_order(reference_code)


@router.get("/{reference_code}/refresh", summary="Refresh order with ezpin.")
async def refresh_order(
    reference_code: UUID, db=Depends(get_database), ezpin=Depends(Ezpin)
):
    """Refresh order with ezpin."""
    order = await find_one_order_by("reference_code", reference_code, db)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    if order["status"] == StatusEnum.pending.value:
        order_ezpin = ezpin.get_order(reference_code)

        if order_ezpin["is_completed"]:
            cards = ezpin.get_order_cards(reference_code)
            await create_order_inventory(order_ezpin, cards, db)

            await mark_order_as_complete(reference_code, db)

            return {"message": "Order inventory created."}

        return {"message": "Order is still in progress."}  # pragma: no cover

    return {"message": "Order has already been completed."}


@router.get("/events", summary="Process order event from ezpin.")
def order_event():  # pragma: no cover
    """Process order event from ezpin."""
    # consume ezpin order events
    pass
