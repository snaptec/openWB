import time

import parameters
import soclogging
import state
import soc_external
import abrp

def doExternalUpdate():
    attempt = 0
    
    if state.getState('lastSuccess') == 1:
        maxAttempt = 3
    else:
        maxAttempt = 1
        
    while attempt < maxAttempt:
        try:
            soc = soc_external.DownloadSoC()
        except:
            soc = 0
            raise
            
        if soc > 0:
            saveSoc(soc, 0)
            state.setState('lastSuccess', 1)
            break
        else:
            attempt += 1
            state.setState('lastSuccess', 0)
            if attempt < maxAttempt:
                soclogging.logDebug(2, "Retrying in 60 Seconds...")
                time.sleep(60)
    
    return
    
def doManualUpdate():  
    try:
        f = open(parameters.getParameter('meterFile'), 'r')
        currentMeter = float(f.read())
        f.close()
    except:
        soclogging.logDebug(2, "Could not find current meter file")
        raise
                
    try:
        lastMeter = state.getState('lastMeter')
        lastSoc = state.getState('lastSoc')
        f.close()
    except:
        raise
        
    batterySize = parameters.getParameter('batterySize')
    efficiency = parameters.getParameter('efficiency')
    meterDiff = currentMeter - lastMeter
    meterDiffEff = meterDiff * (efficiency / 100)
    socDiff = 100 * (meterDiffEff / batterySize)
    newSoc = int(max(min(lastSoc + socDiff, 100), 1))
    
    soclogging.logDebug(2, "Charged since last update: " + '{:.3f}'.format(meterDiff) + " kWh = " + '{:.3f}'.format(meterDiffEff) + " kWh @ " + '{:.0f}'.format(efficiency) + "% efficency")
    soclogging.logDebug(2, "Charged since last update: " + '{:.3f}'.format(meterDiffEff) + " kWh of " + '{:.0f}'.format(batterySize) + " kWh = " + '{:.2f}'.format(socDiff) + "% SoC")
    soclogging.logDebug(1, "Estimated SoC: " + '{:.0f}'.format(lastSoc) + "% (last update) + " + '{:.2f}'.format(socDiff) + "% (extrapolation) = " + '{:.0f}'.format(newSoc) + "% SoC")
    
    saveSoc(newSoc, 1)
    
    return
    
def saveSoc(soc, manual):
    try:
        f = open(parameters.getParameter('currentSocFile'), 'r')
        socOld = int(f.read())
        f.close()
    except:
        socOld = 0
        pass
        
    try:
        f = open(parameters.getParameter('currentSocFile'), 'w')
        f.write(str(int(soc)))
        f.close()
    except:
        raise
        
    try:
        if (parameters.getParameter('abrpEnable') == 1) and ((manual == 0) or (soc != socOld)):
            abrp.pushABRP(soc)
    except:
        pass
    
    if manual == 0:    
        try:
            f = open(parameters.getParameter('meterFile'), 'r')
            meter = float(f.read())
            f.close()
        except:
            meter = 0
        
        try:
            state.setState('lastSoc', soc)
            state.setState('lastMeter', meter)
            state.setState('unplug', 0)
            state.setState('charged', 0)
        except:
            raise
        
    return