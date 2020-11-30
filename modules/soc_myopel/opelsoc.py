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

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S opelsoc lp1", named_tuple) 
userID=str(sys.argv[1])
password=str(sys.argv[2])
client_id=str(sys.argv[3])
client_secret=str(sys.argv[4])

userpass = client_id + ':' + client_secret 
encoded_u = base64.b64encode(userpass.encode()).decode() 
header1 = str('Basic %s' % encoded_u)
scope = 'openid profile'
brand = 'opel.com'
realm = 'clientsB2COpel'
vin='?'
data = {'realm': realm,'grant_type':'password','password':password,'username': userID,'scope': scope}
headers = {'Content-Type':'application/x-www-form-urlencoded','Authorization': 'Basic %s' % encoded_u}
reg = 'https://idpcvs.' + brand + '/am/oauth2/access_token'
f = open('/var/www/html/openWB/ramdisk/opelreq1lp1', 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()
response=requests.post(reg,  data=data, headers=headers )
responsetext  = response.text
responestatus = response.status_code
f = open('/var/www/html/openWB/ramdisk/opelreply1lp1', 'w')
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
f = open('/var/www/html/openWB/ramdisk/opelreq2lp1', 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()
response=requests.get(reg,headers=headers )
f = open('/var/www/html/openWB/ramdisk/opelreply2lp1', 'w')
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
f = open('/var/www/html/openWB/ramdisk/opelreq3lp1', 'w')
f.write(str(reg))
f.write(str(data))
f.write(str(headers))
f.close()
response=requests.get(reg,headers=headers )
f = open('/var/www/html/openWB/ramdisk/opelreply3lp1', 'w')
responsetext  = response.text
responestatus = response.status_code
f.write(str(responsetext))
f.write(str(responestatus))
f.close()
batt = json.loads(responsetext)
soc = batt['energy'][0]['level']
#print(time_string,'soc lp1',soc)
f = open('/var/www/html/openWB/ramdisk/soc', 'w')
f.write(str(soc))
f.close()
