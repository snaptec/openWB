import parameters
import requests
import time
import json
import state

import soclogging

def pushABRP(soc):
    now = int(time.time())
    apiKey = "49589dbf-37a8-4c22-a49c-7d62fe1a6531"
    userToken = parameters.getParameter('abrpToken')
    
    soclogging.logDebug(2, "Submitting ABRP-Data")
    
    url = "https://api.iternio.com/1/tlm/send?api_key=" + requests.utils.quote(apiKey) + "&token=" + requests.utils.quote(userToken)
    data = {'tlm': {'utc': now, 'soc': soc, 'is_charging': state.isCharging()}}
    
    try:
        f = open(parameters.getParameter('auxDataFile'), 'r')
        auxData = json.loads(f.read())
        f.close()        
        data['tlm']['odometer'] = auxData['odometer']['value']
        data['tlm']['lat'] = auxData['vehicleLocation']['coord']['lat']
        data['tlm']['lon'] = auxData['vehicleLocation']['coord']['lon']
        data['tlm']['speed'] = auxData['vehicleLocation']['speed']['value']
        data['tlm']['is_parked'] = auxData['vehicleStatus']['doorLock']
    except:
        pass
        
    try:
        response = requests.post(url, json = data)
    except requests.Timeout as err:
        soclogging.logDebug(1, "ABRP - Connection Timeout")
        pass
    except:
        soclogging.logDebug(1, "ABRP - HTTP Error")
        pass
    
    if response.status_code != 200:
        soclogging.logDebug(1, 'ABRP - Request failed, StatusCode: ' + str(response.status_code) + ' - Error: '+ str(response.text))   
    
    return