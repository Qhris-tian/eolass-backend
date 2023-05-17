from fastapi import APIRouter, Depends

from src.plugins.eneba import EnebaClient

from .schema import TransactionTypeEnum

router = APIRouter()


@router.get("/")
def get_transactions(
    type: TransactionTypeEnum = TransactionTypeEnum.sale, eneba=Depends(EnebaClient)
):
    response = eneba.get_transactions(type)

    return {"response": response}
