import json


class Sbase0:
    _basePath = '/var/www/html/openWB'
    _prefixpy = _basePath+'/modules/smarthome/'

    def __init__(self):
        print('__init__ Sbase executed')

    def readret(self):
        with open(self._basePath+'/ramdisk/smarthome_device_ret' +
                  str(self.device_nummer), 'r') as f1:
            answer = json.loads(json.load(f1))
        return answer
