import json
from typing import Sequence

from fastapi import status

from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from fastapi.requests import Request
from fastapi.responses import JSONResponse

from project.src.api.exceptions.base import APIException

from project.src import logger


def build_exc_desc(
        errs: Sequence
) -> str:
    detail = errs[0]
    return f"""{detail.get('loc')[0]} parameter {detail.get('loc')[-1]} {detail.get("msg").replace("Input ", "")}"""


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, str):
        detail = json.loads(exc.detail)
    else:
        detail = exc.detail
    logger.debug(f"err_code={detail.get('err_code')}, err_desc={detail.get('err_desc')}")
    return JSONResponse({
        "err_code": detail.get("err_code"),
        "err_desc": detail.get("err_desc")
    }, exc.status_code)


async def api_exception_handler(_: Request, exc: APIException) -> JSONResponse:
    return JSONResponse({
        "err_code": exc.err_code,
        "err_desc": exc.err_desc
    }, exc.status_code)


async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
    logger.info(exc.errors())
    return JSONResponse({
        "err_code": "BAD_REQUEST",
        "err_desc": build_exc_desc(exc.errors())
    }, status.HTTP_400_BAD_REQUEST)


async def internal_server_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.error(exc)
    return JSONResponse({
        "err_code": "INTERNAL_ERR",
        "err_desc": "Internal API Server error"
    }, status.HTTP_500_INTERNAL_SERVER_ERROR)
