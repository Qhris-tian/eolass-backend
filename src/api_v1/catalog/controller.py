from fastapi import APIRouter
from .schema import CatalogAvailabilityInput, CatalogListResponse

router = APIRouter()


@router.get("/", summary="Get catalog list.", response_model=CatalogListResponse)
def get_catalog_list():
    """Get catalog list."""
    pass


@router.get(
    "/{id}/availability",
    summary="Checks enough cards are available for a product.",
    response_model=CatalogAvailabilityInput,
)
def check_catalog_availability(id=str):
    pass
