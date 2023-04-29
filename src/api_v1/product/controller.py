from fastapi import APIRouter, Depends, HTTPException, status

from src.plugins.eneba import EnebaClient

from .schema import Product, ProductResponse
from .utils import sanitize_response

router = APIRouter()


@router.get(
    "/search",
    summary="Search for eneba products.",
    response_model=ProductResponse,
)
def search_product(
    product: str,
    per_page: int = 5,
    eneba=Depends(EnebaClient),
):
    """Search for eneba products."""
    data = sanitize_response(eneba.search(product_name=product, count=per_page))

    return {"products": data}


@router.get(
    "/{id}",
    summary="Get product details.",
    response_model=Product,
)
def get_product_details(
    id: str,
    eneba=Depends(EnebaClient),
):
    """Get product details."""
    response = eneba.get_product(product_id=id)

    if response:
        return sanitize_response([response]).pop()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist."
    )
