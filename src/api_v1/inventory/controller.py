from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.database import get_database

from .crud import (
    create_product,
    create_product_card,
    filter_inventory_by_title,
    find_inventory,
    find_one_product_by,
    find_product_cards,
    update_product,
)
from .schema import BaseInventory, CreateInventoryCardRequest, Inventory

router = APIRouter()


@router.get("/", summary="Get products in inventory.")
async def get_inventory(limit: int = 10, db=Depends(get_database)):
    """Get products in inventory."""
    inventory = await find_inventory(limit=limit, db=db)

    return inventory


@router.get("/search", summary="Search products in inventory.")
async def search_inventory(name: str, db=Depends(get_database)):
    """Get products in inventory."""
    inventory = await filter_inventory_by_title(name, db)

    return inventory


@router.get("/{product_sku}/cards", summary="Get product cards.")
async def get_inventory_cards(product_sku: int, db=Depends(get_database)):
    response = await find_product_cards(product=product_sku, db=db)

    return response


@router.post(
    "/{sku}/cards",
    summary="Create an order.",
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_card(
    sku: int,
    request: CreateInventoryCardRequest = Body(...),
    db=Depends(get_database),
):
    product = await find_one_product_by(by="sku", value=sku, db=db)

    if product:
        card = await create_product_card(product=sku, card_detais=request.dict(), db=db)

        return {"card": card}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Price and quantity must be greater than zero",
    )


@router.post(
    "/",
    summary="Create new product.",
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory(
    request: Inventory = Body(...),
    db=Depends(get_database),
):
    existing_product = await find_one_product_by(by="sku", value=request.sku, db=db)

    if existing_product:
        product = await update_product(request.sku, request.dict(), db)
    else:
        product = await create_product(request.dict(), db)

    return product


@router.put("/{sku}", summary="Update inventory product.")
async def update_inventory(
    sku: int,
    request: BaseInventory = Body(...),
    db=Depends(get_database),
):
    """Update inventory product."""
    existing_product = await find_one_product_by(by="sku", value=sku, db=db)
    if existing_product:
        product = await update_product(sku, request.dict(), db)
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Inventory does not exist."
    )
