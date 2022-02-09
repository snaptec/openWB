
from requests import Session

from helpermodules import log


def get_http_session() -> Session:
    session = Session()
    session.hooks['response'].append(lambda r, *args, **kwargs: r.raise_for_status())
    session.hooks['response'].append(lambda r, *args, **kwargs: log.MainLogger().debug("Get-Response: " + r.text))
    return session
