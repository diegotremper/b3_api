import base64
import functools
import json

from requests import Session
from requests_cache import NEVER_EXPIRE, CacheMixin
from requests_ratelimiter import LimiterMixin

from b3_api.api_configs import APIConfigs


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """Session class with caching and rate-limiting behavior. Accepts arguments for both
    LimiterSession and CachedSession.

    See also:
        https://pypi.org/project/requests-cache/
    """


@functools.cache
def request_session(
    name, expire_after=NEVER_EXPIRE, configs=APIConfigs()
) -> Session:
    """
    Create a persistent session with `requests_cache` and `requests_ratelimiter`.
    Used to not overload B3 servers until they decide to block us.
    """
    return CachedLimiterSession(
        cache_name="{}/{}.sqlite".format(configs.http_cache_dir, name),
        expire_after=expire_after,
        per_second=configs.requests_per_seconds,
    )


def encode_param(params: dict) -> str:
    """
    Encode a dict as json-encoded-base64 string.
    A lovely pattern for API parameters by the way 🤌.
    Congratulations to the B3 API team. 👏
    """
    json_string = json.dumps(params).encode("utf-8")
    return base64.b64encode(json_string).decode("utf-8")
