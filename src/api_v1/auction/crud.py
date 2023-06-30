from typing import Any, Dict

from fastapi.encoders import jsonable_encoder

from .schema import CreateAuctionInDB


async def find_one_auction_by(key: str, value: Any, db):
    auction = await db["auctions"].find_one({key: str(value)})

    return auction


async def create_auction_details(auction: Dict, db):
    data = CreateAuctionInDB(**auction)
    result = await db["auctions"].insert_one(jsonable_encoder(data))
    created_auction = await find_one_auction_by("_id", result.inserted_id, db)

    return created_auction
