from typing import Optional

from fastapi import APIRouter, Depends

from src.database import get_database

from .crud import find_available_cards, find_cards

router = APIRouter()


@router.get("/", summary="Get all cards")
async def get_cards(available: Optional[bool] = None, db=Depends(get_database)):
    if available is not None:
        cards = await find_available_cards(available, db)
    else:
        cards = await find_cards(db)

    return {"cards": cards}
