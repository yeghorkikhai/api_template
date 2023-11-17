from sqlalchemy import URL

from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession


class Database:

    def __init__(self, database_url: URL):
        self._async_engine: AsyncEngine = _create_async_engine(database_url)
        self._async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._async_engine,
            expire_on_commit=False
        )

    @property
    def engine(self) -> AsyncEngine:
        return self._async_engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session_maker
