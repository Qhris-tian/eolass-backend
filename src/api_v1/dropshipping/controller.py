from fastapi import APIRouter, Body, Depends, status
from starlette.responses import JSONResponse

from src.api_v1.inventory.schema import CreateCardInDB
from src.api_v1.orders.crud import create_new_order, find_one_order_by
from src.database import get_database
from src.plugins.ezpin import Ezpin

from .crud import get_auction_inventory
from .schema import (
    ActionEnum,
    ProvisionRequest,
    ProvisionResponse,
    ReserveRequest,
    ReserveRespone,
    TypeEnum,
)

router = APIRouter()


@router.post("/reserve", response_model=ReserveRespone)
async def reserve(
    request: ReserveRequest = Body(...), db=Depends(get_database), ezpin=Depends(Ezpin)
):
    auction = request.auctions[0]
    product = await get_auction_inventory(auction["auctionId"], db=db)

    if product:
        response = ezpin.catalog_availability(
            product["sku"], {"item_count": auction["keyCount"]}, request.available
        )

        if response.status_code == status.HTTP_200_OK:
            created_order = await create_new_order(
                {
                    "reference_code": request.orderId,
                    "product_id": product["sku"],
                    "quantity": auction["keyCount"],
                    "price": auction["price"],
                    "auction_id": auction["auctionId"],
                },
                db,
            )

            status_code, response_json = ezpin.create_order(created_order)

            return JSONResponse(
                status_code=status_code or 200,
                content={
                    "action": ActionEnum.reserve.value,
                    "orderId": request.orderId,
                    "success": True,
                    "message": None,
                },
            )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "action": ActionEnum.reserve.value,
            "orderId": request.orderId,
            "success": False,
            "message": "We are unable to fulfil this request.",
        },
    )


@router.post("/provision", response_model=ProvisionResponse)
async def provision(
    request: ProvisionRequest = Body(...),
    db=Depends(get_database),
    ezpin=Depends(Ezpin),
):
    existing_order = await find_one_order_by(
        key="reference_code", value=request.orderId, db=db
    )

    cards = ezpin.get_order_cards(request.orderId)

    [
        CreateCardInDB(
            **card,
            product=existing_order["product_id"] if existing_order else 0,
            order_id=request.orderId,
            available=False
        )
        for card in cards
    ]

    return {
        "action": ActionEnum.provide.value,
        "orderId": request.orderId,
        "success": True,
        "message": None,
        "auctions": [
            {
                "auctionId": "e5c02e0e-13ec-11ee-aac8-72483fd869ac",
                "keys": [
                    {
                        "type": TypeEnum.text.value,
                        "value": card["card_number"],
                    }
                    for card in cards
                ],
            }
        ],
    }
