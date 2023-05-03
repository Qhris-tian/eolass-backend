from fastapi.encoders import jsonable_encoder

from .schema import CreateCardInDB


async def find_inventory(limit: int, db):
    data = await db["inventory"].find().to_list(10)
    return data


async def find_product_cards(product: int, db):
    data = await db["cards"].find({"product": product}).to_list(10)
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
