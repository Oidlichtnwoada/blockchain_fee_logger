import functools

import requests
from requests import RequestException
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_REQUEST_TIMEOUT_SECONDS = 5


class SessionFactory:
    session: requests.Session | None = None

    @classmethod
    def get_session(cls) -> requests.Session:
        if cls.session is None:
            session = requests.Session()
            session.mount(
                "https://", HTTPAdapter(max_retries=Retry(total=2, backoff_factor=0.1))
            )
            session.request = functools.partial(  # type: ignore[method-assign]
                session.request, timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS
            )
            cls.session = session
        return cls.session


class BadStatusCodeError(RequestException):
    def __init__(self, response: requests.Response) -> None:
        self.response = response
        super().__init__()


def check_request_status_code(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.ok:
            return response
        else:
            raise BadStatusCodeError(response)

    return wrapper


checked_get_request = check_request_status_code(SessionFactory.get_session().get)

checked_post_request = check_request_status_code(SessionFactory.get_session().post)
