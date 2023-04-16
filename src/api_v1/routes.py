from fastapi import APIRouter

from starlette.responses import JSONResponse

api_router = APIRouter(
    default_response_class=JSONResponse
)

@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
