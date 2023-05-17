from typing import List


async def find_cards(db):
    result = await db["cards"].find().to_list(10)
    return result


async def find_available_cards(availibility: bool, db):
    result = await db["cards"].find({"available": availibility}).to_list(10)
    return result


async def mark_cards_as_unavialable(cards: List, db):
    result = await db["cards"].update_many(
        {"card_number": {"$in": cards}}, {"$set": {"available": False}}
    )
    return result
