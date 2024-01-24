from functools import wraps, partial
from typing import Callable

from requests import RequestException, Session, Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_REQUEST_TIMEOUT_SECONDS = 5


class SessionFactory:
    session: Session | None = None

    @classmethod
    def get_session(cls) -> Session:
        if cls.session is None:
            session = Session()
            session.mount(
                "https://", HTTPAdapter(max_retries=Retry(total=2, backoff_factor=0.1))
            )
            session.request = partial(  # type: ignore[method-assign]
                session.request, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS
            )
            cls.session = session
        return cls.session


class BadStatusCodeError(RequestException):
    def __init__(self, response: Response) -> None:
        super().__init__()
        self.response = response


def check_response_status_code(
    func: Callable[..., Response]
) -> Callable[..., Response]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.ok:
            return response
        else:
            raise BadStatusCodeError(response)

    return wrapper


checked_get_request = check_response_status_code(SessionFactory.get_session().get)

checked_post_request = check_response_status_code(SessionFactory.get_session().post)
