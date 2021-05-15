#!/usr/bin/python
import sys
import os
import time
import getopt
import json
import urllib
import urllib2 
import requests

loginID=str(sys.argv[1])
password=str(sys.argv[2])
location=str(sys.argv[3])
country=str(sys.argv[4])
vin=str(sys.argv[5])
chargepoint=str(sys.argv[6])

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S myrenault wake lp"+chargepoint, named_tuple)
f = open('/var/www/html/openWB/ramdisk/zoereply1lp'+chargepoint, 'r')
android_config = json.loads(f.read())
f.close()
gigyarooturl = android_config['servers']['gigyaProd']['target'] 
gigyaapikey = android_config['servers']['gigyaProd']['apikey'] 
kamereonrooturl = android_config['servers']['wiredProd']['target']
#kamereonapikey = android_config['servers']['wiredProd']['apikey']
kamereonapikey = 'Ae9FDWugRxZQAGm3Sxgk7uJn6Q4CGEA2'
#print(time_string, 'gigyarooturl',gigyarooturl,gigyaapikey,kamereonrooturl,kamereonapikey)
#
f = open('/var/www/html/openWB/ramdisk/zoereply4lp'+chargepoint, 'r')
gigya_jwt = json.loads(f.read())
f.close()
gigya_jwttoken= gigya_jwt['id_token']
#print(time_string,'gigya_jwttoken',gigya_jwttoken)
#
f = open('/var/www/html/openWB/ramdisk/zoereply5lp'+chargepoint, 'r')
kamereon_per = json.loads(f.read())
f.close()
kamereonaccountid = kamereon_per['accounts'][0]['accountId']
#print(time_string,'kamereonaccountid',kamereonaccountid)
#

#f = open('/var/www/html/openWB/ramdisk/zoereply6lp'+chargepoint, 'r')
#kamereon_token = json.loads(f.read())
#f.close()
#kamereonaccesstoken = kamereon_token['accessToken']
#print(time_string,'kamereonaccesstoken',kamereonaccesstoken)
#
f = open('/var/www/html/openWB/ramdisk/zoereply7lp'+chargepoint, 'r')
vehic = json.loads(f.read())
f.close()
if len(vin) < 10:
    vin = vehic['vehicleLinks'][0]['vin']
print(time_string,'vin wakeup',vin)
payload = {"data":{"type":"ChargingStart","attributes":{"action":"start"}}}
data=json.dumps(payload)
payloadc = {'country': country} 
#head1 = 'Bearer ' + kamereonaccesstoken
#headers = {'Content-Type':'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey,'x-kamereon-authorization': head1} 
headers = {'Content-Type':'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey} 
reg= kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v1/cars/' + vin + '/actions/charging-start'
response=requests.post(reg, params=payloadc, data=data, headers=headers)
responsetext  = response.text
f = open('/var/www/html/openWB/ramdisk/zoereply10lp'+chargepoint, 'w')
f.write(str(responsetext))
f.close()
f = open('/var/www/html/openWB/ramdisk/zoereply11lp'+chargepoint, 'w')
f.write(str(reg))
f.write(str(payloadc))
f.write(str(data))
f.write(str(headers))
f.close()
