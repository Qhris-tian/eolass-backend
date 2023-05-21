from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from ratelimit.exception import RateLimitException  # type: ignore
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.api_v1.exception_handlers import (
    http_exception_handler,
    rate_limit_error_handler,
    request_error_handler,
)
from src.api_v1.routes import main_router
from src.config import get_settings
from src.events import shutdown_app_handler, start_app_handler

settings = get_settings()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        description="Eolass API",
        openapi_url="/api/{0}/openapi.json".format(settings.API_VERSION),
    )
    application.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings.ALLOWED_ORIGINS.split(","),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(main_router)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, request_error_handler)
    application.add_exception_handler(RateLimitException, rate_limit_error_handler)
    application.add_event_handler("startup", start_app_handler)
    application.add_event_handler("shutdown", shutdown_app_handler)

    return application


app = create_application()
