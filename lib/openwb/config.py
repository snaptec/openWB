from os.path import dirname, realpath, join

OPENWB_ROOT = dirname(dirname(dirname(realpath(__file__))))
"""Contains the root directory of openWB without trailing slash (usually /var/www/html/openWB)"""
RAMDISK_PATH = join(OPENWB_ROOT, "ramdisk")
"""Contains the path to the ramdisk without trailing slash (usually /var/www/html/openWB/ramdisk)"""


class Config:
    """A utility class to access the openWB configuration.

    To use:

    >>> config = Config()
    >>> config["maximalstromstaerke"]
    '32'

    `Config()` returns a singleton, so the config file will be read only once, even if calling `Config()` multiple times
    """
    __instance = None

    class __Config:
        def __init__(self):
            with open(join(OPENWB_ROOT, "openwb.conf"), "r") as f:
                self.__values = dict(tuple(line.rstrip().split("=", 1)) for line in f)

        def __getitem__(self, item: str) -> str:
            return self.__values[item]

    def __new__(cls):
        if Config.__instance is None:
            Config.__instance = Config.__Config()
        return Config.__instance
