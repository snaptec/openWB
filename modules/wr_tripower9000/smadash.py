#!/usr/bin/python
import sys
import urllib
import ssl
import json

class SMADASH:
    valueURL = '/dyn/getDashValues.json'
    def __init__(self, ip): 
        self.host = ip

    def read(self):
#       urllib.disable_warnings()
       power, generation = 0,0
       context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
       context.verify_mode = ssl.CERT_NONE
       r = urllib.urlopen('https://' + self.host + self.valueURL, context = context)
       if r.getcode() == 200:
          content = json.loads(r.read())
          for unitName, unitResult in content['result'].items():
             powerOut = int(unitResult['6100_40463600']['1'][0]['val']) # Generation
             powerIn = int(unitResult['6100_40463700']['1'][0]['val'])  # Consumption
             power = unitResult['6100_40263F00']['1'][0]['val']
             if power is None:
                power = 0
             else:
                power = -int(power) # generated power is negative
       return power, generation
if __name__ == '__main__':
   power, generation = SMADASH(sys.argv[1]).read()
   print("Current power: %s; Total generation: %s" % (power,generation))

