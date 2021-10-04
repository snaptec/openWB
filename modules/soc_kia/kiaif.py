import time
import json

import parameters
import soclogging
import kiahttp
import stamps

def timeToStamp(timeString):
    timestamp = int(time.mktime(time.strptime(timeString, "%Y%m%d%H%M%S")))
    return timestamp

def getVehicleId(vin):
    soclogging.logDebug(2, "Requesting vehicle list")
    
    url = parameters.getParameter('baseUrl') + '/api/v1/spa/vehicles'
    headers = {
        'Authorization': parameters.getParameter('tokenType') + ' ' + parameters.getParameter('accessToken'),
        'ccsp-device-id': parameters.getParameter('deviceId'),
        'ccsp-application-id': parameters.getParameter('appId'),
        'offset': '1',
        'Host': parameters.getParameter('host'),
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': stamps.getStamp()}

    try:
        response = kiahttp.getHTTP(url = url, headers = headers, timeout = parameters.getParameter('reqTimeout'))
    except:
        raise    

    vehicleId = ''
    try:
        responseDict = json.loads(response)
        for vehicle in responseDict['resMsg']['vehicles']:
            if vehicle['vin'] == vin:
                vehicleId = vehicle['vehicleId']
    except:
        soclogging.logDebug(1, "Vehicle request failed, invalid response")
        soclogging.logDebug(2, response)
        raise     
            
    if vehicleId == '':
        soclogging.logDebug(1, "VIN " + vin + " unknown")
        raise
        
    soclogging.logDebug(2, "VehicleId = " + vehicleId)
        
    return vehicleId

def getStatusCached(vehicleId):
    soclogging.logDebug(2, "Receiving cached status")
    
    statusDict = {
    }
    
    url = parameters.getParameter('baseUrl') + '/api/v2/spa/vehicles/' + vehicleId + '/status/latest'
    headers = {
        'Authorization': parameters.getParameter('controlToken'),
        'ccsp-device-id': parameters.getParameter('deviceId'),
        'Content-Type': 'application/json',
        'Stamp': stamps.getStamp()}
    
    try:
        response = kiahttp.getHTTP(url = url, headers = headers, timeout = parameters.getParameter('reqTimeout'))
    except:
        raise 

    try:
        responseDict = json.loads(response)
    except:
        soclogging.logDebug(1, "Receiving cached status failed, invalid response")
        soclogging.logDebug(2, response)
        raise
        
    try:
        statusDict['soc12v'] = int(responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']['battery']['batSoc'])
    except:
        statusDict['soc12v'] = 100
        pass
        
    try:
        statusDict['time'] = timeToStamp(responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']['time'])
        statusDict['socev'] = int(responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']['evStatus']['batteryStatus'])
        statusDict['vehicleLocation'] = responseDict['resMsg']['vehicleStatusInfo']['vehicleLocation']
        statusDict['vehicleStatus'] = responseDict['resMsg']['vehicleStatusInfo']['vehicleStatus']
        statusDict['odometer'] = responseDict['resMsg']['vehicleStatusInfo']['odometer']
    except:
        soclogging.logDebug(1, "Receiving cached status failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    return statusDict

def doPrewakeup(vehicleId):
    soclogging.logDebug(2, "Triggering Pre-Wakeup")
        
    url = parameters.getParameter('baseUrl') + '/api/v1/spa/vehicles/' + vehicleId + '/control/engine'
    data = {"action":"prewakeup","deviceId": parameters.getParameter('deviceId')}
    headers = {
        'Authorization': parameters.getParameter('tokenType') + ' ' + parameters.getParameter('accessToken'),
        'ccsp-device-id': parameters.getParameter('deviceId'),
        'ccsp-application-id': parameters.getParameter('appId'),
        'offset': '1',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': str(len(data)),
        'Host': parameters.getParameter('host'),
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.10.0',
        'Stamp': stamps.getStamp()}

    try:
        response = kiahttp.postHTTP(url = url, data = data, headers = headers, timeout = parameters.getParameter('statusTimeout'))
    except:
        raise
        
    return

def getStatusFull(vehicleId):  
    soclogging.logDebug(2, "Receiving current status from vehicle")

    statusDict = {
    }
    
    url = parameters.getParameter('baseUrl') + '/api/v2/spa/vehicles/' + vehicleId + '/status'
    headers = {
        'Authorization': parameters.getParameter('controlToken'),
        'ccsp-device-id': parameters.getParameter('deviceId'),
        'Content-Type': 'application/json',
        'Stamp': stamps.getStamp()}

    try:
        response = kiahttp.getHTTP(url = url, headers = headers, timeout = parameters.getParameter('statusTimeout'))
    except:
        raise
        
    try:
        responseDict = json.loads(response)
    except:
        soclogging.logDebug(1, "Receiving current status failed, invalid response")
        soclogging.logDebug(2, response)
        raise
        
    try:
        statusDict['soc12v'] = int(responseDict['resMsg']['battery']['batSoc'])
    except:
        statusDict['soc12v'] = 100
        pass

    try:
        statusDict['time'] = timeToStamp(responseDict['resMsg']['time'])
        statusDict['socev'] = int(responseDict['resMsg']['evStatus']['batteryStatus'])
        statusDict['vehicleStatus'] = responseDict['resMsg']
    except:
        soclogging.logDebug(1, "Receiving current status failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    return statusDict   