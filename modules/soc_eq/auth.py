#!/usr/bin/python3

import requests, json, sys, time, os, time

#call parameters
ChargePoint = str(sys.argv[1]) 
code        = str(sys.argv[2]) 

moddir = '/var/www/html/openWB/modules/soc_eq/'
print("<html>")

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
if act.status_code == 200:
	print( "Anmeldung erfolgreich! <br/>Sie können das Fenster schließen." )
elif act.status_code == 400:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (Bad Request)")
elif act.status_code == 401:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (Invalid or missing authorization in header)")	
elif act.status_code == 402:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (Payment required)")		
elif act.status_code == 403:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (Forbidden)")			
elif act.status_code == 404:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (The requested resource was not found, e.g.: the selected vehicle could not be found)")				
elif act.status_code == 429:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (The service received too many requests in a given amount of time)")					
elif act.status_code == 500:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (The service received too many requests in a given amount of time)")						
elif act.status_code == 503:
	print("Anmeldung Fehlgeschlagen Code: " + str(act.status_code) + " (The server is unable to service the request due to a temporary unavailability condition)")					
else:
	print("Anmeldung Fehlgeschlagen unbekannter Code: " + str(act.status_code))					
	
print("</html>")