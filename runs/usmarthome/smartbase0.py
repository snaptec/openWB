import json
from datetime import datetime, timezone


class Sbase0:
    _basePath = '/var/www/html/openWB'
    _prefixpy = _basePath+'/modules/smarthome/'

    def logClass(self, level, msg):
        if (int(level) >= 0):
            local_time = datetime.now(timezone.utc).astimezone()
            with open(self._basePath+'/ramdisk/smarthome.log', 'a',
                      encoding='utf8', buffering=1) as file:
                if (int(level) == 0):
                    file.write(local_time.strftime(format="%Y-%m-%d %H:%M:%S")
                               + '-: ' + str(msg) + '\n')
                if (int(level) == 1):
                    file.write(local_time.strftime(format="%Y-%m-%d %H:%M:%S")
                               + '-: ' + str(msg) + '\n')
                if (int(level) == 2):
                    file.write(local_time.strftime(format="%Y-%m-%d %H:%M:%S")
                               + '-: ' + str(msg) + '\n')

    def readret(self):
        with open(self._basePath+'/ramdisk/smarthome_device_ret' +
                  str(self.device_nummer), 'r') as f1:
            answer = json.loads(json.load(f1))
        return answer
