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
