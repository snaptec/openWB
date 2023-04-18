#!/usr/bin/python
import sys
import time
import json
import requests

loginID = str(sys.argv[1])
password = str(sys.argv[2])
location = str(sys.argv[3])
country = str(sys.argv[4])
vin = str(sys.argv[5])
chargepoint = str(sys.argv[6])

named_tuple = time.localtime()
time_string = time.strftime("%m/%d/%Y, %H:%M:%S myrenault wake lp"+chargepoint, named_tuple)
gigyarooturl = 'https://accounts.eu1.gigya.com'
gigyaapi = '3_7PLksOyBRkHv126x5WhHb-5pqC1qFR8pQjxSeLB6nhAnPERTUlwnYoznHSxwX668'
kamereonrooturl = 'https://api-wired-prod-1-euw1.wrd-aws.com'
kamereonapikey = 'YjkKtHmGfaceeuExUDKGxrLZGGvtVS0J'
with open('/var/www/html/openWB/ramdisk/zoereply4lp'+chargepoint, 'r') as f:
    gigya_jwt = json.loads(f.read())
gigya_jwttoken = gigya_jwt['id_token']
with open('/var/www/html/openWB/ramdisk/zoereply5lp'+chargepoint, 'r') as f:
    kamereon_per = json.loads(f.read())
kamereonaccountid = kamereon_per['accounts'][0]['accountId']
with open('/var/www/html/openWB/ramdisk/zoereply7lp'+chargepoint, 'r') as f:
    vehic = json.loads(f.read())
if len(vin) < 10:
    vin = vehic['vehicleLinks'][0]['vin']
print(time_string, 'vin wakeup', vin)
payload = {"data": {"type": "ChargingStart", "attributes": {"action": "start"}}}
data = json.dumps(payload)
payloadc = {'country': country}
headers = {'Content-Type': 'application/vnd.api+json', 'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey}
reg = kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/'
reg += vin + '/actions/charging-start'
response = requests.post(reg, params=payloadc, data=data, headers=headers)
responsetext = response.text
with open('/var/www/html/openWB/ramdisk/zoereply10lp'+chargepoint, 'w') as f:
    f.write(str(responsetext))
with open('/var/www/html/openWB/ramdisk/zoereply11lp'+chargepoint, 'w') as f:
    f.write(str(reg))
    f.write(str(payloadc))
    f.write(str(data))
    f.write(str(headers))
