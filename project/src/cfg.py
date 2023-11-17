from os.path import abspath
from os import getenv

from dataclasses import dataclass

from requests import __version__

from project.src.configs.database import DatabaseConfig

from dotenv import load_dotenv

load_dotenv(abspath(".env"))


@dataclass(frozen=True)
class AppConfig:

    database: DatabaseConfig = DatabaseConfig(
        host=getenv("DATABASE_HOST"),
        port=getenv("DATABASE_PORT"),
        user=getenv("DATABASE_USER"),
        password=getenv("DATABASE_PASSWORD"),
        name=getenv("DATABASE_NAME")
    )

    broker_url: str = getenv("BROKER_URL")

    test_database: DatabaseConfig = DatabaseConfig(
        host=getenv("TEST_DATABASE_HOST"),
        port=getenv("TEST_DATABASE_PORT"),
        user=getenv("TEST_DATABASE_USER"),
        password=getenv("TEST_DATABASE_PASSWORD"),
        name=getenv("TEST_DATABASE_NAME")
    )

    title: str = "Newsletter API"
    description: str = ""
    version: str = __version__
