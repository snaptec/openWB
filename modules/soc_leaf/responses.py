# Copyright 2016 Jason Horne
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from datetime import timedelta, datetime
import pycarwings2

log = logging.getLogger(__name__)


def _time_remaining(t):
    minutes = float(0)
    if t:
        if ("hours" in t) and t["hours"]:
            minutes = 60 * float(t["hours"])
        elif ("HourRequiredToFull" in t) and t["HourRequiredToFull"]:
            minutes = 60 * float(t["HourRequiredToFull"])
        if ("minutes" in t) and t["minutes"]:
            minutes += float(t["minutes"])
        elif ("MinutesRequiredToFull" in t) and t["MinutesRequiredToFull"]:
            minutes += float(t["MinutesRequiredToFull"])

    return minutes


class CarwingsResponse:
    def __init__(self, response):
        op_result = None
        if ("operationResult" in response):
            op_result = response["operationResult"]
        elif ("OperationResult" in response):
            op_result = response["OperationResult"]

        # seems to indicate that the vehicle cannot be reached
        if ("ELECTRIC_WAVE_ABNORMAL" == op_result):
            log.error("could not establish communications with vehicle")
            raise pycarwings2.CarwingsError("could not establish communications with vehicle")

    def _set_cruising_ranges(self, status, off_key="cruisingRangeAcOff", on_key="cruisingRangeAcOn"):
        if off_key in status:
            self.cruising_range_ac_off_km = float(status[off_key]) / 1000
        if on_key in status:
            self.cruising_range_ac_on_km = float(status[on_key]) / 1000

    def _set_timestamp(self, status):
        self.timestamp = datetime.strptime(status["timeStamp"], "%Y-%m-%d %H:%M:%S")   # "2016-01-02 17:17:38"


class CarwingsInitialAppResponse(CarwingsResponse):
    def __init__(self, response):
        CarwingsResponse.__init__(self, response)
        self.baseprm = response["baseprm"]


class CarwingsLoginResponse(CarwingsResponse):
    """
        example JSON response to login:
        {
            "status":200,
            "message":"success",
            "sessionId":"12345678-1234-1234-1234-1234567890",
            "VehicleInfoList": {
                "VehicleInfo": [
                    {
                        "charger20066":"false",
                        "nickname":"LEAF",
                        "telematicsEnabled":"true",
                        "vin":"1ABCDEFG2HIJKLM3N"
                    }
                ],
                "vehicleInfo": [
                    {
                        "charger20066":"false",
                        "nickname":"LEAF",
                        "telematicsEnabled":"true",
                        "vin":"1ABCDEFG2HIJKLM3N"
                    }
                ]
            },
            "vehicle": {
                "profile": {
                    "vin":"1ABCDEFG2HIJKLM3N",
                    "gdcUserId":"FG12345678",
                    "gdcPassword":"password",
                    "encAuthToken":"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ",
                    "dcmId":"123456789012",
                    "nickname":"Alpha124",
                    "status":"ACCEPTED",
                    "statusDate": "Aug 15, 2015 07:00 PM"
                }
            },
            "EncAuthToken":"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "CustomerInfo": {
                "UserId":"AB12345678",
                "Language":"en-US",
                "Timezone":"America/New_York",
                "RegionCode":"NNA",
                "OwnerId":"1234567890",
                "Nickname":"Bravo456",
                "Country":"US",
                "VehicleImage":"/content/language/default/images/img/ph_car.jpg",
                "UserVehicleBoundDurationSec":"999971200",
                "VehicleInfo": {
                    "VIN":"1ABCDEFG2HIJKLM3N",
                    "DCMID":"201212345678",
                    "SIMID":"12345678901234567890",
                    "NAVIID":"1234567890",
                    "EncryptedNAVIID":"1234567890ABCDEFGHIJKLMNOP",
                    "MSN":"123456789012345",
                    "LastVehicleLoginTime":"",
                    "UserVehicleBoundTime":"2015-08-17T14:16:32Z",
                    "LastDCMUseTime":""
                }
            },
            "UserInfoRevisionNo":"1"
        }
    """
    def __init__(self, response):
        CarwingsResponse.__init__(self, response)

        profile = response["vehicle"]["profile"]
        self.gdc_user_id = profile["gdcUserId"]
        self.dcm_id = profile["dcmId"]
        self.vin = profile["vin"]

        # vehicleInfo block may be top level, or contained in a VehicleInfoList object;
        # why it's sometimes one way and sometimes another is not clear.
        if "VehicleInfoList" in response:
            self.nickname = response["VehicleInfoList"]["vehicleInfo"][0]["nickname"]
            self.custom_sessionid = response["VehicleInfoList"]["vehicleInfo"][0]["custom_sessionid"]
        elif "vehicleInfo" in response:
            self.nickname = response["vehicleInfo"][0]["nickname"]
            self.custom_sessionid = response["vehicleInfo"][0]["custom_sessionid"]

        customer_info = response["CustomerInfo"]
        self.tz = customer_info["Timezone"]
        self.language = customer_info["Language"]
        self.user_vehicle_bound_time = customer_info["VehicleInfo"]["UserVehicleBoundTime"]

        self.leafs = [{
            "vin": self.vin,
            "nickname": self.nickname,
            "bound_time": self.user_vehicle_bound_time
        }]


