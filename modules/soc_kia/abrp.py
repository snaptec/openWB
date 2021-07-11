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