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

"""
When logging in, you must specify a geographic 'region' parameter. The only
known values for this are as follows:

    NNA  : USA
    NE   : Europe
    NCI  : Canada
    NMA  : Australia
    NML  : Japan

Information about Nissan on the web (e.g. http://nissannews.com/en-US/nissan/usa/pages/executive-bios)
suggests others (this page suggests NMEX for Mexico, NLAC for Latin America) but
these have not been confirmed.

There are three asynchronous operations in this API, paired with three follow-up
"status check" methods.

    request_update           -> get_status_from_update
    start_climate_control    -> get_start_climate_control_result
    stop_climate_control     -> get_stop_climate_control_result

The asynchronous operations immediately return a 'result key', which
is then supplied as a parameter for the corresponding status check method.

Here's an example response from an asynchronous operation, showing the result key:

    {
        "status":200,
        "userId":"user@domain.com",
        "vin":"1ABCDEFG2HIJKLM3N",
        "resultKey":"12345678901234567890123456789012345678901234567890"
    }

The status check methods return a JSON blob containing a 'responseFlag' property.
If the communications are complete, the response flag value will be the string "1";
otherwise the value will be the string "0". You just gotta poll until you get a
"1" back. Note that the official app seems to poll every 20 seconds.

Example 'no response yet' result from a status check invocation:

    {
        "status":200,
        "responseFlag":"0"
    }

When the responseFlag does come back as "1", there will also be an "operationResult"
property. If there was an error communicating with the vehicle, it seems that
this field will contain the value "ELECTRIC_WAVE_ABNORMAL". Odd.

"""

import requests
from requests import Request, RequestException
import json
import logging
from datetime import date
from responses import *
import base64
from Crypto.Cipher import Blowfish

BASE_URL = "https://gdcportalgw.its-mo.com/api_v210707_NE/gdc/"

log = logging.getLogger(__name__)


# from http://stackoverflow.com/questions/17134100/python-blowfish-encryption
def _PKCS5Padding(string):
    byteNum = len(string)
    packingLength = 8 - byteNum % 8
    appendage = chr(packingLength) * packingLength
    return string + appendage


class CarwingsError(Exception):
    pass


class Session(object):
    """Maintains a connection to CARWINGS, refreshing it when needed"""

    def __init__(self, username, password, region="NNA"):
        self.username = username
        self.password = password
        self.region_code = region
        self.logged_in = False
        self.custom_sessionid = None

    def _request_with_retry(self, endpoint, params):
        ret = self._request(endpoint, params)

        if ("status" in ret) and (ret["status"] >= 400):
            log.error(
                "carwings error; logging in and trying request again: %s" % ret)
            # try logging in again
            self.connect()
            ret = self._request(endpoint, params)

        return ret

    def _request(self, endpoint, params):
        params["initial_app_str"] = "9s5rfKVuMrT03RtzajWNcA"
        if self.custom_sessionid:
            params["custom_sessionid"] = self.custom_sessionid
        else:
            params["custom_sessionid"] = ""

        req = Request('POST', url=BASE_URL + endpoint, data=params).prepare()

        log.debug("invoking carwings API: %s" % req.url)
        log.debug("params: %s" % json.dumps(
            {k: v.decode('utf-8') if isinstance(v, bytes)
             else v for k, v in params.items()},
            sort_keys=True, indent=3, separators=(',', ': '))
        )

        try:
            sess = requests.Session()
            response = sess.send(req)
            log.debug('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            log.debug('Response HTTP Response Body: {content}'.format(
                content=response.content))
        except RequestException:
            log.warning('HTTP Request failed')
            raise CarwingsError

        # Nissan servers can return html instead of jSOn on occassion, e.g.
        #
        # <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//END>
        # <html<head>
        #    <title>503 Service Temporarily Unavailable</title>
        # </head><body>
        # <h1>Service Temporarily Unavailable>
        # <p>The server is temporarily unable to service your
        # request due to maintenance downtime or capacity
        # problems. Please try again later.</p>
        # </body></html>
        try:
            j = json.loads(response.text)
        except ValueError:
            log.error("Invalid JSON returned")
            raise CarwingsError

        if "message" in j and j["message"] == "INVALID PARAMS":
            log.error("carwings error %s: %s" % (j["message"], j["status"]))
            raise CarwingsError("INVALID PARAMS")
        if "ErrorMessage" in j:
            log.error("carwings error %s: %s" %
                      (j["ErrorCode"], j["ErrorMessage"]))
            raise CarwingsError

        return j

    def connect(self):
        self.custom_sessionid = None
        self.logged_in = False

        response = self._request("InitialApp_v2.php", {
            "RegionCode": self.region_code,
            "lg": "en-US",
        })
        ret = CarwingsInitialAppResponse(response)

        c1 = Blowfish.new(ret.baseprm.encode(), Blowfish.MODE_ECB)
        packedPassword = _PKCS5Padding(self.password)
        encryptedPassword = c1.encrypt(packedPassword.encode())
        encodedPassword = base64.standard_b64encode(encryptedPassword)

        response = self._request("UserLoginRequest.php", {
            "RegionCode": self.region_code,
            "UserId": self.username,
            "Password": encodedPassword,
        })

        ret = CarwingsLoginResponse(response)

        self.custom_sessionid = ret.custom_sessionid

        self.gdc_user_id = ret.gdc_user_id
        log.debug("gdc_user_id: %s" % self.gdc_user_id)
        self.dcm_id = ret.dcm_id
        log.debug("dcm_id: %s" % self.dcm_id)
        self.tz = ret.tz
        log.debug("tz: %s" % self.tz)
        self.language = ret.language
        log.debug("language: %s" % self.language)
        log.debug("vin: %s" % ret.vin)
        log.debug("nickname: %s" % ret.nickname)

        self.leaf = Leaf(self, ret.leafs[0])

        self.logged_in = True

        return ret

    def get_leaf(self, index=0):
        if not self.logged_in:
            self.connect()

        return self.leaf


