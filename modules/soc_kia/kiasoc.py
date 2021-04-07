import sys
import time
import requests
import uuid
import json
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
import stamps

email = str(sys.argv[1])
password = str(sys.argv[2])
pin = str(sys.argv[3])
vin = str(sys.argv[4])
socfile = str(sys.argv[5])
chargepoint = str(sys.argv[6])
debuglevel = int(sys.argv[7])
successfile = str(sys.argv[8])

host = 'prd.eu-ccapi.kia.com:8080'
baseUrl = 'https://' + host
clientId = 'fdc85c00-0a2f-4c64-bcb4-2cfb1500730a'
appId = '693a33fa-c117-43f2-ae3b-61a02d24f417'
basicToken = 'Basic ZmRjODVjMDAtMGEyZi00YzY0LWJjYjQtMmNmYjE1MDA3MzBhOnNlY3JldA=='

reqTimeout = 10
statusTimeout = 60

# Kia API expects a stamp. The solution to handle this problem was implemented for bluelinky and is used here as well.
# For more information: https://github.com/Hacksore/bluelinky/pull/105
# A random stamp from the list in the file stamps.py is used here.
# Instruction for generating new stamps can be found in stamps.py
#
def get_stamp(): 
    return stamps.stamps[random.randint(0,len(stamps.stamps)-1)]

def socDebugLog(msgLevel, msgText):
    if debuglevel >= msgLevel:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        line = timestamp + ": LP" + chargepoint + ": " + msgText
        print(line)
    return

