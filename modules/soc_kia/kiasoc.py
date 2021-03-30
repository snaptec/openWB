import sys
import time
import requests
import uuid
import json
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
import stamps

email = str(sys.argv[1])
password = str(sys.argv[2])
pin = str(sys.argv[3])
vin = str(sys.argv[4])
socfile = str(sys.argv[5])
soctimefile = str(sys.argv[6])

# Kia API expects a stamp. The solution to handle this problem was implemented for bluelinky and is used here as well.
# For more information: https://github.com/Hacksore/bluelinky/pull/105
# A random stamp from the list in the file stamps.py is used here.
# Instruction for generating new stamps can be found in stamps.py
#
def get_stamp(): 
    return stamps.stamps[random.randint(0,len(stamps.stamps)-1)]

def main():
    #deviceID
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/spa/notifications/register'
    headers = {
        'ccsp-service-id': 'fdc85c00-0a2f-4c64-bcb4-2cfb1500730a',
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': '80',
        'Host': 'prd.eu-ccapi.kia.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': get_stamp()}
    data = {"pushRegId":"1","pushType":"GCM","uuid": str(uuid.uuid1())}
    response = requests.post(url, json = data, headers = headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        deviceId = response['resMsg']['deviceId']
        print(deviceId)
    else:
        print('NOK deviceID')
        return

    #cookie for login
    session = requests.Session()
    response = session.get('https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/authorize?response_type=code&state=test&client_id=fdc85c00-0a2f-4c64-bcb4-2cfb1500730a&redirect_uri=https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/redirect')
    if response.status_code == 200:
        cookies = session.cookies.get_dict()
        #print(cookies)
    else:
        print('NOK cookie for login')
        return

    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/user/language' 
    headers = {'Content-type': 'application/json'}
    data = {"lang": "en"}
    response = requests.post(url, json = data, headers = headers, cookies = cookies)

    #login
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/user/signin' 
    headers = {'Content-type': 'application/json'}
    data = {"email": email,"password": password}
    response = requests.post(url, json = data, headers = headers, cookies = cookies)
    if response.status_code == 200:
        response = json.loads(response.text)
        response = response['redirectUrl']
        parsed = urlparse.urlparse(response)
        authCode = ''.join(parse_qs(parsed.query)['code'])
        #print(authCode)
	
    else:
        print('NOK login')
        return

    #token
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/user/oauth2/token'
    headers = {
        'Authorization': 'Basic ZmRjODVjMDAtMGEyZi00YzY0LWJjYjQtMmNmYjE1MDA3MzBhOnNlY3JldA==',
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': '150',
        'Host': 'prd.eu-ccapi.kia.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = 'grant_type=authorization_code&redirect_uri=https%3A%2F%2Fprd.eu-ccapi.kia.com%3A8080%2Fapi%2Fv1%2Fuser%2Foauth2%2Fredirect&code=' + authCode
    response = requests.post(url, data = data, headers = headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        access_token = response['token_type'] + ' ' + response['access_token']
        #print(access_token)
    else:
        print('NOK token')
        return

    #vehicles
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/spa/vehicles'
    headers = {
        'Authorization': access_token,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': '693a33fa-c117-43f2-ae3b-61a02d24f417',
        'offset': '1',
        'Host': 'prd.eu-ccapi.kia.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': get_stamp()}
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        vehicleId = response['resMsg']['vehicles'][0]['vehicleId']
        #print(vehicleId)
    else:
        print('NOK vehicles')
        return

    #vehicles/profile

    #prewakeup
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/spa/vehicles/' + vehicleId + '/control/engine'
    headers = {
        'Authorization': access_token,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': '693a33fa-c117-43f2-ae3b-61a02d24f417',
        'offset': '1',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '72',
        'Host': 'prd.eu-ccapi.kia.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': get_stamp()}
    data = {"action":"prewakeup","deviceId": deviceId}
    response = requests.post(url, json = data, headers = headers)
    if response.status_code == 200:
        #print(response.text)
        response = ''
    else:
        print('NOK prewakeup')
        return

    #pin
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v1/user/pin'
    headers = {
        'Authorization': access_token,
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': '64',
        'Host': 'prd.eu-ccapi.kia.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = {"deviceId": deviceId,"pin": pin}
    response = requests.put(url, json = data, headers = headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        controlToken = 'Bearer ' + response['controlToken']
        #print(controlToken)
    else:
        print('NOK pin')
        return

    #status
    url = 'https://prd.eu-ccapi.kia.com:8080/api/v2/spa/vehicles/' + vehicleId + '/status'
    headers = {
        'Authorization': controlToken,
        'ccsp-device-id': deviceId,
        'Content-Type': 'application/json',
        'Stamp': get_stamp()}
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
       statusresponse = json.loads(response.text)
       #log (statusresponse)
       soc = statusresponse['resMsg']['evStatus']['batteryStatus']
       print('soc: ',soc)
       charging = statusresponse['resMsg']['evStatus']['batteryCharge']
       print('charging: ', charging)
       
       #Retry if SoC returns 0 (also happens to the app sometimes)
       if soc == 0:
          print('Retry')
          response = requests.get(url, headers = headers)
          if response.status_code == 200:
             statusresponse = json.loads(response.text)
             #log (statusresponse)
             soc = statusresponse['resMsg']['evStatus']['batteryStatus']
             print('soc: ',soc)
             charging = statusresponse['resMsg']['evStatus']['batteryCharge']
             print('charging: ', charging)          

       if soc > 0:
          f = open(socfile, 'w')
          f.write(str(soc))
          f.close()
       
          soctime = time.time()
          f = open(soctimefile, 'w')
          f.write(str(int(soctime)))
          f.close()

    else:
         print('NOK status')
         return

if __name__ == '__main__':
    main()
