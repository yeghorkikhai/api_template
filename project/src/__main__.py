from fastapi import FastAPI

from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from sqlalchemy import URL

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from project.src.middlewares import DatabaseMiddleware

from project.src.database.database import Database

from project.src.api.routers import api_router

from project.src.api.exceptions.base import APIException
from project.src.api.exceptions.exception_handlers import api_exception_handler
from project.src.api.exceptions.exception_handlers import http_exception_handler
from project.src.api.exceptions.exception_handlers import request_validation_exception_handler
from project.src.api.exceptions.exception_handlers import internal_server_error_handler

from project.src.cfg import AppConfig


class Application:

    @property
    def database_url(self) -> URL:
        url = URL.create(
            'postgresql+asyncpg',
            host=AppConfig.database.host,
            port=AppConfig.database.port,
            username=AppConfig.database.user,
            password=AppConfig.database.password,
            database=AppConfig.database.name
        )
        return url

    @property
    def database(self) -> Database:
        db = Database(self.database_url)
        return db

    def startup(self) -> FastAPI:
        application = FastAPI(
            docs_url='/api/docs',
            # Disable reDoc
            redoc_url=None,
            openapi_url='/api/docs/openapi.json',
            # App info
            title=AppConfig.title,
            description=AppConfig.description,
            version=AppConfig.version
        )

        setattr(application, "database", self.database)

        # Include routers
        application.include_router(api_router)

        # Add middlewares
        application.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=['*'],
            allow_methods=['*'],
            allow_headers=['*']
        )

        application.add_middleware(
            BaseHTTPMiddleware,
            dispatch=DatabaseMiddleware(
                session_maker=self.database.session_maker
            )
        )

        # Add exception handlers
        application.add_exception_handler(HTTPException, http_exception_handler)
        application.add_exception_handler(APIException, api_exception_handler)
        application.add_exception_handler(RequestValidationError, request_validation_exception_handler)
        application.add_exception_handler(500, internal_server_error_handler)

        return application


app = Application().startup()
