from functools import wraps
from typing import Callable, Awaitable

from aiohttp import (
    ClientSession,
    ClientResponse,
    ClientError,
    ClientTimeout,
)
from aiohttp_retry import RetryClient, ExponentialRetry

DEFAULT_REQUEST_TIMEOUT_SECONDS = 5
DEFAULT_RETRIES = 3


class SessionFactory:
    session: RetryClient | None = None

    @classmethod
    async def get_session(cls) -> RetryClient:
        if cls.session is None:
            session = RetryClient(
                client_session=ClientSession(
                    timeout=ClientTimeout(total=DEFAULT_REQUEST_TIMEOUT_SECONDS)
                ),
                retry_options=ExponentialRetry(attempts=DEFAULT_RETRIES),
            )
            cls.session = session
        return cls.session

    @classmethod
    async def close_session(cls) -> None:
        if cls.session is not None:
            await cls.session.close()


class BadStatusCodeError(ClientError):
    def __init__(self, response: ClientResponse) -> None:
        super().__init__()
        self.response = response


def get_response_text(
    func: Callable[..., Awaitable[ClientResponse]], check_status_code: bool = True
) -> Callable[..., Awaitable[str]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> str:
        async with func(*args, **kwargs) as response:
            if check_status_code and not response.ok:
                raise BadStatusCodeError(response)
            return await response.text()

    return wrapper


async def checked_get_request_body_text(*args, **kwargs) -> str:
    session = await SessionFactory.get_session()
    return await get_response_text(session.get)(*args, **kwargs)


async def checked_post_request_body_text(*args, **kwargs) -> str:
    session = await SessionFactory.get_session()
    return await get_response_text(session.post)(*args, **kwargs)
