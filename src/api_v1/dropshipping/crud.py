from src.api_v1.auction.crud import find_one_auction_by
from src.api_v1.inventory.crud import find_one_product_by


async def get_auction_inventory(auction_id: str, db):
    auction = await find_one_auction_by(key="auction_id", value=auction_id, db=db)

    product = await find_one_product_by(by="sku", value=auction["inventory_id"], db=db)
    return product