class CarwingsBatteryStatusResponse(CarwingsResponse):
    """
        Note that before December 2018 this returned a response. Between Dec-2018 and Aug-2019
        it did not return a response from the Nissan Servers.  As of Aug 2019 a response is now
        returned again.

        # Original
        {
            "status": 200,
            "message": "success",
            "responseFlag": "1",
            "operationResult": "START",
            "timeStamp": "2016-01-02 17:17:38",
            "cruisingRangeAcOn": "115328.0",
            "cruisingRangeAcOff": "117024.0",
            "currentChargeLevel": "0",
            "chargeMode": "220V",
            "pluginState": "CONNECTED",
            "charging": "YES",
            "chargeStatus": "CT",
            "batteryDegradation": "10",
            "batteryCapacity": "12",
            "timeRequiredToFull": {
                "hours": "",
                "minutes": ""
            },
            "timeRequiredToFull200": {
                "hours": "",
                "minutes": ""
            },
            "timeRequiredToFull200_6kW": {
                "hours": "",
                "minutes": ""
            }
        }

        # As at 21/01/2019 for a 30kWh Leaf now seems that
        # BatteryStatusCheckResultRequest.php always returns this
        # regardless of battery status.
        {
            "status":200,
            "responseFlag":"0"
        }

        {
            "status":200,
            "message":"success",
            "responseFlag":"1",
            "operationResult":"START",
            "timeStamp":"2016-02-14 20:28:45",
            "cruisingRangeAcOn":"107136.0",
            "cruisingRangeAcOff":"115776.0",
            "currentChargeLevel":"0",
            "chargeMode":"NOT_CHARGING",
            "pluginState":"QC_CONNECTED",
            "charging":"YES",
            "chargeStatus":"CT",
            "batteryDegradation":"11",
            "batteryCapacity":"12",
            "timeRequiredToFull":{
                "hours":"",
                "minutes":""
            },
            "timeRequiredToFull200":{
                "hours":"",
                "minutes":""
            },
            "timeRequiredToFull200_6kW":{
                "hours":"",
                "minutes":""
            }
        }

        # As at 22/08/2019 for a 30kWh Leaf now seesm that
        # BatteryStatusCheckResultRequest.php returns data again
        # after polling a number of times.
        {
                "status": 200,
                "responseFlag": "1",
                "operationResult": "START",
                "timeStamp": "2019-08-22 10:26:51",
                "cruisingRangeAcOn": "129000.0",
                "cruisingRangeAcOff": "132000.0",
                "currentChargeLevel": "0",
                "chargeMode": "NOT_CHARGING",
                "pluginState": "NOT_CONNECTED",
                "charging": "NO",
                "chargeStatus": "0",
                "batteryDegradation": "180",
                "batteryCapacity": "240",
                "timeRequiredToFull": {
                        "hours": "11",
                        "minutes": "30"
                },
                "timeRequiredToFull200": {
                        "hours": "6",
                        "minutes": "30"
                },
                "timeRequiredToFull200_6kW": {
                        "hours": "2",
                        "minutes": "30"
                }
        }

    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        self._set_timestamp(status)
        self._set_cruising_ranges(status)

        self.answer = status

        self.battery_capacity = status["batteryCapacity"]
        self.battery_degradation = status["batteryDegradation"]

        self.is_connected = ("NOT_CONNECTED" != status["pluginState"])    # fun double negative
        self.plugin_state = status["pluginState"]

        self.charging_status = status["chargeMode"]

        self.is_charging = ("YES" == status["charging"])

        self.is_quick_charging = ("RAPIDLY_CHARGING" == status["chargeMode"])
        self.is_connected_to_quick_charger = ("QC_CONNECTED" == status["pluginState"])

        self.time_to_full_trickle = timedelta(minutes=_time_remaining(status["timeRequiredToFull"]))
        self.time_to_full_l2 = timedelta(minutes=_time_remaining(status["timeRequiredToFull200"]))
        self.time_to_full_l2_6kw = timedelta(minutes=_time_remaining(status["timeRequiredToFull200_6kW"]))

        # For some leafs the battery_percent is not returned
        self.battery_percent = 100 * float(self.battery_degradation) / 12


class CarwingsLatestClimateControlStatusResponse(CarwingsResponse):
    """
    climate control on:
        {
            "status":200,
            "message":"success",
            "RemoteACRecords":{
                "OperationResult":"START_BATTERY",
                "OperationDateAndTime":"Feb 10, 2016 10:22 PM",
                "RemoteACOperation":"START",
                "ACStartStopDateAndTime":"Feb 10, 2016 10:23 PM",
                "CruisingRangeAcOn":"107712.0",
                "CruisingRangeAcOff":"109344.0",
                "ACStartStopURL":"",
                "PluginState":"NOT_CONNECTED",
                "ACDurationBatterySec":"900",
                "ACDurationPluggedSec":"7200"
            },
            "OperationDateAndTime":""
        }

    climate control off:
        {
            "status":200,
            "message":"success",
            "RemoteACRecords":{
                "OperationResult":"START",
                "OperationDateAndTime":"Feb 10, 2016 10:26 PM",
                "RemoteACOperation":"STOP",
                "ACStartStopDateAndTime":"Feb 10, 2016 10:27 PM",
                "CruisingRangeAcOn":"111936.0",
                "CruisingRangeAcOff":"113632.0",
                "ACStartStopURL":"",
                "PluginState":"NOT_CONNECTED",
                "ACDurationBatterySec":"900",
                "ACDurationPluggedSec":"7200"
            },
            "OperationDateAndTime":""
        }

    error:
        {
            "status":200,
            "RemoteACRecords":{
                "OperationResult":"ELECTRIC_WAVE_ABNORMAL",
                "OperationDateAndTime":"2018/04/08 10:00",
                "RemoteACOperation":"START",
                "ACStartStopDateAndTime":"08-Apr-2018 11:06",
                "ACStartStopURL":"",
                "PluginState":"INVALID",
                "ACDurationBatterySec":"900",
                "ACDurationPluggedSec":"7200",
                "PreAC_unit":"C",
                "PreAC_temp":"22"
            }
        }
    noinfo (from a 2014 24kWh Leaf):
        {
            "status":200,
            "RemoteACRecords":[]
        }

    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status["RemoteACRecords"])
        racr = status["RemoteACRecords"]

        self._set_cruising_ranges(racr, on_key="CruisingRangeAcOn", off_key="CruisingRangeAcOff")

        # If no empty RemoteACRecords list is returned then assume CC is off.
        if type(racr) is not dict:
            self.is_hvac_running = False
        else:
            # Seems to be running only if both of these contain "START".
            self.is_hvac_running = (
                racr["OperationResult"] and
                racr["OperationResult"].startswith("START") and
                racr["RemoteACOperation"] == "START"
            )


