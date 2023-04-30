from fastapi import APIRouter, Depends

from src.database import get_database

from .crud import filter_inventory_by_title, find_inventory, find_product_cards

router = APIRouter()


@router.get("/", summary="Get products in inventory.")
async def get_inventory(limit=10, db=Depends(get_database)):
    """Get products in inventory."""
    inventory = await find_inventory(limit=limit, db=db)

    return inventory


@router.get("/search", summary="Search products in inventory.")
async def search_inventory(name: str, db=Depends(get_database)):
    """Get products in inventory."""
    inventory = await filter_inventory_by_title(name, db)

    return inventory


@router.get("/{product_sku}/cards", summary="Get product cards")
async def get_inventory_cards(product_sku: int, db=Depends(get_database)):
    response = await find_product_cards(product=product_sku, db=db)

    return response


@router.post("/", summary="Create new product.")
def create_inventory():  # pragma: no cover
    """Create a new product."""
    pass


@router.put("/", summary="Update inventory product.")
def update_inventory():  # pragma: no cover
    """Update inventory product."""
    pass