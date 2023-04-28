from fastapi import APIRouter, Depends
from src.plugins.eneba import EnebaClient

from .schema import CreateAuctionRequest

router = APIRouter()

@router.get("/")
def get_auctions(page: int = 1, 
                 limit: int = 10,
                  eneba=Depends(EnebaClient)
                  ):

    data = eneba.get_auctions(limit)

    return {
        "auctions": data
    }


@router.post("/")
def create_auction(auctionData: CreateAuctionRequest,
                   eneba=Depends(EnebaClient)):

    auctionData.enabled = "true" if auctionData.enabled == True else "false"
    auctionData.autoRenew = "true" if auctionData.autoRenew == True else "false"
    response = eneba.create_auction(auctionData)

    return {
        "response": response
    }