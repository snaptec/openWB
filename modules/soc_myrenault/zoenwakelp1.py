#!/usr/bin/python
import sys
import os
import time
import getopt
import json
import urllib
import urllib2 

loginID=str(sys.argv[1])
password=str(sys.argv[2])
location=str(sys.argv[3])
country=str(sys.argv[4])

#handler=urllib2.HTTPSHandler(debuglevel=1) 
#opener = urllib2.build_opener(handler) 
#urllib2.install_opener(opener)

#reg=urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S myrenault wake lp1", named_tuple)
f = open('/var/www/html/openWB/ramdisk/zoereply1lp1', 'r')
android_config = json.loads(f.read())
f.close()
gigyarooturl = android_config['servers']['gigyaProd']['target'] 
gigyaapikey = android_config['servers']['gigyaProd']['apikey'] 
kamereonrooturl = android_config['servers']['wiredProd']['target']
kamereonapikey = android_config['servers']['wiredProd']['apikey']
#print(time_string, 'gigyarooturl',gigyarooturl,gigyaapikey,kamereonrooturl,kamereonapikey)
#
f = open('/var/www/html/openWB/ramdisk/zoereply4lp1', 'r')
gigya_jwt = json.loads(f.read())
f.close()
gigya_jwttoken= gigya_jwt['id_token']
#print(time_string,'gigya_jwttoken',gigya_jwttoken)
#
f = open('/var/www/html/openWB/ramdisk/zoereply6lp1', 'r')
kamereon_token = json.loads(f.read())
f.close()
kamereonaccesstoken = kamereon_token['accessToken']
#print(time_string,'kamereonaccesstoken',kamereonaccesstoken)
#
f = open('/var/www/html/openWB/ramdisk/zoereply7lp1', 'r')
vehic = json.loads(f.read())
f.close()
vin = vehic['vehicleLinks'][0]['vin']
print(time_string,'vin wakeup',vin)

payload = {"data":{"type":"ChargingStart","attributes":{"action":"start"}}}
data=json.dumps(payload)
payloadc = {'country': country} 
datac = urllib.urlencode(payloadc) 
datac = datac.encode('Big5')
#data = urllib.urlencode(payload) 
#print ('data' ,data)
head1 = ' Bearer ' + kamereonaccesstoken
headers = {'Content-Type':'application/vnd.api+json','x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey,'x-kamereon-authorization': head1} 
reg = urllib2.Request(kamereonrooturl + '/commerce/v1/accounts/kmr/remote-services/car-adapter/v1/cars/' + vin + '/actions/charging-start?' + datac,data=data,headers=headers)
response = urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply10lp1', 'w')
f.write(str(responsetext))
f.close()
