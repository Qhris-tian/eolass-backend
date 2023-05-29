from fastapi import APIRouter
from starlette.responses import JSONResponse, RedirectResponse

from src.api_v1.account.controller import router as account_router
from src.api_v1.auction.controller import router as auction_router
from src.api_v1.card.controller import router as card_router
from src.api_v1.catalog.controller import router as catalog_router
from src.api_v1.inventory.controller import router as inventory_router
from src.api_v1.orders.controller import router as order_router
from src.api_v1.product.controller import router as product_router
from src.api_v1.transaction.controller import router as transaction_router
from src.api_v1.preference.controller import router as preference_router
from src.config import get_settings

settings = get_settings()

main_router = APIRouter()

api_router = APIRouter(
    default_response_class=JSONResponse, prefix="/api/{0}".format(settings.API_VERSION)
)


api_router.include_router(
    account_router,
    prefix="/account",
    tags=["Account"],
)

api_router.include_router(
    product_router,
    prefix="/products",
    tags=["Products"],
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

api_router.include_router(
    card_router,
    prefix="/cards",
    tags=["Card"],
)

api_router.include_router(
    auction_router,
    prefix="/auctions",
    tags=["Auctions"],
)

api_router.include_router(
    transaction_router,
    prefix="/transactions",
    tags=["Transactions"],
)

api_router.include_router(
    preference_router,
    prefix="/preferences",
    tags=["Preferences"],
)


@api_router.get("/health-check", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


main_router.include_router(api_router)


@main_router.get("/", include_in_schema=False)  # pragma: no cover
def root():
    return RedirectResponse("/redoc")
