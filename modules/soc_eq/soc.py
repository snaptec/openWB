#!/usr/bin/python3

import os, requests, json, time

ramdir = '/var/www/html/openWB/ramdisk/'
moddir = '/var/www/html/openWB/modules/soc_eq/'

client_id     = os.environ.get('soc_eq_client_id', 'id')
client_secret = os.environ.get('soc_eq_client_secret', 'ecret')
VIN           = os.environ.get('soc_eq_vin', 'VIN')
soc_file      = os.environ.get('soc_file', ramdir + 'soc')
ChargePoint   = os.environ.get('CHARGEPOINT', '1')

tok_url   = "https://id.mercedes-benz.com/as/token.oauth2"
soc_url   = "https://api.mercedes-benz.com/vehicledata/v2/vehicles/"+VIN+"/resources/soc"
soc_url   = "https://api.mercedes-benz.com/vehicledata/v2/vehicles/"+VIN+"/containers/electricvehicle"
#range_url = "https://api.mercedes-benz.com/vehicledata/v2/vehicles/"+VIN+"/resources/rangeelectric"
print("SOC URL: " + soc_url)
#Get Access token expiry from file
fd = open(moddir + 'expires_lp' + str(ChargePoint),'r')
expires_in = fd.read().rstrip()
fd.close()


if int(expires_in) < int(time.time()):
  #Access Token is exired
  print("Acc Token Expired")
  fd = open(moddir + 'ref_tok_lp' + str(ChargePoint),'r')
  refresh_token = fd.read().rstrip()
  fd.close()
  
  #get new Access Token with referesh token
  data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token }
  ref = requests.post(tok_url, data=data, verify=True, allow_redirects=False, auth=(client_id, client_secret))
  print("Refresh Token Call:" + str(ref.status_code))
  #write HTTP reponse code to file
  try:
    fd = open(ramdir + 'soc_eq_lastresp','w')
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
    fd = open(moddir + 'acc_tok_lp' + str(ChargePoint),'w')
    fd.write(str(access_token))
    fd.close()

    fd = open(moddir + 'ref_tok_lp' + str(ChargePoint),'w')
    fd.write(str(refresh_token))
    fd.close()

    fd = open(moddir + 'expires_lp' + str(ChargePoint),'w')
    fd.write(str(expires_in))
    fd.close()
  else:
    print("Error getting Acc after Refresh: " + str(ref.status_code))
    exit(1)

#get access token from file	
fd = open(moddir + 'acc_tok_lp' + str(ChargePoint),'r')
access_token = fd.read().rstrip()
fd.close()

#call API for SoC
header = {'authorization': 'Bearer ' + access_token}
req_soc = requests.get(soc_url, headers=header, verify=True)
print("SOC Request: " + str(req_soc.status_code))
print("SOC Response: " + req_soc.text)

#write HTTP reponse code to file
try:
  fd = open(ramdir + 'soc_eq_lastresp','w')
  fd.write(str(req_soc.status_code))
  fd.close()
except:
  fd.close()

if req_soc.status_code == 200:
  #valid Response
  res = json.loads(req_soc.text)
  #Extract SoC value and write to file
  #for entry in res:
    #print(entry)
    #if entry == 'soc':
     #soc = entry['soc']['value']
    #elif entry == 'rangeelectric':
     #range = entry['rangeelectric']['value']

  soc = res[0]['soc']['value']
  range = res[1]['rangeelectric']['value']
  print("SOC: " + soc + " RANGE: " + range)
  fd = open(soc_file,'w')
  fd.write(str(soc))
  fd.close()

exit(0)
