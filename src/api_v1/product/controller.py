from fastapi import APIRouter, Depends

from src.plugins.eneba import EnebaClient

from .utils import sanitize_response

router = APIRouter()


@router.get(
    "/search",
    summary="Search for eneba products.",
)
def search_product(
    product: str,
    per_page: int = 5,
    eneba=Depends(EnebaClient),
):
    """Search for eneba products."""
    data = sanitize_response(eneba.search(product_name=product, count=per_page))

    return {"products": data}
