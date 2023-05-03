from fastapi import APIRouter, Depends, HTTPException, status

# from src.plugins.ezpin import Ezpin
from tests.mocks.ezpin import Ezpin

from .schema import CatalogAvailabilityResponse, CatalogListResponse

router = APIRouter()


@router.get("/", summary="Get catalog list.", response_model=CatalogListResponse)
def get_catalog_list(ezpin=Depends(Ezpin)):
    """Get catalog list."""
    return ezpin.catalog_list()


@router.get(
    "/{id}/availability",
    summary="Checks enough cards are available for a product.",
    response_model=CatalogAvailabilityResponse,
)
def check_catalog_availability(
    id: str, price: float, quantity: int, ezpin=Depends(Ezpin)
):
    if price > 0 and quantity > 0:
        return ezpin.catalog_availability(id, {"quantity": quantity, "price": price})
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Price and quantity must be greater than zero"},
        )
