from sys import version_info

from .volvooncall import Connection, __version__  # noqa: F401
from .dashboard import Dashboard  # noqa: F401

MIN_PYTHON_VERSION = (3, 5, 3)

_ = version_info >= MIN_PYTHON_VERSION or exit(
    "Python %d.%d.%d required" % MIN_PYTHON_VERSION
)
