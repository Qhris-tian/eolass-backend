from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Get products in inventory.")
def get_inventory():
    """Get products in inventory."""
    pass


@router.post("/", summary="Create new product.")
def create_inventory():
    """Create a new product."""
    pass


@router.put("/", summary="Update inventory product.")
def update_inventory():
    """Update inventory product."""
    pass


@router.delete("/{id}", summary="Delete inventory product.")
def delete_inventory(id: str):
    """Delete inventory product."""
    pass
