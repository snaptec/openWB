import json

import time
import parameters
import soclogging
import kiaauth
import kiaif


def DownloadSoC():
    soclogging.logDebug(0, "SoC download starting")
    now = int(time.time())

    auxData = {}

    try:
        kiaauth.updateAuthToken()
        kiaauth.requestNewControlToken()
    except:
        soclogging.logDebug(0, "Login failed")
        raise

    try:
        vehicleId = kiaif.getVehicleId(parameters.getParameter('vehicleVin'))
        status = kiaif.getStatusCached(vehicleId)
    except:
        soclogging.logDebug(0, "Collecting data from server failed")
        raise

    try:
        auxData['vehicleLocation'] = status['vehicleLocation']
        auxData['vehicleStatus'] = status['vehicleStatus']
        auxData['odometer'] = status['odometer']
    except:
        pass

    if (now - status['time']) < (parameters.getParameter('cacheValid')) and status['socev'] > 0:
        soclogging.logDebug(2, "Cached data is current")
    else:
        if status['soc12v'] < parameters.getParameter('soc12vLimit'):
            soclogging.logDebug(0, "12 V-battery low - 12 V-SoC: " + cachedStatus['soc12v'] + " %; Download cancelled")
            raise RuntimeError

        try:
            kiaif.doPrewakeup(vehicleId)
            status = kiaif.getStatusFull(vehicleId)
        except:
            soclogging.logDebug(0, "Collecting data from vehicle failed")
            raise

        try:
            auxData['vehicleStatus'] = status['vehicleStatus']
        except:
            pass

    if status['soc12v'] >= 80:
        soclogging.logDebug(2, "Received SoC (12 V-battery): " + str(status['soc12v']) + "%")
    elif status['soc12v'] >= 70 and status['soc12v'] < 80:
        soclogging.logDebug(1, "Received SoC (12 V-battery): " + str(status['soc12v']) + "%")
    elif status['soc12v'] < 70:
        soclogging.logDebug(0, "Received SoC (12 V-battery): " + str(status['soc12v']) + "%")

    soc = status['socev']
    soclogging.logDebug(0, "Received SoC (HV-battery): " + str(soc) + "%")

    try:
        f = open(parameters.getParameter('auxDataFile'), 'w')
        f.write(json.dumps(auxData))
        f.close()
    except:
        pass

    soclogging.logDebug(1, "SoC download ending")

    return soc
