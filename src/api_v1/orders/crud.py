from typing import Any, Dict, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder

from src.api_v1.inventory.schema import CreateCardInDB, CreateInventoryInDB

from .schema import CreateOrderInDB, StatusEnum


async def create_new_order(order_request: Dict, db):
    order = CreateOrderInDB(**order_request)

    result = await db["orders"].insert_one(jsonable_encoder(order))
    new_order = await db["orders"].find_one({"_id": result.inserted_id})

    return new_order


async def find_one_order_by(key: str, value: Any, db):
    order = await db["orders"].find_one({key: str(value)})

    return order


async def find_pending_orders_in(key: str, values: List, db, count: int = 10):
    orders = (
        await db["orders"]
        .find({key: {"$in": values}}, {"status": StatusEnum.pending.value})
        .to_list(count)
    )

    return orders


async def create_order_inventory(order: Dict, cards, db):
    """Create or update inventory with order details."""
    inventory = CreateInventoryInDB(
        **order["product"], price=order["total_customer_cost"] / order["count"]
    )

    found_inventory = await db["inventory"].find_one({"sku": order["product"]["sku"]})

    if not found_inventory:  # pragma: no cover
        await db["inventory"].insert_one(jsonable_encoder(inventory))
        found_inventory = await db["inventory"].find_one(
            {"sku": order["product"]["sku"]}
        )

    cards_to_insert = [
        CreateCardInDB(**card, product=found_inventory["sku"]) for card in cards
    ]

    await db["cards"].insert_many(jsonable_encoder(cards_to_insert))

    return found_inventory


def find_orders(db):
    data = db["orders"].find().to_list(10)

    return data


async def mark_order_as_complete(reference_code: UUID, db):
    await db["orders"].update_one(
        {"reference_code": str(reference_code)},
        {"$set": {"status": StatusEnum.complete.value}},
    )
