from fastapi import APIRouter, Depends, status

from .schema import AccountBalanceResponse

# from src.plugins.ezpin import Ezpin
from tests.mocks.ezpin import Ezpin

router = APIRouter()


@router.get(
    "/balance", response_model=AccountBalanceResponse, status_code=status.HTTP_200_OK
)
def get_account_balance(ezpin=Depends(Ezpin)):
    balance = ezpin.get_account_balance()

    return {"balance": balance}
