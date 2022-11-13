import logging


def initlog(name: str, devicenumber: int) -> None:
    log = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log.setLevel(logging.DEBUG)
    fname = '/var/www/html/openWB/ramdisk/smarthome_device_'
    fname += str(devicenumber) + '_' + str(name) + '.log'
    fh = logging.FileHandler(fname, encoding='utf8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
