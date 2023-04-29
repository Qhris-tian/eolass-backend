from uuid import UUID
from fastapi import APIRouter

router = APIRouter()


@router.post("/", summary="Search for eneba products.")
def create_order():
    """Create order for a product."""
    # Get request details. , price, preorder, quantity, product_id,
    # Generate a uuidv4 reference and order to create order
    # create order in db
    # create order with ezpin
    pass


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
