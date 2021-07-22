#!/usr/bin/python3

import os, requests, json, time, sys, os
from datetime import datetime, timezone
from requests.exceptions import Timeout, RequestException
from json import JSONDecodeError

ramdiskdir = '/var/www/html/openWB/ramdisk/'
moduledir = '/var/www/html/openWB/modules/soc_eq/'

req_timeout=(30,30) #timeout for requests in seconds

client_id     = str(sys.argv[1])
client_secret = str(sys.argv[2])
VIN           = str(sys.argv[3])
soc_file      = str(sys.argv[4])
ChargePoint   = str(sys.argv[5])

Debug         = int(os.environ.get('debug'))
myPid         = str(os.getpid())

tok_url   = "https://id.mercedes-benz.com/as/token.oauth2"
soc_url   = "https://api.mercedes-benz.com/vehicledata/v2/vehicles/"+VIN+"/containers/electricvehicle"


soc = None
range = None

def socDebugLog(message):
	local_time = datetime.now(timezone.utc).astimezone()
	print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") +": Lp" +ChargePoint + ": PID:"+ myPid + ": " + message)

def handleResponse(what, status_code, text):
	if status_code == 204:
		# this is not an error code. Nothing to fetch so nothing to update and no reason to exit(1)  
		socDebugLog(what + " Request Code: " + str(status_code) + " (no data is available for the resource)")
		socDebugLog(text)
	elif status_code == 400:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (Bad Request)")
		socDebugLog(text)
		exit(1)
	elif status_code == 401:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (Invalid or missing authorization in header)")
		socDebugLog(text)
		exit(1)
	elif status_code == 402:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (Payment required)")
		socDebugLog(text)
		exit(1)
	elif status_code == 403:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (Forbidden)")
		socDebugLog(text)
		exit(1)
	elif status_code == 404:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (The requested resource was not found, e.g.: the selected vehicle could not be found)")
		socDebugLog(text)
		exit(1)
	elif status_code == 429:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (The service received too many requests in a given amount of time)")
		socDebugLog(text)
		exit(1)
	elif status_code == 500:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (The service received too many requests in a given amount of time)")
		socDebugLog(text)
		exit(1)
	elif status_code == 503:
		socDebugLog(what + " Request fehlgeschlagen Code: " + str(status_code) + " (The server is unable to service the request due to a temporary unavailability condition)")
		socDebugLog(text)
		exit(1)
	else:
		socDebugLog(what + " Request fehlgeschlagen unbekannter Code: " + str(status_code))
		socDebugLog(text)
		exit(1)

if Debug >= 1:
	socDebugLog("Debug Level: " + str(Debug))
if Debug >= 1:
	socDebugLog("client: " + client_id)


if Debug >= 2:
	socDebugLog("SOC URL: " + soc_url)

#Get Access token from file

fd = open(moduledir + 'soc_eq_acc_lp' + str(ChargePoint),'r')
try:
	tok = json.load(fd)
	access_token = tok['access_token']
except ValueError:
	socDebugLog("ERROR: Access Token not found. Please use Link 'HIER bei Mercedes Me' anmelden in LP Configuration")
	exit(3)        
refresh_token = tok['refresh_token']
expires_in = tok['expires_in']
fd.close()

#socDebugLog("Expire in: " str((int(expires_in)-int(time.time())))

if int(expires_in) < int(time.time()):
	#Access Token is exired
	if Debug >= 1:
		socDebugLog("Acc Token Expired")
  
	#get new Access Token with referesh token
	data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token }
	ref = requests.post(tok_url, data=data, verify=True, allow_redirects=False, auth=(client_id, client_secret), timeout=req_timeout)
	if Debug >= 1:
		socDebugLog("Refresh Token Call:" + str(ref.status_code))
		socDebugLog("Refresh Token Text:" + str(ref.text))


	#write HTTP reponse code to file
	try:
		fd = open(ramdiskdir + 'soc_eq_lastresp','w')
		fd.write(str(ref.status_code))
		fd.close()
	except:
		fd.close()


	if ref.status_code == 200:
		#valid response
		tok = json.loads(ref.text)

		access_token = tok['access_token']
		refresh_token = tok['refresh_token']
		expires_in = tok['expires_in'] - 60 + int(time.time())

		#write new tokens
    
		fd = open(moduledir + 'soc_eq_acc_lp' + str(ChargePoint),'w')
		json.dump({'expires_in' : expires_in, 'refresh_token' : refresh_token, 'access_token' : access_token}, fd)
		fd.close()
	else:
		handleResponse("Refresh",ref.status_code,ref.text)

#call API for SoC
header = {'authorization': 'Bearer ' + access_token}
try:

	req_soc = requests.get(soc_url, headers=header, verify=True)
	#req_soc = requests.get(soc_url, headers=header, verify=True, timeout=req_timeout)

except Timeout:
	socDebugLog("Soc Request Timed Out")
	exit(2)

except RequestException:
	socDebugLog("Soc Request Request Exception occured " + soc_url)
	exit(2)

if Debug >= 1:
	socDebugLog("SOC Request: " + str(req_soc.status_code))
	socDebugLog("SOC Response: " + req_soc.text)

#write HTTP reponse code to file
try:
	fd = open(ramdiskdir + 'soc_eq_lastresp','w')
	fd.write(str(req_soc.status_code))
	fd.close()
except:
	fd.close()

if req_soc.status_code == 200:
	#valid Response
	try:
		res = json.loads(req_soc.text)
	except JSONDecodeError:
		socDebugLog("Soc Response NO VALID JSON " + req_soc.text)
		exit(2)

	#Extract SoC value and write to file
	for entry in res:
		for values in entry:
			if values == "soc":
				soc = entry[values]['value']
			elif values == "rangeelectric":
				range = entry[values]['value']
			else:
				socDebugLog("unknown entry: " + entry)
	if not soc:
		socDebugLog("SoC Value not filled " + req_soc.text)
		soc = "0"
	if not range:
		socDebugLog("RangeElectric Value not filled " + req_soc.text)
		range = "0"
	socDebugLog("SOC: " + soc + " RANGE: " + range)
	fd = open(soc_file,'w')
	fd.write(str(soc))
	fd.close()
  
else:
	handleResponse("SoC",req_soc.status_code,req_soc.text)

if Debug >= 2:
	socDebugLog("SoC EQ Ende ohne Fehler")
exit(0)
