#!/usr/bin/env python3
import pprint
import asyncio
import logging
import inspect
import json
import time
import sys
import os
import paho.mqtt.client as mqtt
from   aiohttp import ClientSession
from   datetime import datetime
import getopt
    

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

try:
    from skodaconnect import Connection
    from skodaconnect.__version__ import __version__ as lib_version    
except ModuleNotFoundError:
    print("callskoda.py Unable to import library")
    sys.exit(1)

## Defaults
username="none"
password="none"


debug=0
lp=1
carinfo=0
mqttskoda=0

        
				
try:
	opts, args = getopt.getopt(sys.argv[1:], 'd:p:u:l:CQcq', ['username=', 'password=', 'lp=', 'debug=', 'car', 'MQTT'])
except getopt.error as msg:
	sys.stdout = sys.stderr
	print(msg)
	print("""usage: %s [-u|-p|-l|-d|-c|-q]
	-u[sername], -p[assword]: username and passwort
	-c|--car  carinfo schreiben
	-q|--MQTT 
	-l[p]: Ladepunkt (1 oder 2)
	-d: debug level 0,1,2""" % sys.argv[0])
	sys.exit(2)
for opt, arg in opts:
	#print(f"{opt} = [{arg}] ")
	if opt in ('-u', '--username'):
		username=arg
		password=''      # must follow username
	elif opt in ('-p', '--password'):
		password=arg
	elif opt in ('-l', '--lp'):
		lp=int(arg)
	elif opt in ('-c', '--car'):
		carinfo=1
	elif opt in ('-q', '--MQTT'):
		mqttskoda=1
	elif opt in ('-d', '--debug'):
		debug=int(arg)
    

if debug < 2:
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.DEBUG)
_LOGGER = logging.getLogger(__name__)

_LOGGER.info(f"{str(sys.argv)}")



if debug>0: print( f"callskoda.py for LP{lp} debug:{debug} car:{carinfo} mqtt:{mqttskoda}") 
   

RESOURCES = [
#    "adblue_level",
#    "auxiliary_climatisation",
    "battery_level",
    "charge_max_ampere",
#    "charger_action_status",
    "charging",
    "charging_cable_connected",
    "charging_cable_locked",
    "charging_time_left",
#    "climater_action_status",
    "climatisation_target_temperature",
    "climatisation_without_external_power",
#    "combined_range",
    "combustion_range",
#    "departure1",           # wird einzel extra gemacht
#    "departure2",           # wird einzel extra gemacht
#    "departure3",           # wird einzel extra gemacht
    "distance",
    "door_closed_left_back",
    "door_closed_left_front",
    "door_closed_right_back",
    "door_closed_right_front",
    "door_locked",
    "electric_climatisation",
#   "electric_range",
    "energy_flow",
    "external_power",
#   "fuel_level",
    "hood_closed",
    "last_connected",
#    "lock_action_status",
#   "oil_inspection",
#   "oil_inspection_distance",
    "outside_temperature",
    "parking_light",
    "parking_time",
#   "pheater_heating",
#   "pheater_status",
#    "pheater_ventilation",
#    "position",  # wird einzeln extar gemacht
#    "refresh_action_status",
#   "refresh_data",
#   "request_in_progress",
#    "request_results",
#    "requests_remaining",
    "service_inspection",
    "service_inspection_distance",
#    "sunroof_closed",
#    "trip_last_average_auxillary_consumption",
    "trip_last_average_electric_consumption",
#   "trip_last_average_fuel_consumption",
    "trip_last_average_speed",
    "trip_last_duration",
#    "trip_last_entry"       # wird einzel extra gemacht
    "trip_last_length",
    "trip_last_recuperation",
    "trip_last_average_recuperation",
    "trip_last_total_electric_consumption",
    "trunk_closed",
    "trunk_locked",
    "vehicle_moving",
#    "window_closed_left_back",
#    "window_closed_left_front",
#    "window_closed_right_back",
#    "window_closed_right_front",
#    "window_heater",
#    "windows_closed",
    "model",
    "nickname",
    "vin",
#    "json"
]

ToMQtt = [
    "battery_level",
    "charge_max_ampere",
    "charging",
    "charging_cable_connected",
    "charging_cable_locked",
    "charging_time_left",
    "combustion_range",
    "outside_temperature",
    "trip_last_average_electric_consumption",
    "ledColor",
    "ledState",
]

