from datetime import date, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, status

from src.api_v1.preference.utils import get_order_limit
from src.database import get_database
from src.plugins.ezpin import Ezpin

from .crud import create_new_order, find_one_order_by, find_orders
from .schema import CreateOrderRequest, OrderHistory, StatusEnum
from .utils import refresh_local_orders, synchronize_order

router = APIRouter()


@router.post(
    "/",
    summary="Create an order.",
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    request: CreateOrderRequest = Body(...),
    db=Depends(get_database),
    ezpin=Depends(Ezpin),
):
    """Create order for a product."""
    if request.price > 0 and request.quantity > 0:
        limit_reached, limit = await get_order_limit(
            db, (request.price * request.quantity)
        )
        if limit_reached:
            raise HTTPException(  # pragma: no cover
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Your order {(request.price * request.quantity)} exceeds your {limit['interval']} limit of {limit['value']}",
            )

        created_order = await create_new_order(request.dict(), db=db)

        status_code, response_json = ezpin.create_order(created_order)

        if status_code == status.HTTP_200_OK or status_code == status.HTTP_201_CREATED:
            return response_json

        raise HTTPException(  # pragma: no cover
            status_code=status_code,
            detail=response_json,
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Price and quantity must be greater than zero",
    )


@router.get("/", summary="Get order history.", response_model=OrderHistory)
def get_order_history(
    background_tasks: BackgroundTasks,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 10,
    offset: int = 1,
    ezpin=Depends(Ezpin),
    db=Depends(get_database),
):
    """Get order history."""
    if start_date is None:
        start_date = date.today() - timedelta(days=5)
    if end_date is None:
        end_date = date.today()

    history = ezpin.get_order_history(
        start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )

    background_tasks.add_task(refresh_local_orders, history["results"], db, ezpin)

    return history


@router.get("/local", summary="Get local orders.")
async def get_local_orders(db=Depends(get_database)):
    data = await find_orders(db)

    return data


@router.get("/{reference_code}", summary="Get order details.")
def get_order(reference_code: str, ezpin=Depends(Ezpin)):
    """Get order details."""
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
        response = await synchronize_order(order, db, ezpin)

        return response

    return {"message": "Order has already been completed."}


@router.get("/{reference_code}/cards", summary="Get Order cards.")
def get_order_cards(reference_code: UUID, ezpin=Depends(Ezpin)):  # pragma: no cover
    return ezpin.get_order_cards(reference_code)


@router.post("/events", summary="Process order event from ezpin.")
def order_event(request=Body()):  # pragma: no cover
    """Process order event from ezpin."""
    # consume ezpin order events
    print(request)

    return {"message": "Order event received successfully."}
