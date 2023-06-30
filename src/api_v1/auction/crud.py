

async def create_auction_details(auction, db):
    result = await db["auctions"].insert_one(auction)
    newly_created_auction = await db["auctions"].find_one({"_id": result.inserted_id})

    return newly_created_auction