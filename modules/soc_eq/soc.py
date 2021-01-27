#!/usr/bin/python3

import os, requests, json, time, sys, os
from datetime import datetime, timezone
from requests.exceptions import Timeout

ramdiskdir = '/var/www/html/openWB/ramdisk/'
moduledir = '/var/www/html/openWB/modules/soc_eq/'

req_timeout=(15,15) #Timeout for requests in seconds

client_id     = str(sys.argv[1])
client_secret = str(sys.argv[2])
VIN           = str(sys.argv[3])
soc_file      = str(sys.argv[4])
ChargePoint   = str(sys.argv[5])

Debug         = int(os.environ.get('debug'))

def socDebugLog(message):
    local_time = datetime.now(timezone.utc).astimezone()
#    print(local_time.isoformat() +": Lp" +ChargePoint + ": " + message)
    print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") +": Lp" +ChargePoint + ": " + message)

if Debug >= 1:
    socDebugLog("Debug Level: " + str(Debug))
if Debug >= 1:
    socDebugLog("client: " + client_id)

tok_url   = "https://id.mercedes-benz.com/as/token.oauth2"
soc_url   = "https://api.mercedes-benz.com/vehicledata/v2/vehicles/"+VIN+"/containers/electricvehicle"

if Debug >= 1:
    socDebugLog("SOC URL: " + soc_url)

#Get Access token from file

fd = open(moduledir + 'soc_eq_acc_lp' + str(ChargePoint),'r')
try:
    tok = json.load(fd)
    access_token = tok['access_token']
except ValueError:
    socDebugLog("ERROR: Access Token not found. Please use Link 'HIER bei Mercedes Me' anmelden in LP Configuration")
    exit(1)        
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

  elif ref.status_code == 400:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (Bad Request)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 401:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (Invalid or missing authorization in header)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 402:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (Payment required)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 403:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (Forbidden)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 404:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (The requested resource was not found, e.g.: the selected vehicle could not be found)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 429:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (The service received too many requests in a given amount of time)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 500:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (The service received too many requests in a given amount of time)")
    socDebugLog(ref.text)
    exit(1)
  elif ref.status_code == 503:
    socDebugLog("Refresh fehlgeschlagen Code: " + str(ref.status_code) + " (The server is unable to service the request due to a temporary unavailability condition)")
    socDebugLog(ref.text)
    exit(1)
  else:
    socDebugLog("Refresh fehlgeschlagen unbekannter Code: " + str(ref.status_code))
    socDebugLog(ref.text)
    exit(1)

#call API for SoC
header = {'authorization': 'Bearer ' + access_token}
try:

    #req_soc = requests.get(soc_url, headers=header, verify=True)
    req_soc = requests.get(soc_url, headers=header, verify=True, timeout=req_timeout)
    #req_soc = requests.get(soc_url, headers=header, verify=True, timeout=(5,10))
except Timeout:
    socDebugLog("Soc Request Timed Out")
    exit(5)
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
  res = json.loads(req_soc.text)
  #Extract SoC value and write to file
  for entry in res:
      for values in entry:
          if values == "soc":
              soc = entry[values]['value']
          elif values == "rangeelectric":
              range = entry[values]['value']
          else:
              socDebugLog("unknown entry: " + entry)

  #soc = res[0]['soc']['value']
  #range = res[1]['rangeelectric']['value']
  socDebugLog("SOC: " + soc + " RANGE: " + range)
  fd = open(soc_file,'w')
  fd.write(str(soc))
  fd.close()
  
elif req_soc.status_code == 204:
  # this is not an error code. Nothing to fetch so nothing to update and no reason to exit(1)  
  socDebugLog("SoC Request Code: " + str(req_soc.status_code) + " (no data is available for the resource)")
  socDebugLog(req_soc.text)
elif req_soc.status_code == 400:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (Bad Request)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 401:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (Invalid or missing authorization in header)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 402:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (Payment required)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 403:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (Forbidden)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 404:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (The requested resource was not found, e.g.: the selected vehicle could not be found)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 429:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (The service received too many requests in a given amount of time)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 500:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (The service received too many requests in a given amount of time)")
  socDebugLog(req_soc.text)
  exit(1)
elif req_soc.status_code == 503:
  socDebugLog("SoC Request fehlgeschlagen Code: " + str(req_soc.status_code) + " (The server is unable to service the request due to a temporary unavailability condition)")
  socDebugLog(req_soc.text)
  exit(1)
else:
  socDebugLog("SoC Request fehlgeschlagen unbekannter Code: " + str(req_soc.status_code))
  socDebugLog(req_soc.text)
  exit(1)

if Debug >= 2:
    socDebugLog("SoC EQ Ende ohne Fehler")
exit(0)
