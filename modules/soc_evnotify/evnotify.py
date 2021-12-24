from helpermodules.cli import run_using_positional_cli_args
from modules.evnotify.EVNotify import EVNotify, EVNotifyConfiguration


def evnotify_update(akey: str, token: str, charge_point: int):
    EVNotify(EVNotifyConfiguration(charge_point, akey, token)).update()


if __name__ == '__main__':
    run_using_positional_cli_args(evnotify_update)
