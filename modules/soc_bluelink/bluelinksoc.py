import sys
import requests
import uuid
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs

email = str(sys.argv[1])
password = str(sys.argv[2])
pin = str(sys.argv[3])
#vin = str(sys.argv[4])

def main():
    #diviceID
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v1/spa/notifications/register'
    headers = {
        'ccsp-service-id': '6d477c38-3ca4-4cf3-9557-2a1929a94654',
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': '80',
        'Host': 'prd.eu-ccapi.hyundai.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = {"pushRegId":"1","pushType":"GCM","uuid": str(uuid.uuid1())}
    response = requests.post(url, json = data, headers = headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        deviceId = response['resMsg']['deviceId']
        #print(deviceId)
    else:
        print('NOK diviceID')
        return

    #cookie für login
    session = requests.Session()
    response = session.get('https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/authorize?response_type=code&state=test&client_id=6d477c38-3ca4-4cf3-9557-2a1929a94654&redirect_uri=https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/redirect')
    if response.status_code == 200:
        cookies = session.cookies.get_dict()
        #print(cookies)
    else:
        print('NOK cookie für login')
        return

    #login
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/signin'
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
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token'
    headers = {
        'Authorization': 'Basic NmQ0NzdjMzgtM2NhNC00Y2YzLTk1NTctMmExOTI5YTk0NjU0OktVeTQ5WHhQekxwTHVvSzB4aEJDNzdXNlZYaG10UVI5aVFobUlGampvWTRJcHhzVg==',
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': '154',
        'Host': 'prd.eu-ccapi.hyundai.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = 'grant_type=authorization_code&redirect_uri=https%3A%2F%2Fprd.eu-ccapi.hyundai.com%3A8080%2Fapi%2Fv1%2Fuser%2Foauth2%2Fredirect&code=' + authCode
    response = requests.post(url, data = data, headers = headers)
    if response.status_code == 200:
        response = json.loads(response.text)
        access_token = response['token_type'] + ' ' + response['access_token']
        #print(access_token)
    else:
        print('NOK token')
        return

    #vehicles
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v1/spa/vehicles'
    headers = {
        'Authorization': access_token,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': '99cfff84-f4e2-4be8-a5ed-e5b755eb6581',
        'offset': '1',
        'Host': 'prd.eu-ccapi.hyundai.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
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
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v1/spa/vehicles/' + vehicleId + '/control/engine'
    headers = {
        'Authorization': access_token,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': '99cfff84-f4e2-4be8-a5ed-e5b755eb6581',
        'offset': '1',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '72',
        'Host': 'prd.eu-ccapi.hyundai.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = {"action":"prewakeup","deviceId": deviceId}
    response = requests.post(url, json = data, headers = headers)
    if response.status_code == 200:
        #print(response.text)
        response = ''
    else:
        print('NOK prewakeup')
        return

    #pin
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/pin'
    headers = {
        'Authorization': access_token,
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': '64',
        'Host': 'prd.eu-ccapi.hyundai.com:8080',
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
    url = 'https://prd.eu-ccapi.hyundai.com:8080/api/v2/spa/vehicles/' + vehicleId + '/status'
    headers = {
        'Authorization': controlToken,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': '99cfff84-f4e2-4be8-a5ed-e5b755eb6581',
        'offset': '1',
        'Host': 'prd.eu-ccapi.hyundai.com:8080',
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        #print(response.text)
        response = json.loads(response.text)
        soc = response['resMsg']['evStatus']['batteryStatus']
        #print(soc)
        f = open('/var/www/html/openWB/ramdisk/soc', 'w')
        f.write(str(soc))
        f.close()
    else:
        print('NOK status')
        return

if __name__ == '__main__':
    main()
