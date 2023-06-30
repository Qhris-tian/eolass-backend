from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends

from src.api_v1.card.crud import mark_cards_as_unavialable
from src.database import get_database
from src.plugins.eneba import EnebaClient

from .schema import CreateAuctionRequest, UpdateAuctionRequest
from .crud import create_auction_details

router = APIRouter()


@router.get("/")
def get_auctions(page: str = "", limit: int = 10, eneba=Depends(EnebaClient)):
    data = eneba.get_auctions(limit, page)

    return {"auctions": data}


@router.post("/")
async def create_auction(
    auction_data: CreateAuctionRequest,
    type: str,
    inventory_id: str,
    eneba=Depends(EnebaClient),
    db=Depends(get_database),
):
    auction_data.enabled = "true" if auction_data.enabled is True else "false"
    auction_data.autoRenew = "true" if auction_data.autoRenew is True else "false"
    response = eneba.create_auction(auction_data, type)

    await mark_cards_as_unavialable(cards=auction_data.keys, db=db)

    if "errors" not in response:
        created_auction = await create_auction_details({
            "auction_id": response["data"]["S_createAuction"]["actionId"],
            "created_at": str(datetime.now()),
            "inventory_id": inventory_id
            }, db=db)

    return {"response": response}


@router.put("/{stock_id}")
def update_auction(
    stock_id: UUID,
    update_data: UpdateAuctionRequest,
    type: str,
    eneba=Depends(EnebaClient),
):
    update_data.enabled = "true" if update_data.enabled is True else "false"
    update_data.autoRenew = "true" if update_data.autoRenew is True else "false"
    response = eneba.update_auction(update_data, type)

    return {"response": response}


# error coming from eneba api
# @router.post("/enable-declared-stock")
# def enable_declared_stock(eneba=Depends(EnebaClient)):

#     response = eneba.enable_declared_stock()

#     return {
#         "response": response
#     }


@router.get("/keys/{stock_id}")
def get_keys(stock_id: UUID, limit: int, eneba=Depends(EnebaClient)):
    response = eneba.get_keys(stock_id, limit)

    return {"response": response}


@router.get("/fee")
def get_fee(currency: str, type: str, eneba=Depends(EnebaClient)):
    response = eneba.get_fee(currency, type)

    return {"response": response}
