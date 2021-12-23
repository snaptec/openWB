import sys

from modules.evnotify.EVNotify import EVNotify, EVNotifyConfiguration

if __name__ == '__main__':
    try:
        akey, token, charge_point_str = sys.argv[1:]
        charge_point = int(charge_point_str)
    except ValueError:
        print("unable to parse arguments. Expected: <akey> <token> <charge point>")
        raise

    EVNotify(EVNotifyConfiguration(charge_point, akey, token)).update()
