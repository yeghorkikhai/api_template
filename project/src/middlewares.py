from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.requests import Request


class DatabaseMiddleware:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._async_session_factory = session_maker

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session_factory

    async def __call__(self, request: Request, call_next):
        request.state.database_session = self.session
        response = await call_next(request)
        return response
