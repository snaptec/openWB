#!/usr/bin/python3

import sys
import os
import time
import getopt
import json
import urllib
import requests
import base64
import logging
#these two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError: # Python 2
    import httplib as http_client
# to enable http trace set swbedug = 1
swdebug = 0
if swdebug == 1:
   http_client.HTTPConnection.debuglevel = 1
   
   logging.basicConfig()
   logging.getLogger().setLevel(logging.DEBUG)
   requests_log = logging.getLogger("requests.packages.urllib3")
   requests_log.setLevel(logging.DEBUG)
   requests_log.propagate = True

chargepoint=str(sys.argv[1])
userID=str(sys.argv[2])
password=str(sys.argv[3])
client_id=str(sys.argv[4])
client_secret=str(sys.argv[5])
manufacturer=str(sys.argv[6])
soccalc=str(sys.argv[7])

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S psasoc lp"+chargepoint, named_tuple)

userpass = client_id + ':' + client_secret 
encoded_u = base64.b64encode(userpass.encode()).decode() 
header1 = str('Basic %s' % encoded_u)
scope = 'openid profile'
if (manufacturer == "Peugeot"):
	brand = 'peugeot.com'
	realm = 'clientsB2CPeugeot'
elif (manufacturer == "Citroen"):
	brand = 'citroen.com'
	realm = 'clientsB2CCitroen'
elif (manufacturer == "DS"):
	brand = 'driveds.com'
	realm = 'clientsB2CDS'
elif (manufacturer == "Opel"):
	brand = 'opel.com'
	realm = 'clientsB2COpel'
elif (manufacturer == "Vauxhall"):
	brand = 'vauxhall.co.uk'
	realm = 'clientsB2CVauxhall'
vin='?'
data = {'realm': realm,'grant_type':'password','password':password,'username': userID,'scope': scope}
headers = {'Content-Type':'application/x-www-form-urlencoded','Authorization': 'Basic %s' % encoded_u}
reg = 'https://idpcvs.' + brand + '/am/oauth2/access_token'
f = open('/var/www/html/openWB/ramdisk/psareq1lp'+chargepoint, 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()
response=requests.post(reg,  data=data, headers=headers )
responsetext  = response.text
responestatus = response.status_code
f = open('/var/www/html/openWB/ramdisk/psareply1lp'+chargepoint, 'w')
f.write(str(responsetext))
f.write(str(responestatus))
f.close()
psa_config = json.loads(responsetext)
acc_token = psa_config['access_token']
payload = {'client_id':client_id}
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg = 'https://api.groupe-psa.com/connectedcar/v4/user/vehicles?' + data
headers = {'Accept':'application/hal+json','Authorization': 'Bearer %s' % acc_token,'x-introspect-realm ': realm}
f = open('/var/www/html/openWB/ramdisk/psareq2lp'+chargepoint, 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()
response=requests.get(reg,headers=headers )
f = open('/var/www/html/openWB/ramdisk/psareply2lp'+chargepoint, 'w')
responsetext  = response.text
responestatus = response.status_code
f.write(str(responsetext))
f.write(str(responestatus))
f.close()
vin_list = json.loads(responsetext)
vin_id  = vin_list ['_embedded']['vehicles'][0]['id']
vin_vin  = vin_list ['_embedded']['vehicles'][0]['vin']
payload = {'client_id':client_id}
data = urllib.urlencode(payload) 
data = data.encode('Big5')
'/user/vehicles/{id}/status'
reg = 'https://api.groupe-psa.com/connectedcar/v4/user/vehicles/'  + vin_id + '/status?' + data
headers = {'Accept':'application/hal+json','Authorization': 'Bearer %s' % acc_token,'x-introspect-realm ': realm}
f = open('/var/www/html/openWB/ramdisk/psareq3lp'+chargepoint, 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()
response=requests.get(reg,headers=headers )
f = open('/var/www/html/openWB/ramdisk/psareply3lp'+chargepoint, 'w')
responsetext  = response.text
responestatus = response.status_code
f.write(str(responsetext))
f.write(str(responestatus))
f.close()
batt = json.loads(responsetext)
soc = batt['energy'][0]['level']
#print(time_string,'soc lp'+chargepoint,soc)

if (int(soccalc) == 0):
	#manual calculation not enabled, using existing logic
	if (int(chargepoint) == 1):
		f = open('/var/www/html/openWB/ramdisk/soc', 'w')
	if (int(chargepoint) == 2):
		f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
	f.write(str(soc))
	f.close()
else:
	#manual calculation  enabled, using new logic with timestamp
	if (int(chargepoint) == 1):
		f = open('/var/www/html/openWB/ramdisk/psasoc', 'w')
	if (int(chargepoint) == 2):
		f = open('/var/www/html/openWB/ramdisk/psasoc1', 'w')
	f.write(str(soc))
	f.close()
	# getting timestamp of fetched SoC
	fetchedsoctime = batt['energy'][0]['updatedAt']
	soct = time.strptime(fetchedsoctime, "%Y-%m-%dT%H:%M:%SZ")
	soctime = time.mktime(soct)
	# checking for daylight saving time
	dst=time.localtime()
	if (dst.tm_isdst == 0):
		# adding one hour to fetched SoCtime if needed
		soctime = soctime + 3600
	# writing timestamp to ramdisk
	if (int(chargepoint) == 1):
		f = open('/var/www/html/openWB/ramdisk/psasoctime', 'w')
	if (int(chargepoint) == 2):
		f = open('/var/www/html/openWB/ramdisk/psasoctime1', 'w')
	f.write(str(int(soctime)))
	f.close()
