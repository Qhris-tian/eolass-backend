from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.api_v1.product.controller import router as product_router

api_router = APIRouter(default_response_class=JSONResponse)

api_router.include_router(
    product_router,
    prefix="/products",
    tags=["products"],
)


@api_router.get("/health-check", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
