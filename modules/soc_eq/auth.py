#!/usr/bin/python3

import requests, json, sys, time, os, time

#call parameters
ChargePoint = str(sys.argv[1]) 
code        = str(sys.argv[2]) 

moddir = '/var/www/html/openWB/modules/soc_eq/'


client_id = ""
client_secret = ""
callback = ""

#get SoC module config from openWB cofig
fd = open('/var/www/html/openWB/openwb.conf','r')
for line in fd:
  try: 
    (key, val) = line.rstrip().split("=")
    if key == "soc_eq_client_id_lp" + str(ChargePoint):
      client_id = val
    if key == "soc_eq_client_secret_lp" + str(ChargePoint):
      client_secret = val
    if key == "soc_eq_cb_lp" + str(ChargePoint):
      callback = val
  except:
    val = ""

fd.close()

tok_url  = "https://id.mercedes-benz.com/as/token.oauth2"

data = {'grant_type': 'authorization_code', 'code': str(code), 'redirect_uri': callback}
#call API to get Access/Refresh tokens
act = requests.post(tok_url, data=data, verify=True, allow_redirects=False, auth=(client_id, client_secret))

if act.status_code == 200:
  #valid Response
  toks = json.loads(act.text)
  access_token = toks['access_token']
  refresh_token = toks['refresh_token']
	#write tokens to files
  fd = open(moddir + 'acc_tok_lp' + str(ChargePoint),'w')
  fd.write(str(access_token))
  fd.close()

  fd = open(moddir + 'ref_tok_lp' + str(ChargePoint),'w')
  fd.write(str(refresh_token))
  fd.close()
	#write token expiy to file
  fd = open(moddir + 'expires_lp' + str(ChargePoint),'w')
  fd.write(str(int(time.time())))
  fd.close()

print( "<h1>Antwort (200 ist OK, alles andere ein Fehler): " + str(act.status_code) + "</h1>")