class CarwingsStartClimateControlResponse(CarwingsResponse):
    """
        {
            "status":200,
            "message":"success",
            "responseFlag":"1",
            "operationResult":"START_BATTERY",
            "acContinueTime":"15",
            "cruisingRangeAcOn":"106400.0",
            "cruisingRangeAcOff":"107920.0",
            "timeStamp":"2016-02-05 12:59:46",
            "hvacStatus":"ON"
        }
    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        self._set_timestamp(status)
        self._set_cruising_ranges(status)

        self.operation_result = status["operationResult"]     # e.g. "START_BATTERY", ...?
        self.ac_continue_time = timedelta(minutes=float(status["acContinueTime"]))
        self.hvac_status = status["hvacStatus"]               # "ON" or "OFF"
        self.is_hvac_running = ("ON" == self.hvac_status)


class CarwingsStopClimateControlResponse(CarwingsResponse):
    """
        {
            "status":200,
            "message":"success",
            "responseFlag":"1",
            "operationResult":"START",
            "timeStamp":"2016-02-09 03:32:51",
            "hvacStatus":"OFF"
        }
    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        self._set_timestamp(status)
        self.hvac_status = status["hvacStatus"]                # "ON" or "OFF"
        self.is_hvac_running = ("ON" == self.hvac_status)


