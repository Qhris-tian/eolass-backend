from uuid import UUID

from fastapi import APIRouter, Depends

from src.plugins.eneba import EnebaClient

from .schema import CreateAuctionRequest, UpdateAuctionRequest

router = APIRouter()


@router.get("/")
def get_auctions(page: str = None, limit: int = 10, eneba=Depends(EnebaClient)):
    data = eneba.get_auctions(limit, page)

    return {"auctions": data}


@router.post("/")
def create_auction(
    auction_data: CreateAuctionRequest, type: str, eneba=Depends(EnebaClient)
):
    auction_data.enabled = "true" if auction_data.enabled is True else "false"
    auction_data.autoRenew = "true" if auction_data.autoRenew is True else "false"
    response = eneba.create_auction(auction_data, type)

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
