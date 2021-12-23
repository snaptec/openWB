import json
import soclogging

paramDict = {}

def getParameter(key):
    global paramDict
    
    if key in paramDict:
        value = paramDict[key]
    else:
        raise RuntimeError
        
    return value
    
def setParameter(key, value):
    global paramDict
    
    paramDict[key] = value
    
    return

def loadParameters(argsFile):
    setParameter('reqTimeout', 60)
    setParameter('statusTimeout', 150)

    try:
        f = open(argsFile, 'r')
        argsStr = f.read()
        argsDict = json.loads(argsStr)
        f.close()
        
        setParameter('moduleName', str(argsDict['moduleName']))
        setParameter('chargePoint', str(argsDict['chargePoint']))
        setParameter('debugLevel', int(argsDict['debugLevel']))   
        setParameter('timerInterval',int(argsDict['timerInterval']))
        setParameter('manualCalc', int(argsDict['manualCalc']))
        setParameter('batterySize', float(argsDict['batterySize']))
        setParameter('efficiency', float(argsDict['efficiency']))
        setParameter('abrpEnable', int(argsDict['abrpEnable']))
        setParameter('abrpToken', str(argsDict['abrpToken']))
        setParameter('accountName', str(argsDict['accountName']))
        setParameter('accountPassword', str(argsDict['accountPassword']))
        setParameter('accountPin', str(argsDict['accountPin']))
        setParameter('vehicleVin', str(argsDict['vehicleVin']))
        setParameter('ramDiskDir', str(argsDict['ramDiskDir']))
        setParameter('advEnable', int(argsDict['advEnable']))
        
        if getParameter('advEnable') == 0:
            setParameter('cacheValid', 10 * 60)
            setParameter('soc12vLimit', 20)
            setParameter('timerMinInterval', 15 * 60)
            setParameter('timerIntervalUnplug', getParameter('timerInterval'))
        else:
            setParameter('cacheValid', (int(argsDict['advCacheValid']) * 60))
            setParameter('soc12vLimit', int(argsDict['adv12vLimit']))
            setParameter('timerMinInterval', (int(argsDict['advRateLimit']) * 60))
            setParameter('timerIntervalUnplug', int(argsDict['advIntUnplug']))
    except:
        raise

    return
    
def loadFileNames():
    try:
        ramDiskDir = getParameter('ramDiskDir')
        
        setParameter('logFile', ramDiskDir + "/soc.log")
        setParameter('lockFile', ramDiskDir + "/soc_" + getParameter('moduleName')+ "_lp" + getParameter('chargePoint') + "_lock")
        setParameter('tokenFile', ramDiskDir + "/soc_" + getParameter('moduleName')+ "_lp" + getParameter('chargePoint') + "_token")
        setParameter('stateFile', ramDiskDir + "/soc_" + getParameter('moduleName')+ "_lp" + getParameter('chargePoint') + "_state")
        setParameter('auxDataFile', ramDiskDir + "/soc_" + getParameter('moduleName')+ "_lp" + getParameter('chargePoint') + "_auxdata")
        
        if getParameter('chargePoint') == '1':
            setParameter('currentSocFile', ramDiskDir + "/soc")
            setParameter('timerFile', ramDiskDir + "/soctimer")
            setParameter('meterFile', ramDiskDir + "/llkwh")
            setParameter('isPluggedFile', ramDiskDir + "/plugstat")
            setParameter('isChargingFile', ramDiskDir + "/chargestat")
        elif getParameter('chargePoint') == '2':
            setParameter('currentSocFile', ramDiskDir + "/soc1")
            setParameter('timerFile', ramDiskDir + "/soctimer1")
            setParameter('meterFile', ramDiskDir + "/llkwhs1")
            setParameter('isPluggedFile', ramDiskDir + "/plugstats1")
            setParameter('isChargingFile', ramDiskDir + "/chargestats1")
        else:
            raise RuntimeError
    except:
        raise
        
    return
    
def loadBrandData():
    vin = getParameter('vehicleVin')
    
    if vin[:2]=='KN' or vin[:3]=='U5Y' or vin[:3]=='U6Z':
        setParameter('brand', 'kia')
        #soclogging.logDebug(2, "Vehicle identified as Kia")
    elif vin[:3]=='KMH' or vin[:3]=='TMA':
        setParameter('brand', 'hyundai')
        #soclogging.logDebug(2, "Vehicle identified as Hyundai")
    else:
        setParameter('brand', '')
        soclogging.logDebug(2, "Vehicle WMI unknown")
        raise RuntimeError
    
    if getParameter('brand') == 'kia':
        setParameter('host', 'prd.eu-ccapi.kia.com:8080')
        setParameter('baseUrl', 'https://' + getParameter('host'))
        setParameter('clientId', 'fdc85c00-0a2f-4c64-bcb4-2cfb1500730a')
        setParameter('authClientId', '572e0304-5f8d-4b4c-9dd5-41aa84eed160')
        setParameter('appId', 'e7bcd186-a5fd-410d-92cb-6876a42288bd')
        setParameter('GCMSenderId', '345127537656')
        setParameter('basicToken', 'Basic ZmRjODVjMDAtMGEyZi00YzY0LWJjYjQtMmNmYjE1MDA3MzBhOnNlY3JldA==')
    if getParameter('brand') == 'hyundai':
        setParameter('host', 'prd.eu-ccapi.hyundai.com:8080')
        setParameter('baseUrl', 'https://' + getParameter('host'))
        setParameter('clientId', '6d477c38-3ca4-4cf3-9557-2a1929a94654')
        setParameter('authClientId', '64621b96-0f0d-11ec-82a8-0242ac130003')
        setParameter('appId', '014d2225-8495-4735-812d-2616334fd15d')
        setParameter('GCMSenderId', '414998006775')
        setParameter('basicToken', 'Basic NmQ0NzdjMzgtM2NhNC00Y2YzLTk1NTctMmExOTI5YTk0NjU0OktVeTQ5WHhQekxwTHVvSzB4aEJDNzdXNlZYaG10UVI5aVFobUlGampvWTRJcHhzVg==')
    
    return