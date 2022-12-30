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
user_id=str(sys.argv[2])
password=str(sys.argv[3])
client_id=str(sys.argv[4])
client_secret=str(sys.argv[5])
manufacturer=str(sys.argv[6])
soccalc=str(sys.argv[7])

# vehicle_vin is optional
vehicle_vin = False
if (len(sys.argv) > 8 ):
	vehicle_vin=str(sys.argv[8])

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

# oAuth2 login
data = {'realm': realm,'grant_type':'password','password':password,'username': user_id,'scope': scope}
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
f.write(responsetext.encode("utf-8"))
f.write(str(responestatus))
f.close()

psa_config = json.loads(responsetext)
acc_token = psa_config['access_token']

# get Vehicles
payload = {'client_id':client_id}
data = urllib.urlencode(payload) 
data = data.encode('Big5')
reg = 'https://api.groupe-psa.com/connectedcar/v4/user/vehicles?' + data
headers = {'Accept':'application/hal+json','Authorization': 'Bearer %s' % acc_token,'x-introspect-realm': realm}

f = open('/var/www/html/openWB/ramdisk/psareq2lp'+chargepoint, 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()

response=requests.get(reg,headers=headers )
responsetext  = response.text
responestatus = response.status_code

f = open('/var/www/html/openWB/ramdisk/psareply2lp'+chargepoint, 'w')
f.write(responsetext.encode("utf-8"))
f.write(str(responestatus))
f.close()

vehicle_response = json.loads(responsetext)
vehicles = vehicle_response['_embedded']['vehicles']

# Filter List for given VIN or select first entry
vehicle_selected = next(vehicle for vehicle in vehicles if vehicle['vin'] == vehicle_vin) if vehicle_vin else vehicles[0]
vehicle_id = vehicle_selected['id']

f = open('/var/www/html/openWB/ramdisk/psareply2filterVINlp'+chargepoint, 'w')
f.write('VIN: ' + str(vehicle_selected['vin']))
f.write(', ID: ' + str(vehicle_id))
f.close()

# get Vehicles Status
payload = {'client_id':client_id}
data = urllib.urlencode(payload) 
data = data.encode('Big5')
'/user/vehicles/{id}/status'
reg = 'https://api.groupe-psa.com/connectedcar/v4/user/vehicles/'  + vehicle_id + '/status?' + data
headers = {'Accept':'application/hal+json','Authorization': 'Bearer %s' % acc_token,'x-introspect-realm': realm}

f = open('/var/www/html/openWB/ramdisk/psareq3lp'+chargepoint, 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()

response=requests.get(reg,headers=headers )
responsetext  = response.text
responestatus = response.status_code

f = open('/var/www/html/openWB/ramdisk/psareply3lp'+chargepoint, 'w')
f.write(responsetext.encode("utf-8"))
f.write(str(responestatus))
f.close()

status_response = json.loads(responsetext)
energies = status_response['energy']

# Filter to only include type=Electric but remove all others. Seen type=Fuel and type=Electric being returned.
energy_selected = next(energy for energy in energies if energy['type'] == 'Electric')
soc = energy_selected['level']
fetchedsoctime = energy_selected['updatedAt']

if (int(soccalc) == 0):
	# manual calculation not enabled, using existing logic
	if (int(chargepoint) == 1):
		f = open('/var/www/html/openWB/ramdisk/soc', 'w')
	if (int(chargepoint) == 2):
		f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
	f.write(str(soc))
	f.close()
else:
	# manual calculation  enabled, using new logic with timestamp
	if (int(chargepoint) == 1):
		f = open('/var/www/html/openWB/ramdisk/psasoc', 'w')
	if (int(chargepoint) == 2):
		f = open('/var/www/html/openWB/ramdisk/psasoc1', 'w')
	f.write(str(soc))
	f.close()
	# getting timestamp of fetched SoC
	soct = time.strptime(fetchedsoctime, "%Y-%m-%dT%H:%M:%SZ")
	soctime = time.mktime(soct)
	# adding one hour to UTC to get CET
	soctime = soctime + 3600
	# checking for daylight saving time
	dst=time.localtime()
	if (dst.tm_isdst == 1):
		# adding one hour to fetched SoCtime in daylight saving time
		soctime = soctime + 3600
	# writing timestamp to ramdisk
	if (int(chargepoint) == 1):
		f = open('/var/www/html/openWB/ramdisk/psasoctime', 'w')
	if (int(chargepoint) == 2):
		f = open('/var/www/html/openWB/ramdisk/psasoctime1', 'w')
	f.write(str(int(soctime)))
	f.close()
