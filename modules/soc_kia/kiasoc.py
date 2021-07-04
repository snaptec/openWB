import sys
import time
import requests
import uuid
import json
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
import stamps_kia
import stamps_hyundai

#---------------Global Variables----------------------------------------
glParams = { 
    'host': '',
    'baseUrl': '',
    'clientId': '',
    'appId': '',
    'basicToken': '',
    'brand': '',
    'reqTimeout': 0,
    'statusTimeout': 0,
    'cacheValid': 0,
    'timerMinInterval': 0,
    'soc12vLimit': 0,
    'controlToken': '',
    'accessToken': {
        'tokenType': '',
        'accessToken': '',
        'refreshToken': '',
        'deviceId': ''
    },
    'files': {
        'logFile': '',
        'lockFile': '',
        'tokenFile': '',
        'currentSocFile': '',
        'lastSocFile': '',
        'lastRunFile': '',
        'lastTickFile': '',
        'timerFile': '',
        'meterFile': '',
        'lastMeterFile': '',
        'isChargingFile': '',
        'isPluggedFile': '',
        'chargedFile': '',
        'unplugFile': '',
#        'lastStampUpdateFile': '',
        'auxDataFile': ''
    },
    'args' : {
        'chargePoint': '',
        'debugLevel': 0
    }
}
     
#---------------Initialization------------------------------------------ 
def setGlobalData(vin):
    if vin[:2]=='KN' or vin[:3]=='U5Y' or vin[:3]=='U6Z':
        glParams['brand'] = 'kia'
        logDebug(2, "Vehicle identified as Kia")
    elif vin[:3]=='KMH' or vin[:3]=='TMA':
        glParams['brand'] = 'hyundai'
        logDebug(2, "Vehicle identified as Hyundai")
    else:
        glParams['brand'] = ''
        logDebug(2, "Vehicle WMI unknown")
        raise RuntimeError
    
    if glParams['brand'] == 'kia':
        glParams['host'] = 'prd.eu-ccapi.kia.com:8080'
        glParams['baseUrl'] = 'https://' + glParams['host']
        glParams['clientId'] = 'fdc85c00-0a2f-4c64-bcb4-2cfb1500730a'
        glParams['appId'] = 'e7bcd186-a5fd-410d-92cb-6876a42288bd'
        glParams['basicToken'] = 'Basic ZmRjODVjMDAtMGEyZi00YzY0LWJjYjQtMmNmYjE1MDA3MzBhOnNlY3JldA=='
    if glParams['brand'] == 'hyundai':
        glParams['host'] = 'prd.eu-ccapi.hyundai.com:8080'
        glParams['baseUrl'] = 'https://' + glParams['host']
        glParams['clientId'] = '6d477c38-3ca4-4cf3-9557-2a1929a94654'
        glParams['appId'] = '99cfff84-f4e2-4be8-a5ed-e5b755eb6581'
        glParams['basicToken'] = 'Basic NmQ0NzdjMzgtM2NhNC00Y2YzLTk1NTctMmExOTI5YTk0NjU0OktVeTQ5WHhQekxwTHVvSzB4aEJDNzdXNlZYaG10UVI5aVFobUlGampvWTRJcHhzVg=='
    
    return

def loadArguments(argsFile):
    glParams['reqTimeout'] = 60
    glParams['statusTimeout'] = 150
    glParams['cacheValid'] = 10 * 60
    glParams['soc12vLimit'] = 20
    glParams['timerMinInterval'] = 15 * 60
    
    retDict = {
        'accountName': '',
        'accountPassword': '',
        'accountPin': '',
        'vehicleVin': '',
        'timerInterval': '',
        'manualCalc': '',
        'batterySize': '',
        'efficiency': '',
        'ramDiskDir': '',
        'moduleDir': ''
    }
    
    try:
        f = open(argsFile, 'r')
        argsStr = f.read()
        argsDict = json.loads(argsStr)
        f.close()
        
        glParams['args']['chargePoint'] = str(argsDict['chargePoint'])
        glParams['args']['debugLevel'] = int(argsDict['debugLevel'])
        
        retDict['timerInterval'] = int(argsDict['timerInterval'])
        retDict['manualCalc'] = int(argsDict['manualCalc'])
        retDict['batterySize'] = float(argsDict['batterySize'])
        retDict['efficiency'] = float(argsDict['efficiency'])
        retDict['accountName'] = str(argsDict['accountName'])
        retDict['accountPassword'] = str(argsDict['accountPassword'])
        retDict['accountPin'] = str(argsDict['accountPin'])
        retDict['vehicleVin'] = str(argsDict['vehicleVin'])
        retDict['ramDiskDir'] = str(argsDict['ramDiskDir'])
        retDict['moduleDir'] = str(argsDict['moduleDir'])
    except:
        raise
        
    return retDict