def DownloadSoC():
    
    #Get deviceId   
    socDebugLog(2, "            Requesting DeviceId")
    
    url = baseUrl + '/api/v1/spa/notifications/register'
    headers = {
        'ccsp-service-id': clientId,
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': '80',
        'Host': host,
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': get_stamp()}
    data = {"pushRegId":"1","pushType":"GCM","uuid": str(uuid.uuid1())}
    
    try:
        response = requests.post(url, json = data, headers = headers, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1
    
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        try:
            deviceId = responseDict['resMsg']['deviceId']
        except KeyError:
            socDebugLog(1, "            Could not receive DeviceId, invalid response")
            socDebugLog(2, "            " + response.text)
            return -1
        socDebugLog(2, "            DeviceId = " + deviceId)
    else:
        socDebugLog(1, "            Could not receive DeviceId, StatusCode: " + str(response.status_code))
        return -1

    #cookie for login
    socDebugLog(2, "            Get cookies for login")
    try:
        session = requests.Session()
        response = session.get(baseUrl + '/api/v1/user/oauth2/authorize?response_type=code&state=test&client_id=' + clientId + '&redirect_uri=' + baseUrl + '/api/v1/user/oauth2/redirect')
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1    
    
    if response.status_code == 200:
        cookies = session.cookies.get_dict()
    else:
        socDebugLog(1, "            Receiving cookies failed")
        return -1

    #Language
    socDebugLog(2, "            Setting language")
    url = baseUrl + '/api/v1/user/language' 
    headers = {'Content-type': 'application/json'}
    data = {"lang": "en"}
    
    try:
        response = requests.post(url, json = data, headers = headers, cookies = cookies, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1  
        
    #login
    socDebugLog(2, "            Sending username/password")
    url = baseUrl + '/api/v1/user/signin' 
    headers = {'Content-type': 'application/json'}
    data = {"email": email,"password": password}
    
    try:
        response = requests.post(url, json = data, headers = headers, cookies = cookies, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1  
    
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        try:
            responseUrl = responseDict['redirectUrl']
        except KeyError:
            socDebugLog(1, "            Login failed, invalid response")
            socDebugLog(2, "            " + response.text)     
            return -1
        parsed = urlparse.urlparse(responseUrl)
        authCode = ''.join(parse_qs(parsed.query)['code'])
        socDebugLog(2, "            AuthCode = " + authCode)
    else:
        socDebugLog(1, "            Login failed, StatusCode: " + str(response.status_code))
        return -1

    #token
    socDebugLog(2, "            Requesting Token")
    
    url = baseUrl + '/api/v1/user/oauth2/token'
    headers = {
        'Authorization': basicToken,
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': '150',
        'Host': host,
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = 'grant_type=authorization_code&redirect_uri=' + baseUrl + '%2Fapi%2Fv1%2Fuser%2Foauth2%2Fredirect&code=' + authCode
    
    try:
        response = requests.post(url, data = data, headers = headers, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1 
        
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        try:
            access_token = responseDict['token_type'] + ' ' + responseDict['access_token']
        except KeyError:
            socDebugLog(1, "            Token request failed, invalid response")
            socDebugLog(2, "            " + response.text)
            return -1            
        socDebugLog(2, "            Token = " + access_token)    
    else:
        socDebugLog(1, "            Token request failed, StatusCode: " + str(response.status_code))
        return -1

    #vehicles
    socDebugLog(2, "            Requesting vehicle list")
    
    url = baseUrl + '/api/v1/spa/vehicles'
    headers = {
        'Authorization': access_token,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': appId,
        'offset': '1',
        'Host': host,
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': get_stamp()}
    
    try:
        response = requests.get(url, headers = headers, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1 
        
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        try:
            vehicleId = ''
            for vehicle in responseDict['resMsg']['vehicles']:
                if vehicle['vin'] == vin:
                    vehicleId = vehicle['vehicleId']
            if vehicleId == '':
                socDebugLog(1, "            VIN " + vin + " unknown")
                return -1;
        except KeyError:
            socDebugLog(1, "            Vehicle request failed, invalid response")
            socDebugLog(2, "            " + response.text)
            return -1     
        socDebugLog(2, "            VehicleId = " + vehicleId)
    else:
        socDebugLog(1, "            Vehicle request failed, StatusCode: " + str(response.status_code))
        return -1

    #prewakeup
    socDebugLog(2, "            Triggering Pre-Wakeup")
        
    url = baseUrl + '/api/v1/spa/vehicles/' + vehicleId + '/control/engine'
    headers = {
        'Authorization': access_token,
        'ccsp-device-id': deviceId,
        'ccsp-application-id': appId,
        'offset': '1',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '72',
        'Host': host,
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': get_stamp()}
    data = {"action":"prewakeup","deviceId": deviceId}
    
    try:    
        response = requests.post(url, json = data, headers = headers, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1 
        
    if response.status_code == 200:
        response = ''
    else:
        socDebugLog(1, "            Pre-Wakeup request failed, StatusCode: " + str(response.status_code))
        return -1

    #pin
    socDebugLog(2, "            Sending PIN")
    
    url = baseUrl + '/api/v1/user/pin'
    headers = {
        'Authorization': access_token,
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': '64',
        'Host': host,
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}
    data = {"deviceId": deviceId,"pin": pin}
    
    try:
        response = requests.put(url, json = data, headers = headers, timeout = reqTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1
        
    if response.status_code == 200:
        responseDict = json.loads(response.text)
        try:
            controlToken = 'Bearer ' + responseDict['controlToken']
        except KeyError:
            socDebugLog(1, "            Sending PIN failed, invalid response")
            socDebugLog(2, "            " + response.text)
            return -1     
        
        socDebugLog(2, "            controlToken = " + controlToken)
    else:
        socDebugLog(1, "            Sending PIN failed, StatusCode: " + str(response.status_code))
        return -1

    #status
    socDebugLog(2, "            Receiving status")
    
    url = baseUrl + '/api/v2/spa/vehicles/' + vehicleId + '/status'
    headers = {
        'Authorization': controlToken,
        'ccsp-device-id': deviceId,
        'Content-Type': 'application/json',
        'Stamp': get_stamp()}
    
    try:
        response = requests.get(url, headers = headers, timeout = statusTimeout)
    except requests.Timeout as err:
        socDebugLog(1, "            Connection Timeout")
        return -1
        
    if response.status_code == 200:
        statusresponse = json.loads(response.text)

        try:
            soc = statusresponse['resMsg']['evStatus']['batteryStatus']
            #charging = statusresponse['resMsg']['evStatus']['batteryCharge']
        except KeyError:
            socDebugLog(1, "            Receiving status failed, invalid response")
            socDebugLog(2, "            " + response.text)
            return -1        
       
        socDebugLog(2, "            SoC = " + str(soc))

        if soc > 0:
            #Save SoC
            f = open(socfile, 'w')
            f.write(str(soc))
            f.close()
                    
            #Save Status Successful
            f = open(successfile, 'w')
            f.write(str("1"))
            f.close()
          
        return soc

    else:
         socDebugLog(1, "            Receiving status failed, StatusCode: " + str(response.status_code))
         return -1


def main():
    socDebugLog(1, "        SoC download starting")
    soc = DownloadSoC()
    if soc == 0:
        socDebugLog(2, "        Retrying in 30 Seconds")
        time.sleep(30)
        soc = DownloadSoC()
    socDebugLog(1, "        SoC download ending")    

if __name__ == '__main__':
    main()
