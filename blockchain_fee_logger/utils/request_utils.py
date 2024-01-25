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


class BadStatusCodeError(ClientError):
    def __init__(self, response: ClientResponse) -> None:
        super().__init__()
        self.response = response


def check_response_status_code(
    func: Callable[..., Awaitable[ClientResponse]]
) -> Callable[..., Awaitable[ClientResponse]]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if response.ok:
            return response
        else:
            raise BadStatusCodeError(response)

    return wrapper


async def checked_get_request(*args, **kwargs) -> ClientResponse:
    session = await SessionFactory.get_session()
    return await check_response_status_code(session.get)(*args, **kwargs)


async def checked_post_request(*args, **kwargs) -> ClientResponse:
    session = await SessionFactory.get_session()
    return await check_response_status_code(session.post)(*args, **kwargs)