def renderFileNames(ramDiskDir):
    try:
        glParams['files']['logFile'] = ramDiskDir + "/soc.log"
        glParams['files']['lockFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_lock"
        glParams['files']['tokenFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_token"
        glParams['files']['lastSocFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_lastsoc"
        glParams['files']['lastRunFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_lastrun"
        glParams['files']['lastTickFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_lasttick"
        glParams['files']['lastMeterFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_lastmeter"
        glParams['files']['chargedFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_charged"
        glParams['files']['unplugFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_unplug"
        glParams['files']['auxDataFile'] = ramDiskDir + "/soc_kia_lp" + glParams['args']['chargePoint'] + "_auxdata"
        
#        glParams['files']['lastStampUpdateFile'] = ramDiskDir + "/soc_kia_laststampupdate"
        
        if glParams['args']['chargePoint'] == '1':
            glParams['files']['currentSocFile'] = ramDiskDir + "/soc"
            glParams['files']['timerFile'] = ramDiskDir + "/soctimer"
            glParams['files']['meterFile'] = ramDiskDir + "/llkwh"
            glParams['files']['isPluggedFile'] = ramDiskDir + "/plugstat"
            glParams['files']['isChargingFile'] = ramDiskDir + "/chargestat"
        elif glParams['args']['chargePoint'] == '2':
            glParams['files']['currentSocFile'] = ramDiskDir + "/soc1"
            glParams['files']['timerFile'] = ramDiskDir + "/soctimer1"
            glParams['files']['meterFile'] = ramDiskDir + "/llkwhs1"
            glParams['files']['isPluggedFile'] = ramDiskDir + "/plugstats1"
            glParams['files']['isChargingFile'] = ramDiskDir + "/chargestats1"
        else:
            raise RuntimeError
    except:
        raise
        
    return

#---------------Access to stamps-----------------------------------------  
#def updateStamps(moduleDir):
#    try:
#        f = open(glParams['files']['lastStampUpdateFile'], 'r')
#        lastDownload = int(f.read())
#        f.close()
#    except:
#        lastDownload = 0
#        pass
#        
#    now = int(time.time())
#        
#    if lastDownload < (now - (3 * 24 * 60 * 60)):
#        logDebug(1, "Stamps expired - updating")
#        
#        url = 'https://gitcdn.link/repo/neoPix/bluelinky-stamps/master/hyundai.json'
#        r = requests.get(url, allow_redirects=True)
#        open( moduleDir + '/stamps_hyundai.py', 'w').write('stamps = ' + r.text)
#    
#        url = 'https://gitcdn.link/repo/neoPix/bluelinky-stamps/master/kia.json'
#        r = requests.get(url, allow_redirects=True)
#        open( moduleDir + '/stamps_kia.py', 'w').write('stamps = ' + r.text)
#        
#    try:
#        f = open(glParams['files']['lastStampUpdateFile'], 'w')
#        f.write(str(now))
#        f.close()
#    except:
#        raise
        
    return 

def getStamp():
    now = int(time.time())
    
    if glParams['brand'] == 'kia':
        index = max(min(int((now - stamps_kia.start) / stamps_kia.step) - 1,len(stamps_kia.stamps) - 1), 0)
        stamp = stamps_kia.stamps[index]
    if glParams['brand'] == 'hyundai':
        index = max(min(int((now - stamps_hyundai.start) / stamps_hyundai.step) - 1,len(stamps_hyundai.stamps) - 1), 0)
        stamp = stamps_hyundai.stamps[index]
    
    return stamp
    
#---------------Helper---------------------------------------------------  
def timeToStamp(timeString):
    timestamp = int(time.mktime(time.strptime(timeString, "%Y%m%d%H%M%S")))
    return timestamp
    
#---------------Debugging/Logging---------------------------------------  
def logDebug(msgLevel, msgText):
    if glParams['args']['debugLevel'] >= msgLevel:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        line = timestamp + ": LP" + glParams['args']['chargePoint'] + ": " + msgText + "\n"
        
        f = open(glParams['files']['logFile'], 'a')
        f.write(line)
        f.close()
    
    return 0

#---------------HTTP handling-------------------------------------------
def getHTTP(url = '', headers = '', cookies = '', timeout = 30):
    try:
        response = requests.get(url, headers = headers, cookies = cookies, timeout = timeout)        
    except requests.Timeout as err:
        logDebug(1, "Connection Timeout")
        raise
    except:
        logDebug(1, "HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        try:
            responseDict = json.loads(response.text)
            if response.status_code == 400 or response.status_code == 408 or response.status_code == 503:
                errorString = "[" + responseDict['resCode'] + "] " + responseDict['resMsg']
            else:
                errorString = "[" + responseDict['errCode'] + "] " + responseDict['errMsg']
        except:
            errorString = "[XXXX] Unidentified Error" + " " + response.text
        logDebug(1, 'Request failed, StatusCode: ' + str(response.status_code) + ', Error: ' + errorString)
        raise RuntimeError
        
    return

def putHTTP(url = '', data = '', headers = '', cookies = '', timeout = 30):
    try:
        if isinstance(data, dict):
            response = requests.put(url, json = data, headers = headers, cookies = cookies, timeout = timeout)
        else:
            response = requests.put(url, data = data, headers = headers, cookies = cookies, timeout = timeout)        
    except requests.Timeout as err:
        logDebug(1, "Connection Timeout")
        raise
    except:
        logDebug(1, "HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        try:
            responseDict = json.loads(response.text)
            if response.status_code == 408:
                errorString = "[" + responseDict['resCode'] + "] " + responseDict['resMsg']
            else:
                errorString = "[" + responseDict['errCode'] + "] " + responseDict['errMsg']
        except:
            errorString = "[XXXX] Unidentified Error"
        logDebug(1, 'Request failed, StatusCode: ' + str(response.status_code) + ', Error: ' + errorString)
        raise RuntimeError
        
    return
    
def postHTTP(url = '', data = '', headers = '', cookies = '', timeout = 30):
    try:
        if isinstance(data, dict):
            response = requests.post(url, json = data, headers = headers, cookies = cookies, timeout = timeout)
        else:
            response = requests.post(url, data = data, headers = headers, cookies = cookies, timeout = timeout)        
    except requests.Timeout as err:
        logDebug(1, "Connection Timeout")
        raise
    except:
        logDebug(1, "HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        try:
            responseDict = json.loads(response.text)
            if response.status_code == 408:
                errorString = "[" + responseDict['resCode'] + "] " + responseDict['resMsg']
            else:
                errorString = "[" + responseDict['errCode'] + "] " + responseDict['errMsg']
        except:
            errorString = "[XXXX] Unidentified Error"
        logDebug(1, 'Request failed, StatusCode: ' + str(response.status_code) + ', Error: ' + errorString)
        raise RuntimeError
        
    return

def getHTTPCookies(url):
    try:
        session = requests.Session()
        response = session.get(url)
    except requests.Timeout as err:
        logDebug(1, "Connection Timeout")
        raise    
    
    if response.status_code == 200:
        cookies = session.cookies.get_dict()
    else:
        logDebug(1, "Receiving cookies failed, StatusCode: " + str(response.status_code))
        raise
        
    return cookies

#---------------Request handling----------------------------------------
def getDeviceId():
    logDebug(2, "Requesting DeviceId")

    url = glParams['baseUrl'] + '/api/v1/spa/notifications/register'
    data = {"pushRegId":"1","pushType":"GCM","uuid": str(uuid.uuid1())}
    headers = {
        'ccsp-service-id': glParams['clientId'],
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': str(len(data)),
        'Host': glParams['host'],
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': getStamp()}

    try:
        response = postHTTP(url = url, data = data, headers = headers, timeout = glParams['reqTimeout'])
    except:
        raise
        
    try:
        responseDict = json.loads(response)
        deviceId = responseDict['resMsg']['deviceId']
    except:
        logDebug(1, "Could not receive DeviceId, invalid response")
        logDebug(2, response)
        raise
        
    logDebug(2, "DeviceId = " + deviceId)
        
    return deviceId

def getCookies():
    logDebug(2, "Get cookies for login")

    url = glParams['baseUrl'] + '/api/v1/user/oauth2/authorize?response_type=code&state=test&client_id=' + glParams['clientId'] + '&redirect_uri=' + glParams['baseUrl'] + '/api/v1/user/oauth2/redirect'
    
    try:
        cookies = getHTTPCookies(url)
    except:
        raise

    return cookies

def setLanguage(cookies):
    logDebug(2, "Setting language")
    
    url = glParams['baseUrl'] + '/api/v1/user/language' 
    headers = {'Content-type': 'application/json'}
    data = {"lang": "en"}
    
    try:
        response = postHTTP(url = url, data = data, headers = headers, cookies = cookies, timeout = glParams['reqTimeout'])
    except:
        raise
        
    return

def getAuthCode(email, password, cookies):
    logDebug(2, "Sending username/password")

    url = glParams['baseUrl'] + '/api/v1/user/signin' 
    headers = {'Content-type': 'application/json'}
    data = {"email": email,"password": password}
    
    try:
        response = postHTTP(url = url, data = data, headers = headers, cookies = cookies, timeout = glParams['reqTimeout'])
    except:
        raise 
    
    try:
        responseDict = json.loads(response)
        responseUrl = responseDict['redirectUrl']
        parsed = urlparse.urlparse(responseUrl)
        authCode = ''.join(parse_qs(parsed.query)['code'])
    except:
        logDebug(0, "Login failed, invalid response")
        logDebug(2, response)     
        raise
        
    logDebug(2, "AuthCode = " + authCode)
        
    return authCode

def getAccessToken(authCode):
    logDebug(2, "Requesting access token")
    
    url = glParams['baseUrl'] + '/api/v1/user/oauth2/token'
    data = 'grant_type=authorization_code&redirect_uri=' + glParams['baseUrl'] + '%2Fapi%2Fv1%2Fuser%2Foauth2%2Fredirect&code=' + authCode
    headers = {
        'Authorization': glParams['basicToken'],
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(data)),
        'Host': glParams['host'],
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}

    try:
        response = postHTTP(url = url, headers = headers, data = data, timeout = glParams['reqTimeout'])
    except:
        raise
        
    try:
        accessToken = json.loads(response)
    except:
        logDebug(0, "Token request failed, invalid response")
        logDebug(2, response)
        raise
        
    logDebug(2, "Access token = " + accessToken['access_token'])      

    return accessToken
    
def refreshAccessToken(refreshToken):
    logDebug(2, "Refreshing access token")
    
    url = glParams['baseUrl'] + '/api/v1/user/oauth2/token'
    data = 'grant_type=refresh_token&redirect_uri=https://www.getpostman.com/oauth2/callback&refresh_token=' + refreshToken
    headers = {
        'Authorization': glParams['basicToken'],
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(data)),
        'Host': glParams['host'],
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}

    try:
        response = postHTTP(url = url, headers = headers, data = data, timeout = glParams['reqTimeout'])
    except:
        raise
        
    try:
        accessToken = json.loads(response)
        accessToken['refresh_token'] = refreshToken
    except:
        logDebug(0, "Token request failed, invalid response")
        logDebug(2, response)
        raise
        
    logDebug(2, "Access token = " + accessToken['access_token'])      

    return accessToken
    
def getControlToken(pin):
    logDebug(2, "Sending PIN")
    
    url = glParams['baseUrl'] + '/api/v1/user/pin'
    data = {"deviceId": glParams['accessToken']['deviceId'],"pin": pin}
    headers = {
        'Authorization': glParams['accessToken']['tokenType'] + ' ' + glParams['accessToken']['accessToken'],
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': str(len(data)),
        'Host': glParams['host'],
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0'}

    try:
        response = putHTTP(url = url, data = data, headers = headers, timeout = glParams['reqTimeout'])
    except:
        raise
        
    try:
        responseDict = json.loads(response)
        controlToken = 'Bearer ' + responseDict['controlToken']
    except:
        logDebug(1, "Sending PIN failed, invalid response")
        logDebug(2, response)
        raise    
        
    logDebug(2, "Control token = " + controlToken)
   
    return controlToken

def getVehicleId(vin):
    logDebug(2, "Requesting vehicle list")
    
    url = glParams['baseUrl'] + '/api/v1/spa/vehicles'
    headers = {
        'Authorization': glParams['accessToken']['tokenType'] + ' ' + glParams['accessToken']['accessToken'],
        'ccsp-device-id': glParams['accessToken']['deviceId'],
        'ccsp-application-id': glParams['appId'],
        'offset': '1',
        'Host': glParams['host'],
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': getStamp()}

    try:
        response = getHTTP(url = url, headers = headers, timeout = glParams['reqTimeout'])
    except:
        raise    

    vehicleId = ''
    try:
        responseDict = json.loads(response)
        for vehicle in responseDict['resMsg']['vehicles']:
            if vehicle['vin'] == vin:
                vehicleId = vehicle['vehicleId']
    except:
        logDebug(1, "Vehicle request failed, invalid response")
        logDebug(2, response)
        raise     
            
    if vehicleId == '':
        logDebug(1, "VIN " + vin + " unknown")
        raise
        
    logDebug(2, "VehicleId = " + vehicleId)
        
    return vehicleId

def getStatusCached(vehicleId):
    logDebug(2, "Receiving cached status")
    
    statusDict = {
        'time': 0,
        'socev': 0,
        'soc12v': 0,
        'vehicleLocation': '',
        'vehicleStatus': '',
        'odometer': ''
    }
    
    url = glParams['baseUrl'] + '/api/v2/spa/vehicles/' + vehicleId + '/status/latest'
    headers = {
        'Authorization': glParams['controlToken'],
        'ccsp-device-id': glParams['accessToken']['deviceId'],
        'Content-Type': 'application/json',
        'Stamp': getStamp()}
    
    try:
        response = getHTTP(url = url, headers = headers, timeout = glParams['reqTimeout'])
    except:
        raise 

    try:
        responseDict = json.loads(response)
        statusDict['time'] = timeToStamp(responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']['time'])
        statusDict['socev'] = int(responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']['evStatus']['batteryStatus'])
        statusDict['soc12v'] = int(responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']['battery']['batSoc'])
        statusDict['vehicleLocation'] = responseDict['resMsg']['vehicleStatusInfo']['vehicleLocation']
        statusDict['vehicleStatus'] = responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']
        statusDict['odometer'] = responseDict['resMsg']['vehicleStatusInfo']['odometer']
    except:
        logDebug(1, "Receiving cached status failed, invalid response")
        logDebug(2, response)
        raise

    return statusDict

def doPrewakeup(vehicleId):
    logDebug(2, "Triggering Pre-Wakeup")
        
    url = glParams['baseUrl'] + '/api/v1/spa/vehicles/' + vehicleId + '/control/engine'
    data = {"action":"prewakeup","deviceId": glParams['accessToken']['deviceId']}
    headers = {
        'Authorization': glParams['accessToken']['tokenType'] + ' ' + glParams['accessToken']['accessToken'],
        'ccsp-device-id': glParams['accessToken']['deviceId'],
        'ccsp-application-id': glParams['appId'],
        'offset': '1',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': str(len(data)),
        'Host': glParams['host'],
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': getStamp()}

    try:
        response = postHTTP(url = url, data = data, headers = headers, timeout = glParams['statusTimeout'])
    except:
        raise
        
    return

def getStatusFull(vehicleId):  
    logDebug(2, "Receiving current status from vehicle")

    statusDict = {
        'time': 0,
        'socev': 0,
        'soc12v': 0,
        'vehicleStatus': ''
    }
    
    url = glParams['baseUrl'] + '/api/v2/spa/vehicles/' + vehicleId + '/status'
    headers = {
        'Authorization': glParams['controlToken'],
        'ccsp-device-id': glParams['accessToken']['deviceId'],
        'Content-Type': 'application/json',
        'Stamp': getStamp()}

    try:
        response = getHTTP(url = url, headers = headers, timeout = glParams['statusTimeout'])
    except:
        raise
        

    try:
        responseDict = json.loads(response)
        statusDict['time'] = timeToStamp(responseDict['resMsg']['time'])
        statusDict['socev'] = int(responseDict['resMsg']['evStatus']['batteryStatus'])
        statusDict['soc12v'] = int(responseDict['resMsg']['battery']['batSoc'])
        statusDict['vehicleStatus'] = responseDict['resMsg']
    except:
        logDebug(1, "Receiving current status failed, invalid response")
        logDebug(2, response)
        raise

    return statusDict        

#---------------Token Handling------------------------------------------
def loadAccessToken():
    try:
        f = open(glParams['files']['tokenFile'], 'r')
        tokenDict = json.loads(f.read())
        f.close()
        
        glParams['accessToken']['accessToken'] = tokenDict['accessToken']
        glParams['accessToken']['tokenType'] = tokenDict['tokenType']
        glParams['accessToken']['refreshToken'] = tokenDict['refreshToken']
        glParams['accessToken']['deviceId'] = tokenDict['deviceId']
    except:
        raise
        
    return
    
def saveAccessToken(accessToken, deviceId):
    glParams['accessToken']['accessToken'] = accessToken['access_token']
    glParams['accessToken']['tokenType'] = accessToken['token_type']
    glParams['accessToken']['refreshToken'] = accessToken['refresh_token']
    glParams['accessToken']['deviceId'] = deviceId
    
    f = open(glParams['files']['tokenFile'], 'w')
    f.write(json.dumps(glParams['accessToken']))
    f.close()
    
    return
    
def requestNewAuthToken(email, password):
    try:
        deviceId = getDeviceId()
        cookies = getCookies()
        setLanguage(cookies)
        authCode = getAuthCode(email, password, cookies)
        accessToken = getAccessToken(authCode)
        saveAccessToken(accessToken, deviceId)
    except:
        raise
        
    return

def refreshAuthToken():
    try:
        accessToken = refreshAccessToken(glParams['accessToken']['refreshToken'])
        saveAccessToken(accessToken, glParams['accessToken']['deviceId'])
    except:
        raise
        
    return
    
def updateAuthToken(email, password):
    try:
        loadAccessToken()
        refreshAuthToken()
    except:
        try:
            requestNewAuthToken(email, password)
        except:
            raise
    
    return
    
def requestNewControlToken(pin):
    try:
        controlToken = getControlToken(pin)
        glParams['controlToken'] = controlToken
    except:
        raise
        
    return
    
#---------------Download Logic------------------------------------------ 
def DownloadSoC(email, password, pin, vin):
    logDebug(0, "SoC download starting")
      
    auxData = {
        'vehicleLocation': '',
        'vehicleStatus': '',
        'odometer': ''
    }
    
    try:
        now = int(time.time())       
        setGlobalData(vin)
    except:
        logDebug(0, "Initialisation failed")
        raise
    
    try:       
        updateAuthToken(email, password)
        requestNewControlToken(pin)
    except:
        logDebug(0, "Login failed")
        raise
        
    try:
        vehicleId = getVehicleId(vin)
        status = getStatusCached(vehicleId)
    except:
        logDebug(0, "Collecting data from server failed")
        raise

    try:
        auxData['vehicleLocation'] = status['vehicleLocation']
        auxData['vehicleStatus'] = status['vehicleStatus']
        auxData['odometer'] = status['odometer']
    except:
        pass

    if (now - status['time']) < (glParams['cacheValid']) and status['socev'] > 0:
        logDebug(2, "Cached data is current")
    else:
        if status['soc12v'] < glParams['soc12vLimit']:
            logDebug(0, "12 V-battery low - 12 V-SoC: " + cachedStatus['soc12v'] + " %; Download cancelled")
            raise RuntimeError
            
        try:
            doPrewakeup(vehicleId)
            status = getStatusFull(vehicleId)
        except:
            logDebug(0, "Collecting data from vehicle failed")
            raise
        
        try:
            auxData['vehicleStatus'] = status['vehicleStatus']
        except:
            pass
    
    if status['soc12v'] >= 80:
        logDebug(2, "Received SoC (12 V-battery): " + str(status['soc12v']) + "%")
    elif status['soc12v'] >= 70 and status['soc12v'] < 80:
        logDebug(1, "Received SoC (12 V-battery): " + str(status['soc12v']) + "%")
    elif status['soc12v'] < 70:
        logDebug(0, "Received SoC (12 V-battery): " + str(status['soc12v']) + "%")
        
    soc = status['socev']
    logDebug(0, "Received SoC (HV-battery): " + str(soc) + "%")
    
    try:
        f = open(glParams['files']['auxDataFile'], 'w')
        f.write(json.dumps(auxData))
        f.close()
    except:
        pass
        
    logDebug(1, "SoC download ending")
    
    return soc

def doExternalUpdate(email, password, pin, vin):
    attempt = 0
   
    while attempt < 3:
        try:
            soc = DownloadSoC(email, password, pin, vin)
        except:
            soc = 0
            
        if soc > 0:
            saveSoc(soc, 0)
            break
        else:
            attempt += 1
            if attempt < 3:
                logDebug(2, "Retrying in 60 Seconds...")
                time.sleep(60)
    
    return
    
def doManualUpdate(batterySize, efficiency):  
    try:
        f = open(glParams['files']['meterFile'], 'r')
        currentMeter = float(f.read())
        f.close()
    except:
        logDebug(2, "Could not find current meter file")
        raise
                
    try:
        f = open(glParams['files']['lastMeterFile'], 'r')
        lastMeter = float(f.read())
        f.close()
    except:
        logDebug(2, "Could not find last meter file")
        raise
        
    try:
        f = open(glParams['files']['lastSocFile'], 'r')
        lastSoc = float(f.read())
        f.close()
    except:
        logDebug(2, "Could not find last SoC file")
        raise

    meterDiff = currentMeter - lastMeter
    meterDiffEff = meterDiff * (efficiency / 100)
    socDiff = 100 * (meterDiffEff / batterySize)
    newSoc = int(max(min(lastSoc + socDiff, 100), 1))
    
    logDebug(2, "Charged since last update: " + '{:.3f}'.format(meterDiff) + " kWh = " + '{:.3f}'.format(meterDiffEff) + " kWh @ " + '{:.0f}'.format(efficiency) + "% efficency")
    logDebug(2, "Charged since last update: " + '{:.3f}'.format(meterDiffEff) + " kWh of " + '{:.0f}'.format(batterySize) + " kWh = " + '{:.2f}'.format(socDiff) + "% SoC")
    logDebug(1, "Estimated SoC: " + '{:.0f}'.format(lastSoc) + "% (last update) + " + '{:.2f}'.format(socDiff) + "% (extrapolation) = " + '{:.0f}'.format(newSoc) + "% SoC")
    
    saveSoc(newSoc, 1)
    
    return
    
#---------------Lockfile handling---------------------------------------
def checkLockFile():
    
    try:
        f = open(glParams['files']['lockFile'], 'r')
        lockTime = int(f.read())
        f.close()
    except:
        lockTime = 0
        
    now = time.time()
    if lockTime > (now - 10*60):
        raise RuntimeError
        
    return

def createLockFile():
    try:
        f = open(glParams['files']['lockFile'], 'w')
        f.write(str(int(time.time())))
        f.close()
    except:
        raise
        
    return

def purgeLockFile():
    try:
        f = open(glParams['files']['lockFile'], 'w')
        f.write(str(0))
        f.close()
    except:
        raise
        
    return
    
#---------------SoCfile handling----------------------------------------
def saveSoc(soc, manual):
    f = open(glParams['files']['currentSocFile'], 'w')
    f.write(str(int(soc)))
    f.close()
        
    if manual == 0:
        f = open(glParams['files']['lastSocFile'], 'w')
        f.write(str(soc))
        f.close()
               
        try:
            f = open(glParams['files']['meterFile'], 'r')
            meter = float(f.read())
            f.close()
        except:
            meter = 0
        
        f = open(glParams['files']['lastMeterFile'], 'w')
        f.write(str(meter))
        f.close()
        
        resetUnplugState()
        resetChargedState()
        
    return

#---------------Timer handling------------------------------------------
def ackExternalTrigger():
    try:
        f = open(glParams['files']['timerFile'], 'w')
        f.write(str(0))
        f.close()
    except:
        raise
        
    return
    
def ackTimerTrigger():
    try:
        now = int(time.time())
        
        f = open(glParams['files']['lastRunFile'], 'w')
        f.write(str(now))
        f.close()
    except:
        raise
        
    return

def isCharging():
    chargeState = 0
    
    try:  
        f = open(glParams['files']['isChargingFile'], 'r')
        chargeState = int(f.read())
        f.close()    
    except:
        raise

    return chargeState
       
def isPlugged():
    plugState = 0
    
    try:  
        f = open(glParams['files']['isPluggedFile'], 'r')
        plugState = int(f.read())
        f.close()    
    except:
        raise

    return plugState
    
def saveTickTime():
    try:
        now = int(time.time())
        
        f = open(glParams['files']['lastTickFile'], 'w')
        f.write(str(now))
        f.close()
    except:
        raise
        
    return
    
def saveUnplugState():
    unplugState = 0
    
    try:  
        f = open(glParams['files']['isPluggedFile'], 'r')
        plugState = int(f.read())
        f.close()
        
        if plugState == 0:
            unplugState = 1
    except:
        raise
        
    try:  
        now = int(time.time())
        
        f = open(glParams['files']['lastTickFile'], 'r')
        lastTick = int(f.read())
        f.close() 
        
        secsSinceLastTick = now - lastTick
        if secsSinceLastTick > 60:
            unplugState = 1
    except:
        raise
    
    if unplugState == 1:
        f = open(glParams['files']['unplugFile'], 'w')
        f.write(str(unplugState))
        f.close()        
        
    return
    
def saveChargedState():
    chargedState = 0
    
    try:  
        f = open(glParams['files']['isChargingFile'], 'r')
        chargedState = int(f.read())
        f.close()      
    except:
        raise
        
    
    if chargedState == 1:
        f = open(glParams['files']['chargedFile'], 'w')
        f.write(str(chargedState))
        f.close()        
        
    return

def resetUnplugState():
    f = open(glParams['files']['unplugFile'], 'w')
    f.write(str(0))
    f.close()  

    return
    
def resetChargedState():
    f = open(glParams['files']['chargedFile'], 'w')
    f.write(str(0))
    f.close()  

    return

def wasUnplugged():
    unplugState = 1
    
    try:  
        f = open(glParams['files']['unplugFile'], 'r')
        unplugState = int(f.read())
        f.close()    
    except:
        unplugState = 1
    
    return unplugState

def wasCharging():
    chargedState = 1
    
    try:  
        f = open(glParams['files']['chargedFile'], 'r')
        chargedState = int(f.read())
        f.close()    
    except:
        chargedState = 1
    
    return chargedState
    
def isExternalTriggered():
    trigger = 0
    
    try:  
        f = open(glParams['files']['timerFile'], 'r')
        ticksLeft = int(f.read())
        f.close()    
    except:
        ticksLeft = 0

    if ticksLeft > 0:
        trigger = 1
        logDebug(1, "SoC download triggered externally")
        
    return trigger
    
def isMinimumTimerExpired(timerMinInterval):
    trigger = 0
    now = int(time.time())

    try:
        f = open(glParams['files']['lastRunFile'], 'r')
        lastRun = int(f.read())
        f.close()
    except:
        lastRun = 0
        
    secSince = now - lastRun

    if secSince < timerMinInterval:
        trigger = 0
    else:
        trigger = 1
        
    return trigger

def isTimerExpired(timerInterval):
    trigger = 0
    now = int(time.time())
    
    try:
        f = open(glParams['files']['lastRunFile'], 'r')
        lastRun = int(f.read())
        f.close()
    except:
        lastRun = 0
        
    secLeft = (lastRun + (timerInterval * 60)) - now
    if secLeft < 0:
        trigger = 1
        logDebug(1, "SoC download triggered by timer")
    else:
        logDebug(2, "Next Update: " + '{:.1f}'.format(secLeft / 60) + " minutes")
        
    return trigger
    
def isDownloadTriggered(timerInterval, timerMinInterval):
    trigger = 0

    try:
        if isExternalTriggered() == 1:
            ackExternalTrigger()
            trigger = 1
        elif isTimerExpired(timerInterval) == 1:
            trigger = 1
        else:
            trigger = 0

        if trigger == 1:
            if isMinimumTimerExpired(timerMinInterval) == 1:
                ackTimerTrigger()
                trigger = 1
            else: 
                logDebug(1, "Last Download less then "+ '{:.0f}'.format(timerMinInterval / 60) + " minutes ago. Cancelling download")
                trigger = 0
        
        if trigger == 1:
            if wasCharging() == 1 or wasUnplugged() == 1:
                trigger = 1
            else:
                logDebug(1, "Vehicle was not unplugged or charging since last download. Cancelling download")
                trigger = 0
                
    except:
        raise
        
    return trigger
        
#---------------Main Function-------------------------------------------
def main():
    try:
        args = loadArguments(str(sys.argv[1]))
        renderFileNames(args['ramDiskDir'])
    except:
        exit(1)
        
    try:
        checkLockFile()
        createLockFile()
    except:
        exit(1)
    
    logDebug(1, "-------------------------------")    
    logDebug(1, "Kia/Hyundai SoC Module starting")

    #try:
    #    updateStamps(args['moduleDir'])
    #except:
    #    pass
                
    try:
        saveUnplugState()
        saveChargedState()
        
        if isDownloadTriggered(args['timerInterval'], glParams['timerMinInterval']) == 1:
            doExternalUpdate(args['accountName'], args['accountPassword'], args['accountPin'], args['vehicleVin'])
        elif args['manualCalc'] == 1:
            if isCharging() == 1:
                logDebug(2, "Manual calculation starting")
                doManualUpdate(args['batterySize'], args['efficiency'])
        else: 
            logDebug(2, "Nothing to do yet")
    except:
        pass
    
    try:
        saveTickTime()
    except:
        pass
        
    logDebug(1, "Kia/Hyundai SoC Module ending")
    
    try:
        purgeLockFile()
    except:
        exit(1)
    
    exit(0)
        
if __name__ == '__main__':
    main()