class CarwingsClimateControlScheduleResponse(CarwingsResponse):
    """
        {
            "status":200,
            "message":"success",
            "LastScheduledTime":"Feb  9, 2016 05:39 PM",
            "ExecuteTime":"2016-02-10 01:00:00",
            "DisplayExecuteTime":"Feb  9, 2016 08:00 PM",
            "TargetDate":"2016/02/10 01:00"
        }
    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        self.display_execute_time = status["DisplayExecuteTime"]         # displayable, timezone-adjusted
        self.execute_time = datetime.strptime(status["ExecuteTime"] + " UTC", "%Y-%m-%d %H:%M:%S %Z")   # GMT
        self.display_last_scheduled_time = status["LastScheduledTime"]   # displayable, timezone-adjusted
        self.last_scheduled_time = datetime.strptime(status["LastScheduledTime"], "%b %d, %Y %I:%M %p")
        # unknown purpose; don't surface to avoid confusion
        # self.target_date = status["TargetDate"]


class CarwingsDrivingAnalysisResponse(CarwingsResponse):
    """
        {
            "status":200,
            "message":"success",
            "DriveAnalysisBasicScreenResponsePersonalData": {
                "DateSummary":{
                    "TargetDate":"2016-02-03",
                    "ElectricMileage":"4.4",
                    "ElectricMileageLevel":"3",
                    "PowerConsumptMoter":"295.2",
                    "PowerConsumptMoterLevel":"4",
                    "PowerConsumptMinus":"84.8",
                    "PowerConsumptMinusLevel":"3",
                    "PowerConsumptAUX":"17.1",
                    "PowerConsumptAUXLevel":"5",
                    "DisplayDate":"Feb  3, 16"
                },
                "ElectricCostScale":"miles/kWh"
            },
            "AdviceList":{
                "Advice":{
                    "title":"World Number of Trips Rankings (last week):",
                    "body":"The highest number of trips driven was 130 by a driver located in Japan."
                }
            }
        }
    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        summary = status["DriveAnalysisBasicScreenResponsePersonalData"]["DateSummary"]

        # avg energy economy, in units of 'electric_cost_scale' (e.g. miles/kWh)
        self.electric_mileage = summary["ElectricMileage"]
        # rating for above, scale of 1-5
        self.electric_mileage_level = summary["ElectricMileageLevel"]

        # "acceleration performance": "electricity used for motor activation over 1km", Watt-Hours
        self.power_consumption_moter = summary["PowerConsumptMoter"]
        # rating for above, scale of 1-5
        self.power_consumption_moter_level = summary["PowerConsumptMoterLevel"]

        # Watt-Hours generated by braking
        self.power_consumption_minus = summary["PowerConsumptMinus"]
        # rating for above, scale of 1-5
        self.power_consumption_minus_level = summary["PowerConsumptMinusLevel"]

        # Electricity used by aux devices, Watt-Hours
        self.power_consumption_aux = summary["PowerConsumptAUX"]
        # rating for above, scale of 1-5
        self.power_consumption_aux_level = summary["PowerConsumptAUXLevel"]

        self.display_date = summary["DisplayDate"]     # "Feb  3, 16"

        self.electric_cost_scale = status["DriveAnalysisBasicScreenResponsePersonalData"]["ElectricCostScale"]

        self.advice = [status["AdviceList"]["Advice"]]  # will contain "title" and "body"


