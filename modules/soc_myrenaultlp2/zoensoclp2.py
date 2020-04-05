#!/usr/bin/python
import sys
import os
import time
import getopt
import json
import urllib
import urllib2 

#handler=urllib2.HTTPSHandler(debuglevel=1) 
#opener = urllib2.build_opener(handler) 
#urllib2.install_opener(opener)

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S myrenault lp2", named_tuple) 
loginID=str(sys.argv[1])
password=str(sys.argv[2])
location=str(sys.argv[3])
country=str(sys.argv[4])
vin='?'
#vin = '?'
#print(time_string, ' start ', loginID)
#
reg='https://renault-wrd-prod-1-euw1-myrapp-one.s3-eu-west-1.amazonaws.com/configuration/android/config_' + location + '.json'
#print ('c1',reg)
f = open('/var/www/html/openWB/ramdisk/zoereq1lp2', 'w')
f.write(str(reg))
f.close()
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply1lp2', 'w')
f.write(str(responsetext))
f.close()
android_config = json.loads(responsetext)
gigyarooturl = android_config['servers']['gigyaProd']['target'] 
gigyaapikey = android_config['servers']['gigyaProd']['apikey'] 
kamereonrooturl = android_config['servers']['wiredProd']['target']
kamereonapikey = android_config['servers']['wiredProd']['apikey']
#print(time_string, 'gigyarooturl',gigyarooturl,gigyaapikey,kamereonrooturl,kamereonapikey)
#
payload = {'loginID': loginID, 'password': password, 'apiKey': gigyaapikey} 
data = urllib.urlencode(payload) 
data = data.encode('Big5') 
reg= gigyarooturl + '/accounts.login?' + data
#print ('c2',reg)
f = open('/var/www/html/openWB/ramdisk/zoereq2lp2', 'w')
f.write(str(reg))
f.close()
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply2lp2', 'w')
f.write(str(responsetext))
f.close()
gigya_session = json.loads(responsetext)
gigyacookievalue = gigya_session['sessionInfo']['cookieValue']
#print(time_string,'gigyacookievalue',gigyacookievalue)
#
payload = {'oauth_token': gigyacookievalue} 
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg= gigyarooturl + '/accounts.getAccountInfo?' + data
f = open('/var/www/html/openWB/ramdisk/zoereq3lp2', 'w')
f.write(str(reg))
f.close()
#print('c3',reg)
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply3lp2', 'w')
f.write(str(responsetext))
f.close()
gigya_account = json.loads(responsetext)
kamereonpersonid = gigya_account['data']['personId']
#print(time_string,'kamereonpersonid',kamereonpersonid)
payload = {'oauth_token': gigyacookievalue, 'fields': 'data.personId,data.gigyaDataCenter', 'expiration': 900} 
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg= gigyarooturl + '/accounts.getJWT?' + data
f = open('/var/www/html/openWB/ramdisk/zoereq4lp2', 'w')
f.write(str(reg))
f.close()
#print('c4',reg)
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply4lp2', 'w')
f.write(str(responsetext))
f.close()
gigya_jwt = json.loads(responsetext)
gigya_jwttoken= gigya_jwt['id_token']
#print(time_string,'gigya_jwttoken',gigya_jwttoken)
#
payload = {'country': country} 
headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey} 
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg = urllib2.Request(kamereonrooturl + '/commerce/v1/persons/' + kamereonpersonid + '?' + data)
reg.add_header('x-gigya-id_token',gigya_jwttoken)
reg.add_header('apikey', kamereonapikey)
#print('c5',reg)
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply5lp2', 'w')
f.write(str(responsetext))
f.close()
kamereon_per = json.loads(responsetext)
kamereonaccountid = kamereon_per['accounts'][0]['accountId']
#print(time_string,'kamereonaccountid',kamereonaccountid)
#
payload = {'country': country} 
headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey} 
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg = urllib2.Request(kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/token?'  + data)
reg.add_header('x-gigya-id_token',gigya_jwttoken)
reg.add_header('apikey', kamereonapikey)
#print('c6',reg)
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply6lp2', 'w')
f.write(str(responsetext))
f.close()
kamereon_token = json.loads(responsetext)
kamereonaccesstoken = kamereon_token['accessToken']
#print(time_string,'kamereonaccesstoken',kamereonaccesstoken)
#
payload = {'country': country} 
headers = {'x-gigya-id_token': gigya_jwttoken, 'apikey': kamereonapikey} 
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg = urllib2.Request(kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/vehicles?'  + data)
reg.add_header('x-gigya-id_token',gigya_jwttoken)
reg.add_header('apikey', kamereonapikey)
reg.add_header('x-kamereon-authorization', ' Bearer ' + kamereonaccesstoken)
response= urllib2.urlopen(reg)
responsetext  = response.read()
vehic = json.loads(responsetext)
if len(vin) < 10:
    vin = vehic['vehicleLinks'][0]['vin']
f = open('/var/www/html/openWB/ramdisk/zoereply7lp2', 'w')
f.write(str(responsetext))
f.close()
# new
payload = {'country': country} 
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg = urllib2.Request(kamereonrooturl + '/commerce/v1/accounts/' + kamereonaccountid + '/kamereon/kca/car-adapter/v2/cars/' + vin + '/battery-status?'  + data)
reg.add_header('x-gigya-id_token',gigya_jwttoken)
reg.add_header('apikey', kamereonapikey)
reg.add_header('x-kamereon-authorization', ' Bearer ' + kamereonaccesstoken)
#print('c7',reg)
response= urllib2.urlopen(reg)
responsetext  = response.read()
f = open('/var/www/html/openWB/ramdisk/zoereply8lp2', 'w')
f.write(str(responsetext))
f.close()
batt = json.loads(responsetext)
soc = batt['data']['attributes']['batteryLevel']
#print(time_string,'soc lp2',soc)
f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
f.write(str(soc))
f.close()



