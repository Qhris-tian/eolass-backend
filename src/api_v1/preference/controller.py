from fastapi import APIRouter, Body, Depends, status

from src.database import get_database

from .crud import create_new_preference, update_preference, get_preference
from .schema import Preference


router = APIRouter()


@router.get("/")
async def get_account_preference(db=Depends(get_database)):
    result = await get_preference(db)
    return result


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_account_preference(
    request: Preference = Body(...), db=Depends(get_database)
):
    result = await create_new_preference(request.dict(), db)

    return result


@router.put("/{id}")
async def update_account_preference(
    id=str, request: Preference = Body(...), db=Depends(get_database)
):
    result = await update_preference(id, request.dict(), db)
    return result

