from fastapi import APIRouter
from starlette.responses import JSONResponse, RedirectResponse

from src.api_v1.catalog.controller import router as catalog_router
from src.api_v1.inventory.controller import router as inventory_router
from src.api_v1.orders.controller import router as order_router
from src.api_v1.product.controller import router as product_router
from src.config import get_settings

settings = get_settings()

main_router = APIRouter()

api_router = APIRouter(
    default_response_class=JSONResponse, prefix="/api/{0}".format(settings.API_VERSION)
)


api_router.include_router(
    product_router,
    prefix="/products",
    tags=["products"],
)

api_router.include_router(
    order_router,
    prefix="/orders",
    tags=["Orders"],
)

api_router.include_router(
    catalog_router,
    prefix="/catalogs",
    tags=["Catalogs"],
)

api_router.include_router(
    inventory_router,
    prefix="/inventory",
    tags=["Inventory"],
)


@api_router.get("/health-check", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


main_router.include_router(api_router)


@main_router.get("/", include_in_schema=False)  # pragma: no cover
def root():
    return RedirectResponse("/redoc")
