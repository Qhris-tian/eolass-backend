from fastapi import APIRouter, Body, Depends

from src.plugins.ezpin import Ezpin

from .schema import (
    CatalogAvailabilityRequest,
    CatalogAvailabilityResponse,
    CatalogListResponse,
)

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
    id=str, request: CatalogAvailabilityRequest = Body(...), ezpin=Depends(Ezpin)
):
    return ezpin.catalog_availability(id)