class CarwingsLatestBatteryStatusResponse(CarwingsResponse):
    """
        # not connected to a charger
        {
            "status":200,
            "message":"success",
            "BatteryStatusRecords":{
                "OperationResult":"START",
                "OperationDateAndTime":"Feb  9, 2016 11:09 PM",
                "BatteryStatus":{
                    "BatteryChargingStatus":"NOT_CHARGING",
                    "BatteryCapacity":"12",
                    "BatteryRemainingAmount":"3",
                    "BatteryRemainingAmountWH":"",
                    "BatteryRemainingAmountkWH":""
                },
                "PluginState":"NOT_CONNECTED",
                "CruisingRangeAcOn":"39192.0",
                "CruisingRangeAcOff":"39744.0",
                "TimeRequiredToFull":{              # 120V
                    "HourRequiredToFull":"18",
                    "MinutesRequiredToFull":"30"
                },
                "TimeRequiredToFull200":{           # 240V, 3kW
                    "HourRequiredToFull":"6",
                    "MinutesRequiredToFull":"0"
                },
                "TimeRequiredToFull200_6kW":{       # 240V, 6kW
                    "HourRequiredToFull":"4",
                    "MinutesRequiredToFull":"0"
                },
                "NotificationDateAndTime":"2016/02/10 04:10",
                "TargetDate":"2016/02/10 04:09"
            }
        }

        # not connected to a charger - as at 21/01/2019 20:01 (for a 30kWh leaf)
        {
            "status":200,
            "BatteryStatusRecords": {
                "OperationResult":"START",
                "OperationDateAndTime":"21-Jan-2019 13:29",
                "BatteryStatus":{
                    "BatteryChargingStatus":"NOT_CHARGING",
                    "BatteryCapacity":"240",
                    "BatteryRemainingAmount":"220",
                    "BatteryRemainingAmountWH":"24480",
                    "BatteryRemainingAmountkWH":"",
                    "SOC":{
                        "Value":"91"
                    }
                },
                "PluginState":"NOT_CONNECTED",
                "CruisingRangeAcOn":"146000",
                "CruisingRangeAcOff":"168000",
                "TimeRequiredToFull":{
                    "HourRequiredToFull":"4",
                    "MinutesRequiredToFull":"30"
                },
                "TimeRequiredToFull200":{
                    "HourRequiredToFull":"3"
                    ,"MinutesRequiredToFull":"0"
                },
                "TimeRequiredToFull200_6kW":{
                    "HourRequiredToFull":"1",
                    "MinutesRequiredToFull":"30"
                },
                "NotificationDateAndTime":"2019/01/21 13:29",
                "TargetDate":"2019/01/21 13:29"
            }
        }


        # connected to a quick charger
        {
            "status":200,
            "message":"success",
            "BatteryStatusRecords":{
                "OperationResult":"START",
                "OperationDateAndTime":"Feb 14, 2016 03:28 PM",
                "BatteryStatus":{
                    "BatteryChargingStatus":"RAPIDLY_CHARGING",
                    "BatteryCapacity":"12",
                    "BatteryRemainingAmount":"11",
                    "BatteryRemainingAmountWH":"",
                    "BatteryRemainingAmountkWH":""
                },
                "PluginState":"QC_CONNECTED",
                "CruisingRangeAcOn":"107136.0",
                "CruisingRangeAcOff":"115776.0",
                "NotificationDateAndTime":"2016/02/14 20:28",
                "TargetDate":"2016/02/14 20:28"
            }
        }

        # connected to a charging station
        {
          "status": 200,
          "message": "success",
          "BatteryStatusRecords": {
            "OperationResult": "START",
            "OperationDateAndTime": "Feb 19, 2016 12:12 PM",
            "BatteryStatus": {
              "BatteryChargingStatus": "NORMAL_CHARGING",
              "BatteryCapacity": "12",
              "BatteryRemainingAmount": "12",
              "BatteryRemainingAmountWH": "",
              "BatteryRemainingAmountkWH": ""
            },
            "PluginState": "CONNECTED",
            "CruisingRangeAcOn": "132000.0",
            "CruisingRangeAcOff": "134000.0",
            "TimeRequiredToFull200_6kW": {
              "HourRequiredToFull": "0",
              "MinutesRequiredToFull": "40"
            },
            "NotificationDateAndTime": "2016/02/19 17:12",
            "TargetDate": "2016/02/19 17:12"
          }
        }
    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status["BatteryStatusRecords"])
        self.answer = status

        recs = status["BatteryStatusRecords"]

        bs = recs["BatteryStatus"]
        self.battery_capacity = bs["BatteryCapacity"]
        self.battery_remaining_amount = bs["BatteryRemainingAmount"]
        self.charging_status = bs["BatteryChargingStatus"]
        self.is_charging = ("NOT_CHARGING" != bs["BatteryChargingStatus"])    # double negatives are fun
        self.is_quick_charging = ("RAPIDLY_CHARGING" == bs["BatteryChargingStatus"])

        self.plugin_state = recs["PluginState"]
        self.is_connected = ("NOT_CONNECTED" != recs["PluginState"])          # another double negative
        self.is_connected_to_quick_charger = ("QC_CONNECTED" == recs["PluginState"])

        self._set_cruising_ranges(recs, off_key="CruisingRangeAcOff", on_key="CruisingRangeAcOn")

        if "TimeRequiredToFull" in recs:
            self.time_to_full_trickle = timedelta(minutes=_time_remaining(recs["TimeRequiredToFull"]))
        else:
            self.time_to_full_trickle = None

        if "TimeRequiredToFull200" in recs:
            self.time_to_full_l2 = timedelta(minutes=_time_remaining(recs["TimeRequiredToFull200"]))
        else:
            self.time_to_full_l2 = None

        if "TimeRequiredToFull200_6kW" in recs:
            self.time_to_full_l2_6kw = timedelta(minutes=_time_remaining(recs["TimeRequiredToFull200_6kW"]))
        else:
            self.time_to_full_l2_6kw = None

        if float(self.battery_capacity) == 0:
            log.debug("battery_capacity=0, status=%s", status)
            self.battery_percent = 0
        else:
            self.battery_percent = 100 * float(self.battery_remaining_amount) / 12

        # Leaf 2016 has SOC (State Of Charge) in BatteryStatus, a more accurate battery_percentage
        if "SOC" in bs:
            self.state_of_charge = bs["SOC"]["Value"]
            # Update battery_percent with more accurate version
            self.battery_percent = float(self.state_of_charge)
        else:
            self.state_of_charge = None


class CarwingsElectricRateSimulationResponse(CarwingsResponse):
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        r = status["PriceSimulatorDetailInfoResponsePersonalData"]
        t = r["PriceSimulatorTotalInfo"]

        self.month = r["DisplayMonth"]     # e.g. "Feb/2016"

        self.total_number_of_trips = t["TotalNumberOfTrips"]
        self.total_power_consumption = t["TotalPowerConsumptTotal"]                # in kWh
        self.total_acceleration_power_consumption = t["TotalPowerConsumptMoter"]   # in kWh
        self.total_power_regenerated_in_braking = t["TotalPowerConsumptMinus"]     # in kWh
        self.total_travel_distance_km = float(t["TotalTravelDistance"]) / 1000     # assumed to be in meters

        self.total_electric_mileage = t["TotalElectricMileage"]
        self.total_co2_reduction = t["TotalCO2Reductiont"]   # (yep, extra 't' at the end)

        self.electricity_rate = r["ElectricPrice"]
        self.electric_bill = r["ElectricBill"]
        self.electric_cost_scale = r["ElectricCostScale"]    # e.g. "miles/kWh"


class CarwingsMyCarFinderResponse(CarwingsResponse):
    """
        {
            "Location": {
                "Country": "",
                "Home": "OUTSIDE",
                "LatitudeDeg": "69",
                "LatitudeMin": "41",
                "LatitudeMode": "NORTH",
                "LatitudeSec": "5540",
                "LocationType": "WGS84",
                "LongitudeDeg": "18",
                "LongitudeMin": "38",
                "LongitudeMode": "EAST",
                "LongitudeSec": "2506",
                "Position": "UNAVAILABLE"
            },
            "TargetDate": "2017/11/29 20:02",
            "lat": "69.698722222222",
            "lng": "18.640294444444",
            "receivedDate": "2017/11/29 20:02",
            "responseFlag": "1",
            "resultCode": "1",
            "status": 200,
            "timeStamp": "2017-11-29 20:02:45"
        }
    """
    def __init__(self, status):
        CarwingsResponse.__init__(self, status)

        self.latitude = status["lat"]
        self.longitude = status["lng"]