async def main():
    """Main method."""

    all={}  # fields
    if debug>0: print(f'Init Skoda Connect library, version {lib_version}')
    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        if debug>0: print(f"Initiating new session to Skoda Connect with {username} as username")
        if debug>0:
            connection = Connection(session, username, password, True)
        else:
            connection = Connection(session, username, password, False)
        
        if debug>0: print("Attempting to login to the Skoda Connect service")
        if debug>0: print(datetime.now())
        if await connection.doLogin():
            if debug>0: print('Login success!')
            if debug>0: print(datetime.now())
            
            if( lib_version >= '1.1.3'):
                if debug>0: print('Fetching vehicles associated with account.')
                await connection.get_vehicles()
                timername='departuretimer'
            else:
                timername='timers'

            
            
            for vehicle in connection.vehicles:
                if( carinfo>0):
                    if debug>0: print(f" Writing /var/www/html/openWB/ramdisk/carinfo_{lp}.json") 
                    file=open(f"/var/www/html/openWB/ramdisk/carinfo_{lp}.json","w")
                    file.write( vehicle.json)
                    file.close()
                for prop in dir(vehicle):
                    func = f"vehicle.{prop}"
                    name = str(prop)
                    typ = type(eval(func))
                    try:
                        val = eval(func)
                        if( name in RESOURCES):
                            all[name]=val
                        else:
                            if debug>1: print(f"Skip {name}")
                    except:
                        pass
                all['ledColor']=vehicle.attrs.get('charger', {}).get('status',{}).get('ledStatusData',{}).get('ledColor',{}).get('content','')
                all['ledState']=vehicle.attrs.get('charger', {}).get('status',{}).get('ledStatusData',{}).get('ledState',{}).get('content','')
                all['position_lat']=vehicle.position.get('lat','')
                all['position_lng']=vehicle.position.get('lng','')
 
                #all['chargeMinLimit']     = vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerBasicSetting', {}).get('chargeMinLimit', 0)
                #all['targetTemperature']  = vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerBasicSetting', {}).get('targetTemperature', 0)
                
                ds = vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerList', {}).get('timer', False)
                timer = ds[0]
                timer.pop('timestamp', None)
                timer.pop('timerID', None)
                timer.pop('profileID', None)
                dp =  vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerProfileList', {}).get('timerProfile', False)
                timer.update(dp[0])
                timer.pop('timestamp', None)
                timer.pop('timerID', None)
                timer.pop('profileID', None)
                for td in timer:
                    all[f"timer/1/{td}"]=timer[td]

                ds = vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerList', {}).get('timer', False)
                timer = ds[1]
                timer.pop('timestamp', None)
                timer.pop('timerID', None)
                timer.pop('profileID', None)
                dp =  vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerProfileList', {}).get('timerProfile', False)
                timer.update(dp[1])
                timer.pop('timestamp', None)
                timer.pop('timerID', None)
                timer.pop('profileID', None)
                #all['dep2'] = json.dumps(timer)
                for td in timer:
                    all[f"timer/2/{td}"]=timer[td]

                ds = vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerList', {}).get('timer', False)
                timer = ds[2]
                timer.pop('timestamp', None)
                timer.pop('timerID', None)
                timer.pop('profileID', None)
                dp =  vehicle.attrs.get(timername, {}).get('timersAndProfiles', {}).get('timerProfileList', {}).get('timerProfile', False)
                timer.update(dp[2])
                timer.pop('timestamp', None)
                timer.pop('timerID', None)
                timer.pop('profileID', None)
                #all['dep3'] = json.dumps(timer)
                for td in timer:
                    all[f"timer/3/{td}"]=timer[td]
            
    for x in sorted(all):
        if debug>0: print(f"{x} = {all[x]}" )
                
                
                
    # Export to MQTT for Skoda 
    mclient = mqtt.Client("openWB-skoda_broker-" + str(os.getpid()))
    mclient.connect("localhost")
    _LOGGER.debug("MQTTT connect to localhost")
    mclient.loop(timeout=2.0)
    if( mqttskoda > 0):
        if debug>0: print("Write to /Skoda/")
        for x in all:
            val = all[x]
            field=f"Skoda/{x}"
            mclient.publish(str(field), payload=str(val), qos=0, retain=True)
            _LOGGER.debug("MQTTT publish %s %s", field, val) 
        mclient.loop(timeout=2.0)

    # Export to MQTT for openWB      
    for x in all:
        val = all[x]
        if x == 'battery_level' :
            field=f'openWB/set/lp/{lp}/%Soc'
            mclient.publish(str(field), payload=str(val), qos=0, retain=True)
            _LOGGER.debug("MQTTT publish %s %s", field, val) 
        if x in ToMQtt :
            field=f'openWB/lp/{lp}/Skoda_{x}'
            mclient.publish(str(field), payload=str(val), qos=0, retain=True)
            field=f'openWB/set/lp/{lp}/Skoda_{x}'
            mclient.publish(str(field), payload=str(val), qos=0, retain=True)
            _LOGGER.debug("MQTTT publish %s  %s", field, val) 
    mclient.loop(timeout=2.0)
    mclient.disconnect()
    _LOGGER.debug("MQTTT disconnect")
    return True
            

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
