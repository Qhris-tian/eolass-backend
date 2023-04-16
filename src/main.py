import logging
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.api_v1.exception_handlers import http_exception_handler, request_error_handler
from src.api_v1.routes import api_router

from src.events import start_app_handler, shutdown_app_handler
from src.config import get_settings

settings = get_settings()

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        description="Eolass API",
        openapi_url="/api/{0}/openapi.json".format(settings.api_version),
    )
    application.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings.allowed_origins.split(","),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(
        api_router, prefix="/api/{0}".format(settings.api_version)
    )
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(RequestValidationError, request_error_handler)
    application.add_event_handler("startup", start_app_handler)
    application.add_event_handler("shutdown", shutdown_app_handler)

    return application


app = create_application()