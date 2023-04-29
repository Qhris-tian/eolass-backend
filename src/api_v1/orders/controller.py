from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from src.plugins.ezpin import Ezpin

from .schema import CreateOrderRequest, Order
from .utils import get_month_date

router = APIRouter()


@router.post("/", summary="Search for eneba products.", response_model=Order)
def create_order(request: CreateOrderRequest = Body(...), ezpin=Depends(Ezpin)):
    """Create order for a product."""
    # Get request details. , price, preorder, quantity, product_id,
    # Generate a uuidv4 reference and order to create order
    # create order in db
    # create order with ezpin
    return ezpin.create_order(request)


@router.get("/", summary="Get order history.")
def get_order_history(
    start_date: datetime,
    end_date: datetime,
    limit: int = 10,
    offset: int = 0,
    ezpin=Depends(Ezpin),
):
    """Get order history."""
    if start_date is None:
        start_date = datetime.now()
    if end_date is None:
        end_date = get_month_date(datetime.now(), -1)  # Get last month datetime

    history = ezpin.get_order_history(
        start_date=start_date, end_date=end_date, limit=limit, offset=offset
    )

    return history


@router.get("/{id}", summary="Get order details.")
def get_order(id: UUID):
    """Get order details."""
    # Return order details from ezpin
    pass


@router.get("/{id}/refresh", summary="Refresh order with ezpin.")
def refresh_order(id: UUID):
    """Refresh order with ezpin."""
    # if order request status is pending, check with ezpin
    # if order is accepted and execution is pending check with ezpin
    # if pending order is complete create/update the product and add order keys
    pass


@router.get("/events", summary="Process order event from ezpin.")
def order_event():
    """Process order event from ezpin."""
    # consume ezpin order events
    pass
