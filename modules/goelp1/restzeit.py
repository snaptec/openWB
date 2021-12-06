import time
from datetime import datetime
from time import gmtime
from time import strftime
import fhem

#################################### FHEM  ########################################
fh = fhem.Fhem(server="192.168.178.75", protocol="http", port=8083, username="fort", password="user1@")

fhem_device_hyundai = "Bluelink"
fhem_device_cupra = "my_cupra"
fhem_device_lp = "openWB"

def DebugLog(message):
    #local_time = datetime.now(timezone.utc).astimezone()
    local_time= datetime.now()
    #print(local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ": PID: "+ Pid +": " + message) 

def openWBLog(message):
    #local_time = datetime.now(timezone.utc).astimezone()
    local_time = datetime.now()
    log = (local_time.strftime(format = "%Y-%m-%d %H:%M:%S") + ":" 'restzeit_lp1 :' +message + '\n')
    try:
        #print(log)
        # Versuche in ramdisk log zu schreiben
        with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
            f.write(log)
    except:
        #2. Versuch mit print 
        DebugLog(message)  

def loadpoint():
    global kwh_percent
    cupra_accu_capacity = fh.get_device_attribute(fhem_device_cupra, "Accu")*0.01
    hyundai_accu_capacity = fh.get_device_attribute(fhem_device_hyundai, "Accu")*0.01
    loadpoint_assignment = fh.get_device_reading(fhem_device_lp, "loadpoint_assignment")
    loadpoint_assignment = loadpoint_assignment["Value"]
    openWBLog("Loadpoint Assignment:"+str(loadpoint_assignment))
    if loadpoint_assignment == "LP1_Hyundai_LP2_Cupra":
        kwh_percent = hyundai_accu_capacity
    elif loadpoint_assignment == "LP2_Hyundai_LP1_Cupra":
        kwh_percent = cupra_accu_capacity
    openWBLog("Accu Capacity:"+str(kwh_percent))
    return kwh_percent

def readVal(filePath):
    f = open(filePath, 'r')
    val = f.readline()
    val = int(val)
    f.close()
    return val

loadpoint()
current_soc = readVal('/var/www/html/openWB/ramdisk/soc')
# print(current_soc)
current_watt = readVal('/var/www/html/openWB/ramdisk/llaktuell')
current_watt = current_watt / 1000
# print(current_watt)

loading_soc = 100 - current_soc
# print(loading_soc)
soc_in_kwh = kwh_percent * loading_soc
# print(soc_in_kwh)
time_now = time.time()
now = time.localtime()
if now.tm_isdst == 1:
    # print("Sommerzeit")
    offset_time = 7200
else:
    # print("Winterzeit")
    offset_time = 3600


if current_watt >= 1:
    estimate_time = soc_in_kwh / current_watt
    # print(estimate_time)
    estimate_time = round(estimate_time,2)
    estimate_time = str(estimate_time)
    a, b = estimate_time.split(".")
    a = float(a)*3600
    b = float(b)*60
    full_time = (a + b + time_now + offset_time)
    # openWBLog("Full Time:"+str(full_time))
    finish_time = time.strftime("%H:%M:%S", gmtime(full_time))
    # openWBLog("Finish Time:"+str(finish_time))
    with open('/var/www/html/openWB/ramdisk/goelp1estimatetime', 'w') as f:
        f.write(str(finish_time))
    # print(finish_time)
else:
     with open('/var/www/html/openWB/ramdisk/goelp1estimatetime', 'w') as f:
        f.write(str("--:--"))
