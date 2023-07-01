from fastapi.encoders import jsonable_encoder

from .schema import CreateAccountPreference, UpdateAccountPreference


async def create_new_preference(request, db):
    preference = CreateAccountPreference(**request)

    result = await db["preferences"].insert_one(jsonable_encoder(preference))
    new_preference = await db["preferences"].find_one({"_id": result.inserted_id})

    return new_preference


async def update_preference(preference, request, db):
    update = UpdateAccountPreference(**request)

    print(jsonable_encoder(update))
    await db["preferences"].update_one(
        {"_id": preference},
        {"$set": jsonable_encoder(update)},
    )
    update_preference = await db["preferences"].find_one({"_id": preference})

    return update_preference


async def get_preference(db):
    result = await db["preferences"].find_one()

    return result


async def get_sum_of_orders(period, db) -> float:
    total = 0.0
    pipeline = db["orders"].aggregate(
        [
            {"$match": {"created_at": {"$gte": period}}},
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": {"$multiply": ["$price", "$quantity"]}},
                }
            },
        ]
    )

    async for result in pipeline:
        total = float(result["total"])

    return total
