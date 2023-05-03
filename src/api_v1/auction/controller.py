from uuid import UUID

from fastapi import APIRouter, Depends

from src.plugins.eneba import EnebaClient

from .schema import CreateAuctionRequest, UpdateAuctionRequest

router = APIRouter()


@router.get("/")
def get_auctions(page: int = 1, limit: int = 10, eneba=Depends(EnebaClient)):
    data = eneba.get_auctions(limit)

    return {"auctions": data}


@router.post("/")
def create_auction(
    auctionData: CreateAuctionRequest, type: str, eneba=Depends(EnebaClient)
):
    auctionData.enabled = "true" if auctionData.enabled is True else "false"
    auctionData.autoRenew = "true" if auctionData.autoRenew is True else "false"
    response = eneba.create_auction(auctionData, type)

    return {"response": response}


@router.put("/{stock_id}")
def update_auction(
    stock_id: UUID,
    updateData: UpdateAuctionRequest,
    type: str,
    eneba=Depends(EnebaClient),
):
    response = eneba.update_auction(updateData, type)

    return {"response": response}


# error coming from eneba api
# @router.post("/enable-declared-stock")
# def enable_declared_stock(eneba=Depends(EnebaClient)):

#     response = eneba.enable_declared_stock()

#     return {
#         "response": response
#     }


@router.get("/keys/{stock_id}")
def get_keys(stock_id: UUID, eneba=Depends(EnebaClient)):
    response = eneba.get_keys(stock_id)

    return {"response": response}