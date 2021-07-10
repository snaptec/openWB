import sys

import parameters
import lock
import soclogging
import state
import trigger
import soc

def initialize(argsFile):
    try:
        parameters.loadParameters(argsFile)
        parameters.loadFileNames()
        parameters.loadBrandData()
    except:
        raise
        
    return

#---------------Main Function-------------------------------------------
def main():
    try:
        initialize(str(sys.argv[1]))
        
        lock.checkLockFile()
        lock.createLockFile()
    except:
        exit(1)
    
    soclogging.logDebug(1, "-------------------------------")    
    soclogging.logDebug(1, "Kia/Hyundai SoC Module starting")
              
    try:
        state.saveUnplugState()
        state.saveChargedState()
        
        if trigger.isDownloadTriggered() == 1:
            soc.doExternalUpdate()
        elif parameters.getParameter('manualCalc') == 1:
            if state.isCharging() == 1:
                soclogging.logDebug(2, "Manual calculation starting")
                soc.doManualUpdate()
        else: 
            soclogging.logDebug(2, "Nothing to do yet")
    except:
        pass
    
    try:
        state.saveTickTime()
    except:
        pass
        
    soclogging.logDebug(1, "Kia/Hyundai SoC Module ending")
    
    try:
        lock.purgeLockFile()
    except:
        exit(1)
        raise
    
    exit(0)

    
if __name__ == '__main__':
    main()
