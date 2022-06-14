
import logging
from requests import Session

log = logging.getLogger("soc."+__name__)


def get_http_session() -> Session:
    session = Session()
    session.hooks['response'].append(lambda r, *args, **kwargs: r.raise_for_status())
    session.hooks['response'].append(lambda r, *args, **kwargs: log.debug("Get-Response: " + r.text))
    return session
