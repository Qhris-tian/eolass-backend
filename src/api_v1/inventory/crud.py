from datetime import datetime

from fastapi.encoders import jsonable_encoder

from .schema import CreateCardInDB, CreateInventoryInDB, UpdateInventoryInDB


async def find_inventory(db, limit: int = 10):
    data = await db["inventory"].find().to_list(limit)
    return data


async def find_product_cards(product: int, db):
    data = await db["cards"].find({"product": product, "available": True}).to_list(10)
    return data


async def filter_inventory_by_title(title: str, db):
    products = (
        await db["inventory"]
        .find({"title": {"$regex": title, "$options": "i"}})
        .to_list(10)
    )

    return products


async def find_one_product_by(by: str, value: str | int, db):
    product = await db["inventory"].find_one({by: value})
    return product


async def create_product_card(product, card_detais, db):
    card_detais = CreateCardInDB(**card_detais, product=product)

    result = await db["cards"].insert_one(jsonable_encoder(card_detais))
    new_card = await db["cards"].find_one({"_id": result.inserted_id})

    return new_card


async def update_product(sku, product_details, db):
    inventory = UpdateInventoryInDB(**product_details, updated_at=datetime.now())

    await db["inventory"].update_one(
        {"sku": sku}, {"$set": jsonable_encoder(inventory, exclude_none=True)}
    )
    new_product = await db["inventory"].find_one({"sku": sku})

    return new_product


async def create_product(product_details, db):
    inventory = CreateInventoryInDB(**product_details)
    result = await db["inventory"].insert_one(jsonable_encoder(inventory))
    new_product = await db["inventory"].find_one({"_id": result.inserted_id})

    return new_product
