from typing import Dict

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from ratelimit.exception import RateLimitException  # type: ignore
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:  # pragma: no cover
    return JSONResponse(
        {"errors": [exc.detail], "status_code": exc.status_code},
        status_code=exc.status_code,
    )


async def request_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:  # pragma: no cover
    error_bag: Dict = {}

    for error in exc.errors():
        error_bag[error["loc"][1]] = error["msg"]

    return JSONResponse(
        content={
            "errors": error_bag,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


async def rate_limit_error_handler(
    request: Request,
    exception: RateLimitException,
):  # pragma: no cover
    return JSONResponse(
        content={
            "errors": "Too many request try after again later.",
            "status_code": status.HTTP_429_TOO_MANY_REQUESTS,
        },
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )
