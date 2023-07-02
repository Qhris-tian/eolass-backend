from fastapi import APIRouter, Body, Depends, status

from src.plugins.ezpin import Ezpin
from src.plugins.eneba import EnebaClient

from .schema import AccountBalanceResponse, RegisterCallbackRequst

router = APIRouter()


@router.get(
    "/balance", response_model=AccountBalanceResponse, status_code=status.HTTP_200_OK
)
def get_account_balance(ezpin=Depends(Ezpin)):
    balance = ezpin.get_account_balance()

    return {"balance": balance}


router.post("/register-callback")
def register_callback(
    request: RegisterCallbackRequst = Body(...), eneba=Depends(EnebaClient)
):
    eneba.register_callback_url(
        type=request.type,
        authorization=request.authorization,
        url=request.url,
    )

    return {"message": "Callback registered."}
