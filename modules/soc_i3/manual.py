import base64
import json
import sys

# ---------------Main Function-------------------------------------------
def main():
    try:
        argsStr = base64.b64decode(str(sys.argv[1])).decode('utf-8')
        argsDict = json.loads(argsStr)
        
        socfile = str(argsDict["socfile"])
        meterfile = str(argsDict["meterfile"])
        statefile = str(argsDict["statefile"])
        batterysize = float(argsDict["batterysize"])
        efficiency = float(argsDict["efficiency"])
    except:
        print("Parameters could not be processed")
        raise

    try:     
        with open(meterfile, 'r') as f:
            currentMeter = float(f.read())
        with open(statefile, 'r') as f:
            state = json.loads(f.read())
        lastMeter = state["meter"]
        lastSoc = state["soc"]
        
        meterDiff = currentMeter - lastMeter
        meterDiffEff = meterDiff * (efficiency / 100)
        socDiff = 100 * (meterDiffEff / batterysize)
        newSoc = int(max(min(lastSoc + socDiff, 100), 1))
    
        with open(socfile, 'w') as f:
            f.write(str(int(newSoc)))            
    except:
        print("SoC calculation failed")
        raise 
        
if __name__ == '__main__':
    main()