class Leaf:
    def __init__(self, session, params):
        self.session = session
        self.vin = params["vin"]
        self.nickname = params["nickname"]
        self.bound_time = params["bound_time"]
        log.debug("created leaf %s/%s" % (self.vin, self.nickname))

    def request_update(self):
        response = self.session._request_with_retry("BatteryStatusCheckRequest.php", {
            "RegionCode": self.session.region_code,
            "VIN": self.vin,
        })
        return response["resultKey"]

    def get_status_from_update(self, result_key):
        response = self.session._request_with_retry("BatteryStatusCheckResultRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "resultKey": result_key,
        })
        # responseFlag will be "1" if a response has been returned; "0" otherwise
        if response["responseFlag"] == "1":
            return CarwingsBatteryStatusResponse(response)

        return None

    def start_climate_control(self):
        response = self.session._request_with_retry("ACRemoteRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
        })
        return response["resultKey"]

    def get_start_climate_control_result(self, result_key):
        response = self.session._request_with_retry("ACRemoteResult.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "UserId": self.session.gdc_user_id,     # this userid is the 'gdc' userid
            "resultKey": result_key,
        })
        if response["responseFlag"] == "1":
            return CarwingsStartClimateControlResponse(response)

        return None

    def stop_climate_control(self):
        response = self.session._request_with_retry("ACRemoteOffRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
        })
        return response["resultKey"]

    def get_stop_climate_control_result(self, result_key):
        response = self.session._request_with_retry("ACRemoteOffResult.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "UserId": self.session.gdc_user_id,     # this userid is the 'gdc' userid
            "resultKey": result_key,
        })
        if response["responseFlag"] == "1":
            return CarwingsStopClimateControlResponse(response)

        return None

    # execute time example: "2016-02-09 17:24"
    # I believe this time is specified in GMT, despite the "tz" parameter
    # TODO: change parameter to python datetime object(?)
    def schedule_climate_control(self, execute_time):
        response = self.session._request_with_retry("ACRemoteNewRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "ExecuteTime": execute_time,
        })
        return (response["status"] == 200)

    # execute time example: "2016-02-09 17:24"
    # I believe this time is specified in GMT, despite the "tz" parameter
    # TODO: change parameter to python datetime object(?)
    def update_scheduled_climate_control(self, execute_time):
        response = self.session._request_with_retry("ACRemoteUpdateRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "ExecuteTime": execute_time,
        })
        return (response["status"] == 200)

    def cancel_scheduled_climate_control(self):
        response = self.session._request_with_retry("ACRemoteCancelRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
        })
        return (response["status"] == 200)

    def get_climate_control_schedule(self):
        response = self.session._request_with_retry("GetScheduledACRemoteRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
        })
        if (response["status"] == 200):
            if response["ExecuteTime"] != "":
                return CarwingsClimateControlScheduleResponse(response)

        return None

    """
    {
        "status":200,
    }
    """

    def start_charging(self):
        response = self.session._request_with_retry("BatteryRemoteChargingRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "ExecuteTime": date.today().isoformat()
        })
        if response["status"] == 200:
            # This only indicates that the charging command has been received by the
            # Nissan servers, it does not indicate that the car is now charging.
            return True

        return False

    def get_driving_analysis(self):
        response = self.session._request_with_retry("DriveAnalysisBasicScreenRequestEx.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
        })
        if response["status"] == 200:
            return CarwingsDrivingAnalysisResponse(response)

        return None

    def get_latest_battery_status(self):
        response = self.session._request_with_retry("BatteryStatusRecordsRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "TimeFrom": self.bound_time
        })
        if response["status"] == 200:
            if "BatteryStatusRecords" in response:
                return CarwingsLatestBatteryStatusResponse(response)
            else:
                log.warning('no battery status record returned by server')

        return None

    def get_latest_hvac_status(self):
        response = self.session._request_with_retry("RemoteACRecordsRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "TimeFrom": self.bound_time
        })
        if response["status"] == 200:
            if "RemoteACRecords" in response:
                return CarwingsLatestClimateControlStatusResponse(response)
            else:
                log.warning('no remote a/c records returned by server')

        return None

    # target_month format: "YYYYMM" e.g. "201602"
    def get_electric_rate_simulation(self, target_month):
        response = self.session._request_with_retry("PriceSimulatorDetailInfoRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "TargetMonth": target_month
        })
        if response["status"] == 200:
            return CarwingsElectricRateSimulationResponse(response)

        return None

    def request_location(self):
        # As of 25th July the Locate My Vehicle functionality of the Europe version of the
        # Nissan APIs was removed.  It may return, so this call is left here.
        # It currently errors with a 404 MyCarFinderRequest.php was not found on this server
        # for European users.
        response = self.session._request_with_retry("MyCarFinderRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "UserId": self.session.gdc_user_id,     # this userid is the 'gdc' userid
        })
        return response["resultKey"]

    def get_status_from_location(self, result_key):
        response = self.session._request_with_retry("MyCarFinderResultRequest.php", {
            "RegionCode": self.session.region_code,
            "lg": self.session.language,
            "DCMID": self.session.dcm_id,
            "VIN": self.vin,
            "tz": self.session.tz,
            "resultKey": result_key,
        })
        if response["responseFlag"] == "1":
            return CarwingsMyCarFinderResponse(response)

        return None
