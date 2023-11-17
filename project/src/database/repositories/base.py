from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):

    __session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session
