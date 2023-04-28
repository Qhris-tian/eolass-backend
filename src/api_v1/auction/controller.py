from fastapi import APIRouter, Depends
from src.plugins.eneba import EnebaClient

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