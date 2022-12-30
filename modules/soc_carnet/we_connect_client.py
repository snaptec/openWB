#!/usr/bin/python
# Script to emulate VW WE Connect web site login and commands to VW car.
# Author  : Rene Boer
# Version : 2.8
# Date    : 14 Dec 2019

# Should work on python 2 and 3

# Free for use & distribution
# V2.8 Surpress certificate warnings when not verrified and not in debug mode
# V2.7 Ignore certificate check on first Get to work a round an SSL error.
# V2.6 Check for SPIN command to be authorized. Do not send command if not.
# V2.5 The commands needing a SPIN are now working.
#      Added commands for getLatestReport, getAlerts, getGeofences
#      Fix for remoteUnlock
# V2.4 Fix on getting country code for CarNetCheckSecurityLevel
#      Added commands for remoteUnlock, startRemoteVentilation, stopRemoteVentilation, startRemoteHeating, stopRemoteHeating
# V2.3 Added command line parser and spin remoteLock
# V2.2 Added getCharge, getCharge, getWindowMelt status commands
# V2.1 added synonyms for startClimat and stopClimat commands (startClimate, stopClimate)
# V2.0 for new VW WE Connect portal thanks to youpixel - 2019-07-26
# Thanks to birgersp for a number of cleanups and rewrites. See https://github.com/birgersp/carnet-client

import argparse
import logging
import urllib3
import sys
import json
import requests
import re
debug = False
certverify = False

# import correct lib for python v3.x or fallback to v2.x
try:
    import urllib.parse as urlparse
except ImportError:
    # Python 2
    import urlparse

# ---- uncomment to enble http request debugging
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
# ---- end uncomment


portal_base_url = 'https://www.portal.volkswagen-we.com'

request_headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,nl;q=0.7,en;q=0.3',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}


def remove_newline_chars(string):
    return string.replace('\n', '').replace('\r', '')


def extract_csrf(string):
    # Get value from HTML head _csrf meta tag.
    try:
        csrf_re = re.compile('<meta name="_csrf" content="(.*?)"/>')
        resp = csrf_re.search(string).group(1)
    except:
        resp = ''
    return resp


def extract_login_hmac(string):
    # Get hmac value from html input form.
    try:
        regex = re.compile('<input.*?id="hmac".*?value="(.*?)"/>')
        resp = regex.search(string).group(1)
    except:
        resp = ''
    return resp


def extract_login_csrf(string):
    # Get csrf value from html input form.
    try:
        regex = re.compile('<input.*?id="csrf".*?value="(.*?)"/>')
        resp = regex.search(string).group(1)
    except:
        resp = ''
    return resp


def extract_url_parameter(url, cmnd):
    # Get parameter value from url.
    try:
        parsed = urlparse.urlparse(url)
        resp = urlparse.parse_qs(parsed.query)[cmnd][0]
    except:
        resp = ''
    return resp


def CarNetLogin(session, email, password):
    # Perform login steps of WE Connect web portal
    base_url = portal_base_url
    auth_base_url = 'https://identity.vwgroup.io'

    # Step 1
    if debug:
        print("Step 1 ===========")
    # Get initial CSRF from landing page to get login process started.
    # Python Session handles JSESSIONID cookie
    landing_page_url = base_url + '/portal/en_GB/web/guest/home'
    landing_page_response = session.get(landing_page_url, verify=certverify)
    if landing_page_response.status_code != 200:
        return '', 'Failed getting to portal landing page.'
    csrf = extract_csrf(landing_page_response.text)
    if csrf == '':
        return '', 'Failed to get CSRF from landing page.'
    if debug:
        print("_csrf from landing page : ", csrf)

    # Step 1a,1b
    # Note: Portal performs a get-supported-browsers and get-countries at this point. We assumed en_GB

    # Step 2
    if debug:
        print("Step 2 ===========")
    # Get login page url. POST returns JSON with loginURL for next step.
    # returned loginURL includes client_id for step 4
    auth_request_headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,nl;q=0.7,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml,application/json;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    auth_request_headers['Referer'] = landing_page_url
    auth_request_headers['X-CSRF-Token'] = csrf
    get_login_url = base_url + '/portal/en_GB/web/guest/home/-/csrftokenhandling/get-login-url'
    login_page_response = session.post(get_login_url, headers=auth_request_headers, verify=certverify)
    if login_page_response.status_code != 200:
        return '', 'Failed to get login url.'
    login_url = json.loads(login_page_response.text).get('loginURL').get('path')
    client_id = extract_url_parameter(login_url, 'client_id')
    if debug:
        print("client_id found: ", client_id)
    if client_id == '':
        return '', 'Failed to get client_id.'

    # Step 3
    if debug:
        print("Step 3 ===========")
    # Get login form url we are told to use, it will give us a new location.
    # response header location (redirect URL) includes relayState for step 5
    # https://identity.vwgroup.io/oidc/v1/authorize......
    login_url_response = session.get(login_url, allow_redirects=False, headers=auth_request_headers, verify=certverify)
    if login_url_response.status_code != 302:
        return '', 'Failed to get authorization page.'
    login_form_url = login_url_response.headers.get('location')
    login_relay_state_token = extract_url_parameter(login_form_url, 'relayState')
    if debug:
        print("relayState found: ", login_relay_state_token)
    if login_relay_state_token == '':
        return '', 'Failed to get relay State.'

    # Step 4
    if debug:
        print("Step 4 ===========")
    # Get login action url, relay state. hmac token 1 and login CSRF from form contents
    # https://identity.vwgroup.io/signin-service/v1/signin/<client_id>@relayState=<relay_state>
    login_form_location_response = session.get(login_form_url, headers=auth_request_headers, verify=certverify)
    if login_form_location_response.status_code != 200:
        return '', 'Failed to get sign-in page.'
    # We get a SESSION set-cookie here!
    # Get hmac and csrf tokens from form content.
    login_form_location_response_data = remove_newline_chars(login_form_location_response.text)
    hmac_token1 = extract_login_hmac(login_form_location_response_data)
    login_csrf = extract_login_csrf(login_form_location_response_data)
    if debug:
        print("login_csrf found: ", login_csrf)
    if debug:
        print("hmac_token1 found: ", hmac_token1)
    if login_csrf == '':
        return '', 'Failed to get login CSRF.'
    if hmac_token1 == '':
        return '', 'Failed to get 1st HMAC token.'

    # Step 5
    if debug:
        print("Step 5 ===========")
    # Post initial login data
    # https://identity.vwgroup.io/signin-service/v1/<client_id>/login/identifier
    del auth_request_headers['X-CSRF-Token']
    auth_request_headers['Referer'] = login_form_url
    auth_request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    post_data = {
        'email': email,
        'relayState': login_relay_state_token,
        'hmac': hmac_token1,
        '_csrf': login_csrf,
    }
    login_action_url = auth_base_url + '/signin-service/v1/' + client_id + '/login/identifier'
    login_action_url_response = session.post(login_action_url, data=post_data,
                                             headers=auth_request_headers, allow_redirects=True, verify=certverify)
    # performs a 303 redirect to https://identity.vwgroup.io/signin-service/v1/<client_id>/login/authenticate?relayState=<relayState>&email=<email>
    # redirected GET returns form used below.
    if login_action_url_response.status_code != 200:
        return '', 'Failed to get login/identiefer page.'
    # Get 2nd hmac token from form content.
    login_action_url_response_data = remove_newline_chars(login_action_url_response.text)
    hmac_token2 = extract_login_hmac(login_action_url_response_data)
    if debug:
        print("hmac_token2 found: ", hmac_token2)
    if hmac_token2 == '':
        return '', 'Failed to get 2nd HMAC token.'

    # Step 6
    if debug:
        print("Step 6 ===========")
    # Post login data to "login action 2" url
    # https://identity.vwgroup.io/signin-service/v1/<client_id>/login/authenticate
    auth_request_headers['Referer'] = login_action_url
    auth_request_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    login_data = {
        'email': email,
        'password': password,
        'relayState': login_relay_state_token,
        'hmac': hmac_token2,
        '_csrf': login_csrf,
        'login': 'true'
    }
    login_action2_url = auth_base_url + '/signin-service/v1/' + client_id + '/login/authenticate'
    login_post_response = session.post(login_action2_url, data=login_data,
                                       headers=auth_request_headers, allow_redirects=True, verify=certverify)
    # performs a 302 redirect to GET https://identity.vwgroup.io/oidc/v1/oauth/sso?clientId=<client_id>&relayState=<relay_state>&userId=<userID>&HMAC=<...>"
    # then a 302 redirect to GET https://identity.vwgroup.io/consent/v1/users/<userID>/<client_id>?scopes=openid%20profile%20birthdate%20nickname%20address%20email%20phone%20cars%20dealers%20mbb&relay_state=1bc582f3ff177afde55b590af92e17a006f9c532&callback=https://identity.vwgroup.io/oidc/v1/oauth/client/callback&hmac=<.....>
    # then a 302 redirect to https://identity.vwgroup.io/oidc/v1/oauth/client/callback/success?user_id=<userID>&client_id=<client_id>&scopes=openid%20profile%20birthdate%20nickname%20address%20email%20phone%20cars%20dealers%20mbb&consentedScopes=openid%20profile%20birthdate%20nickname%20address%20email%20phone%20cars%20dealers%20mbb&relay_state=<relayState>&hmac=<...>
    # then a 302 redirect to https://www.portal.volkswagen-we.com/portal/web/guest/complete-login?state=<csrf>&code=<....>
    if login_post_response.status_code != 200:
        return '', 'Failed to process login sequence.'
    # ref2_url = login_post_response.headers.get('location') # there is no location attribute, but does not seem to matter much.
    ref2_url = login_post_response.url
    portlet_code = extract_url_parameter(ref2_url, 'code')
    state = extract_url_parameter(ref2_url, 'state')
    if debug:
        print("state found: ", state)
    if portlet_code == '':
        return '', 'Failed to get portlet code.'
    if state == '':
        return '', 'Failed to get state.'

    # Step 7
    if debug:
        print("Step 7 ===========")
    # Site first does a POST https://www.portal.volkswagen-we.com/portal/web/guest/complete-login/-/mainnavigation/get-countries
    # Post login data to complete login url
    # https://www.portal.volkswagen-we.com/portal/web/guest/complete-login?p_auth=<state>&p_p_id=33_WAR_cored5portlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_33_WAR_cored5portlet_javax.portlet.action=getLoginStatus
    auth_request_headers['Referer'] = ref2_url
    portlet_data = {'_33_WAR_cored5portlet_code': portlet_code}
    final_login_url = base_url + '/portal/web/guest/complete-login?p_auth=' + state + \
        '&p_p_id=33_WAR_cored5portlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_33_WAR_cored5portlet_javax.portlet.action=getLoginStatus'
    complete_login_response = session.post(final_login_url, data=portlet_data,
                                           allow_redirects=False, headers=auth_request_headers, verify=certverify)
    if complete_login_response.status_code != 302:
        return '', 'Failed to post portlet page.'

    # Step 8
    if debug:
        print("Step 8 ===========")
    # Get base JSON url for commands
    base_json_url = complete_login_response.headers.get('location')
    base_json_response = session.get(base_json_url, headers=auth_request_headers, verify=certverify)
    csrf = extract_csrf(base_json_response.text)
    if base_json_url == '':
        return '', 'Failed to base json url.'
    if csrf == '':
        return '', 'Failed to get final CSRF.'
    request_headers['Referer'] = base_json_url
    request_headers['X-CSRF-Token'] = csrf
    if debug:
        print('login csrf token: ', csrf)
    if debug:
        print('login base json url: ', base_json_url)
    print('=== login complete ===')
    return base_json_url, 'OK'


def CarNetPost(session, url_base, command):
    print(command)
    r = session.post(url_base + command, headers=request_headers, verify=certverify)
    return r.text


def CarNetPostAction(session, url_base, command, data):
    print(command)
    r = session.post(url_base + command, json=data, headers=request_headers, verify=certverify)
    return r.text


def CarNetCheckSecurityLevel(session, url_base, data):
    print('Check security level for: ' + data.get('operationId'))
    cc = session.cookies['GUEST_LANGUAGE_ID']
    if cc:
        if (len(cc) == 5):
            cc = cc[3:5]
            cc = cc.lower()
        else:
            cc = cc[0:2]
    else:
        cc = 'en'
    url = portal_base_url + '/portal/group/' + cc + '/edit-profile/-/profile/check-security-level'
    response = session.post(url, json=data, headers=request_headers, verify=certverify)
    if response.status_code != 200:
        return False, 'Check security failed, HTTP response ' + response.status_code
    json_data = response.json()
    errCd = json_data['errorCode']
    if errCd == "0":
        return True, 'You are authorized for PIN action'
    if errCd == "1" or errCd == "2":
        return False, 'You are not authorized for PIN action'
    return False, 'Check security failed'


def retrieveCarNetInfo(session, url_base):

    # Get details on all cars on account.
    response = CarNetPost(session, url_base, '/-/mainnavigation/get-fully-loaded-cars')
    print(response)
    # Resp ex: {"errorCode":"0","fullyLoadedVehiclesResponse":{"completeVehicles":[],"vehiclesNotFullyLoaded":[{"vin":"WVWZZZAUZGWxxxxxx","name":"GTE Dhr Boer","expired":false,"model":null,"modelCode":null,"modelYear":null,"imageUrl":null,"vehicleSpecificFallbackImageUrl":null,"modelSpecificFallbackImageUrl":null,"defaultImageUrl":"/portal/delegate/vehicle-image/WVWZZZAUZGWxxxxx","vehicleBrand":"v","enrollmentDate":"20160923","deviceOCU1":null,"deviceOCU2":null,"deviceMIB":null,"engineTypeCombustian":false,"engineTypeHybridOCU1":true,"engineTypeHybridOCU2":false,"engineTypeElectric":false,"engineTypeCNG":false,"engineTypeDefault":false,"stpStatus":"UNAVAILABLE","windowstateSupported":true,"dashboardUrl":"/portal/user/55e2ea85-2a5c-46c4-bb0b-f0cde8bcf22e/v_c5rlgqwltznnz_l-k7dfv5l1vxyuyxuz","vhrRequested":false,"vsrRequested":false,"vhrConfigAvailable":false,"verifiedByDealer":false,"vhr2":false,"roleEnabled":true,"isEL2Vehicle":true,"workshopMode":false,"hiddenUserProfiles":false,"mobileKeyActivated":null,"enrollmentType":"MILEAGE","ocu3Low":false,"packageServices":[{"packageServiceId":"NET.500.010.F","propertyKeyReference":"NET.500.010.1","packageServiceName":"e-Remote","trackingName":"e-Remote","activationDate":"03-11-2015","expirationDate":"03-11-2020","expired":false,"expireInAMonth":false,"packageType":"er","enrollmentPackageType":"er"}],"defaultCar":true,"vwConnectPowerLayerAvailable":false,"xprofileId":"c5rlgqwltznnz_l-k7dfv5l1vxyuyxuz","smartCardKeyActivated":null,"fullyEnrolled":true,"secondaryUser":false,"fleet":false,"touareg":false,"iceSupported":false,"flightMode":false,"esimCompatible":false,"dkyenabled":false,"selected":true}],"status":"VALID","currentVehicleValid":true}}
    vin = json.loads(response).get('fullyLoadedVehiclesResponse').get('vehiclesNotFullyLoaded')[0].get('vin')
    print('found vin: ', vin)

    # Check on invitations of some kind.
    print(CarNetPost(session, url_base, '/-/mainnavigation/check-unanswered-invitations'))
    # Resp ex: {"checkUnansweredInvitationsResponse":{"hasUnansweredInvitations":false},"errorCode":"0"}

    # Set the correct time zone.
    post_data = {
        "timeZoneId": "Europe/Amsterdam"
    }
    # print(CarNetPostAction(session, url_base, '/-/mainnavigation/set-time-zone', post_data))
    # Resp ex: {"errorCode":"0"}

    # Get the car last reported location
    print(CarNetPost(session, url_base, '/-/cf/get-location'))
    # Resp ex: {"errorCode":"0","position":{"lat":52.xxxx,"lng":4.xxxx}}

    # get shutdown (no idea)
    # print(CarNetPost(session, url_base, '-/mainnavigation/get-shutdown'))
    # Resp ex: {"getShutdownResponse":{"enabled":false,"finalEnabled":false,"finalDate":null,"portalRedirect":null,"iosRedirect":null,"androidRedirect":null,"hideShutdownPromotion":false},"errorCode":"0"}

    # Get the latest messages from the car. Includes oil change etc.
    print(CarNetPost(session, url_base, '/-/msgc/get-latest-messages'))
    # Resp ex: {"messageList":[],"errorCode":"0"}

    # Get some stuff if you have apple
    # print(CarNetPost(session, url_base, '/-/service-container/get-apple-music-status'))
    # Resp ex: {"errorCode":"0","appleMusicStatusResponse":{"showAppleMusic":false,"appleMenu":null}}

    # Get the web site navigation config.
    print(CarNetPost(session, url_base, '/-/mainnavigation/get-config'))
    # Resp ex: {"errorCode":"0","userConfiguration":{"hidePackageExpired":false,"hideOnboardingGuide":true,"hideVWConnectPromotion":false,"hideCubicShopHint":"SHOW_CUBIC_SHOP_LAYER","hideRebranding":true,"hideShutdownPromotion":false}}

    # Get car details of specific car based on VIN
    print(CarNetPost(session, url_base, '/-/mainnavigation/load-car-details/' + vin))  # VIN
    # Resp ex: {"errorCode":"0","completeVehicleJson":{"vin":"WVWZZZAUZGWxxxx","name":"GTE Dhr Boer","expired":false,"model":"Golf","modelCode":"5G16YY","modelYear":"2016","imageUrl":null,"vehicleSpecificFallbackImageUrl":null,"modelSpecificFallbackImageUrl":null,"defaultImageUrl":"/portal/delegate/vehicle-image/WVWZZZAUZGWxxxxx","vehicleBrand":"v","enrollmentDate":"20160923","deviceOCU1":true,"deviceOCU2":false,"deviceMIB":false,"engineTypeCombustian":false,"engineTypeHybridOCU1":true,"engineTypeHybridOCU2":false,"engineTypeElectric":false,"engineTypeCNG":false,"engineTypeDefault":false,"stpStatus":"UNAVAILABLE","windowstateSupported":true,"dashboardUrl":"/portal/user/55e2ea85-2a5c-46c4-bb0b-f0cde8bcf22e/v_c5rlgqwltznnz_l-k7dfv5l1vxyuyxuz","vhrRequested":false,"vsrRequested":false,"vhrConfigAvailable":false,"verifiedByDealer":false,"vhr2":false,"roleEnabled":true,"isEL2Vehicle":true,"workshopMode":false,"hiddenUserProfiles":false,"mobileKeyActivated":null,"enrollmentType":"MILEAGE","ocu3Low":false,"packageServices":[{"packageServiceId":"NET.500.010.F","propertyKeyReference":"NET.500.010.1","packageServiceName":"e-Remote","trackingName":"e-Remote","activationDate":"03-11-2015","expirationDate":"03-11-2020","expired":false,"expireInAMonth":false,"packageType":"er","enrollmentPackageType":"er"}],"defaultCar":true,"vwConnectPowerLayerAvailable":false,"xprofileId":"c5rlgqwltznnz_l-k7dfv5l1vxyuyxuz","smartCardKeyActivated":null,"fullyEnrolled":true,"secondaryUser":false,"fleet":false,"touareg":false,"iceSupported":false,"flightMode":false,"esimCompatible":false,"dkyenabled":false,"selected":true}}

    # get psp status (no idea what it is)
    # print(CarNetPost(session, url_base, '/-/mainnavigation/get-psp-status'))
    # Resp ex: {"errorCode":"0","pspStatusResponse":{"reminderStatus":false,"deleteStatus":false}}

    # Get vehicle maintenance data
    print(CarNetPost(session, url_base, '/-/vehicle-info/get-vehicle-details'))
    # Resp ex: {"vehicleDetails":{"lastConnectionTimeStamp":["10-08-2019","05:39"],"distanceCovered":"64.803","range":"41","serviceInspectionData":"225 Dag(en) / 25.400 km","oilInspectionData":"","showOil":false,"showService":true,"flightMode":false},"errorCode":"0"}

    # Get Hybrid/Full electric charging details
    print(CarNetPost(session, url_base, '/-/emanager/get-emanager'))
    # Resp ex: {"errorCode":"0".... long response with all charning related details}

    # get last trip stats
    print(CarNetPost(session, url_base, '/-/rts/get-latest-trip-statistics'))
    # Resp ex: {"errorCode":"0".... long response with all trip data of last weeks}

    # Get vehicle status
    print(CarNetPost(session, url_base, '/-/vsr/get-vsr'))
    # Resp ex: {"errorCode":"0","vehicleStatusData":{"windowStatusSupported":true,"carRenderData":{"parkingLights":2,"hood":3,"doors":{"left_front":3,"right_front":3,"left_back":3,"right_back":3,"trunk":3,"number_of_doors":4},"windows":{"left_front":3,"right_front":3,"left_back":3,"right_back":3},"sunroof":3},"lockData":{"left_front":2,"right_front":2,"left_back":2,"right_back":2,"trunk":2},"headerData":null,"requestStatus":null,"lockDisabled":false,"unlockDisabled":false,"rluDisabled":true,"hideCngFuelLevel":false,"totalRange":41,"primaryEngineRange":41,"fuelRange":null,"cngRange":null,"batteryRange":41,"fuelLevel":null,"cngFuelLevel":null,"batteryLevel":100,"sliceRootPath":"https://www.portal.volkswagen-we.com/static/slices/phev_golf/phev_golf"}}

    # Get dealer info. (getting errorCode 2, not sure why)
    post_data = {
        'vehicleBrand': 'v'
    }
    # print(CarNetPostAction(session, url_base, '/-/mainnavigation/get-preferred-dealer', post_data))
    # Resp ex: {"errorCode":"0","preferredDealerResponse":{"dealer":{"id":"00842","name":"Autobedrijf J. Maas Woerden B.V.","address":" Botnische Golf 22 WOERDEN 3446 CN","addressParts":{"houseNumber":"","streetPrefix":"","street":"Botnische Golf 22","state":"","city":"WOERDEN","postalCode":"3446 CN"},"position":{"lat":52.0733438,"lng":4.9031345},"brand":"V","phoneNumber":"088-0207600","services":["SERVICE"],"openingHours":[]},"dssAvailable":true,"stwAvailableForMarketAndBrand":false,"stwAvailableForPsp":false,"appointmentSchedulingSupported":false}}

    # Poll for new information as log as desired.
    print(CarNetPost(session, url_base, '/-/msgc/get-new-messages'))
    # Resp ex: {"messageList":[],"errorCode":"0"}

    # Obsolete request: print(CarNetPost(session, url_base, '/-/vsr/request-vsr'))
    return 0


def startCharge(session, url_base):
    post_data = {
        'triggerAction': True,
        'batteryPercent': '100'
    }
    print(CarNetPostAction(session, url_base, '/-/emanager/charge-battery', post_data))
    return 0


def stopCharge(session, url_base):
    post_data = {
        'triggerAction': False,
        'batteryPercent': '99'
    }
    print(CarNetPostAction(session, url_base, '/-/emanager/charge-battery', post_data))
    return 0


def getCharge(session, url_base):
    try:
        estat = json.loads(CarNetPost(session, url_base, '/-/emanager/get-emanager'))
        print('{"errorCode":"0","chargingState":"' + estat.get('EManager').get('rbc').get('status').get('chargingState') + '"}')
    except:
        print('{"errorCode":"2","errorMsg":"Failed to get currect charging state"}')
    return 0


def startClimat(session, url_base):
    post_data = {
        'triggerAction': True,
        'electricClima': True
    }
    print(CarNetPostAction(session, url_base, '/-/emanager/trigger-climatisation', post_data))
    return 0


def stopClimat(session, url_base):
    post_data = {
        'triggerAction': False,
        'electricClima': True
    }
    print(CarNetPostAction(session, url_base, '/-/emanager/trigger-climatisation', post_data))
    return 0


def getClimat(session, url_base):
    try:
        estat = json.loads(CarNetPost(session, url_base, '/-/emanager/get-emanager'))
        print('{"errorCode":"0","climatisationState":"' +
              estat.get('EManager').get('rpc').get('status').get('climatisationState') + '"}')
    except:
        print('{"errorCode":"2","errorMsg":"Failed to get current climate state"}')
    return 0


def getVIN(session, url_base, index):
    try:
        estat = json.loads(CarNetPost(session, url_base, '/-/mainnavigation/get-fully-loaded-cars'))
        resp = {
            'errorCode': '0',
            'vin': estat.get('fullyLoadedVehiclesResponse').get('vehiclesNotFullyLoaded')[index].get('vin')
        }
    except:
        resp = {
            'errorCode': '2',
            'errorMsg': 'Failed to get VIN for index ' + index
        }
    return resp


def startWindowMelt(session, url_base):
    post_data = {
        'triggerAction': True
    }
    print(CarNetPostAction(session, url_base, '/-/emanager/trigger-windowheating', post_data))
    return 0


def stopWindowMelt(session, url_base):
    post_data = {
        'triggerAction': False
    }
    print(CarNetPostAction(session, url_base, '/-/emanager/trigger-windowheating', post_data))
    return 0


def getWindowMelt(session, url_base):
    try:
        estat = json.loads(CarNetPost(session, url_base, '/-/emanager/get-emanager'))
        status = estat.get('EManager').get('rpc').get('status')
        print('{"errorCode":"0","windowHeatingStateFront":"' + status.get('windowHeatingStateFront') +
              '","windowHeatingStateRear":"' + status.get('windowHeatingStateRear') + '"}')
    except:
        print('{"errorCode":"2","errorMsg":"Failed to get currect windows melt state"}')
    return 0


def remoteLock(session, url_base, spin, vin):
    post_data = {
        'vin': vin,
        'operationId': 'LOCK',
        'serviceId': 'rlu_v1'}
    res, msg = CarNetCheckSecurityLevel(session, url_base, post_data)
    if res:
        post_data = {
            'spin': str(spin)}
        print(CarNetPostAction(session, url_base, '/-/vsr/remote-lock', post_data))
    else:
        print(msg)
    return 0


def remoteUnlock(session, url_base, spin, vin):
    post_data = {
        'vin': vin,
        'operationId': 'UNLOCK',
        'serviceId': 'rlu_v1'}
    res, msg = CarNetCheckSecurityLevel(session, url_base, post_data)

    if res:
        post_data = {
            'spin': str(spin)}
        print(CarNetPostAction(session, url_base, '/-/vsr/remote-unlock', post_data))
    else:
        print(msg)
    return 0


def startRemoteAccessVentilation(session, url_base, spin, vin):
    post_data = {
        'vin': vin,
        'operationId': 'P_QSACT',
        'serviceId': 'rheating_v1'}
    res, msg = CarNetCheckSecurityLevel(session, url_base, post_data)

    if res:
        post_data = {
            'startMode': 'VENTILATION',
            'spin': str(spin)}
        print(CarNetPostAction(session, url_base, '/-/rah/quick-start', post_data))
    else:
        print(msg)
    return 0


def stopRemoteAccessVentilation(session, url_base):
    print(CarNetPost(session, url_base, '/-/rah/quick-stop'))
    return 0


def startRemoteAccessHeating(session, url_base, spin, vin):
    post_data = {
        'vin': vin,
        'operationId': 'P_QSACT',
        'serviceId': 'rheating_v1'}
    res, msg = CarNetCheckSecurityLevel(session, url_base, post_data)

    if res:
        post_data = {
            'startMode': 'HEATING',
            'spin': str(spin)}
        print(CarNetPostAction(session, url_base, '/-/rah/quick-start', post_data))
    else:
        print(msg)
    return 0


def stopRemoteAccessHeating(session, url_base):
    print(CarNetPost(session, url_base, '/-/rah/quick-stop'))
    return 0


def getRemoteAccessHeating(session, url_base):
    print(CarNetPost(session, url_base, '/-/rah/get-status'))
    return 0


def getLatestReport(session, url_base):
    print(CarNetPost(session, url_base, '/-/vhr/get-latest-report'))
    return 0


def getAlerts(session, url_base):
    print(CarNetPost(session, url_base, '/-/rsa/get-alerts'))
    return 0


def getGeofences(session, url_base):
    print(CarNetPost(session, url_base, '/-/geofence/get-fences'))
    return 0


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description='Control your Connected VW.')
    parser.add_argument('-u', '--user', required=True, help='Your WE-Connect user id.')
    parser.add_argument('-p', '--password', required=True, help='Your WE-Connect password.')
    parser.add_argument('-v', '--vin', help='Your car VIN if more cars on account.')
    parser.add_argument('-c', '--command', choices=['startCharge', 'stopCharge', 'getCharge', 'startClimate', 'stopClimate', 'getClimate', 'startWindowMelt', 'stopWindowMelt', 'getWindowMelt', 'getVIN', 'remoteLock',
                        'remoteUnlock', 'startRemoteVentilation', 'stopRemoteVentilation', 'startRemoteHeating', 'stopRemoteHeating', 'getRemoteHeating', 'getLatestReport', 'getAlerts', 'getGeofences'], help='Command to send.')
    parser.add_argument('-s', '--spin', help='Your WE-Connect s-pin needed for some commands.')
    parser.add_argument('-i', '--index', type=int, default=0, choices=range(0, 10),
                        help='To get the VIN for the N-th car.')
    parser.add_argument('-d', '--debug', action="store_true", help='Show debug commands.')
    args = parser.parse_args()
    CARNET_USERNAME = args.user
    CARNET_PASSWORD = args.password
    CARNET_COMMAND = ''
    CARNET_VIN = args.vin
    CARNET_SPIN = args.spin
    if args.command:
        CARNET_COMMAND = args.command
    if args.debug:
        debug = True

    # Enable debugging of http requests (gives more details on Python 2 than 3 it seems)
    if debug:
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
    else:
        if not certverify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = requests.Session()
    # Get list of browsers the site can support
    # print(CarNetPost(session, portal_base_url + '/portal/en_GB/web/guest/home', '/-/mainnavigation/get-supported-browsers'))
    # Resp ex: {"errorCode":"0","supportedBrowsersResponse":{"browsers":[{"name":"MS Edge","minimalVersion":"15"},{"name":"Internet Explorer","minimalVersion":"11"},{"name":"Safari","minimalVersion":"10"},{"name":"Chrome","minimalVersion":"61"},{"name":"Firefox","minimalVersion":"52"}]}}

    # Get list of countries the site can support
    # print(CarNetPost(session, portal_base_url + '/portal/en_GB/web/guest/home', '/-/mainnavigation/get-countries'))
    # Resp ex: {"errorCode":"0", long list with supported countries}

    url, msg = CarNetLogin(session, CARNET_USERNAME, CARNET_PASSWORD)
    if url == '':
        print('Failed to login', msg)
        sys.exit()

    # If a VIN is specified, put that in the base URL so more than just first car can be controlled
    if CARNET_VIN:
        vin_start = url.rfind('/', 1, -2)
        url = url[0:vin_start+1] + CARNET_VIN + '/'
    else:
        resp = getVIN(session, url, args.index)
        CARNET_VIN = resp.get('vin')

    if debug:
        print('Using VIN : ' + CARNET_VIN)

    # We need to load a car is spin commands are used
    if CARNET_SPIN:
        response = CarNetPost(session, url, '/-/mainnavigation/load-car-details/' + CARNET_VIN)
        if debug:
            print(response)

    if CARNET_COMMAND == 'startCharge':
        startCharge(session, url)
    elif CARNET_COMMAND == 'stopCharge':
        stopCharge(session, url)
    elif CARNET_COMMAND == 'getCharge':
        getCharge(session, url)
    elif CARNET_COMMAND == 'startClimat' or CARNET_COMMAND == 'startClimate':
        startClimat(session, url)
    elif CARNET_COMMAND == 'stopClimat' or CARNET_COMMAND == 'stopClimate':
        stopClimat(session, url)
    elif CARNET_COMMAND == 'getClimat' or CARNET_COMMAND == 'getClimate':
        getClimat(session, url)
    elif CARNET_COMMAND == 'startWindowMelt':
        startWindowMelt(session, url)
    elif CARNET_COMMAND == 'stopWindowMelt':
        stopWindowMelt(session, url)
    elif CARNET_COMMAND == 'getWindowMelt':
        getWindowMelt(session, url)
    elif CARNET_COMMAND == 'getVIN':
        print(getVIN(session, url, args.index))
    elif CARNET_COMMAND == 'remoteLock':
        remoteLock(session, url, CARNET_SPIN, CARNET_VIN)
    elif CARNET_COMMAND == 'remoteUnlock':
        remoteUnlock(session, url, CARNET_SPIN, CARNET_VIN)
    elif CARNET_COMMAND == 'startRemoteVentilation':
        startRemoteAccessVentilation(session, url, CARNET_SPIN, CARNET_VIN)
    elif CARNET_COMMAND == 'stopRemoteVentilation':
        stopRemoteAccessVentilation(session, url)
    elif CARNET_COMMAND == 'startRemoteHeating':
        startRemoteAccessHeating(session, url, CARNET_SPIN, CARNET_VIN)
    elif CARNET_COMMAND == 'stopRemoteHeating':
        stopRemoteAccessHeating(session, url)
    elif CARNET_COMMAND == 'getRemoteHeating':
        getRemoteAccessHeating(session, url)
    elif CARNET_COMMAND == 'getLatestReport':
        getLatestReport(session, url)
    elif CARNET_COMMAND == 'getGeofences':
        getGeofences(session, url)
    elif CARNET_COMMAND == 'getAlerts':
        getAlerts(session, url)
    else:
        retrieveCarNetInfo(session, url)

    # Below is the flow the web app is using to determine when action really started
    # You should look at the notifications until it returns a status JSON like this
    # {"errorCode":"0","actionNotificationList":[{"actionState":"SUCCEEDED","actionType":"STOP","serviceType":"RBC","errorTitle":null,"errorMessage":null}]}
    # print(CarNetPost(session, url, '/-/msgc/get-new-messages'))
    # print(CarNetPost(session, url, '/-/emanager/get-notifications'))
    # print(CarNetPost(session, url, '/-/emanager/get-emanager'))

    # Get the remote heating request status
    # After start / stop command it will first report in progress
    # {"rahRequestStatus":{"state":"REQUEST_IN_PROGRESS"},"errorCode":"0"}
    # You should look at the notifications until it returns the JSON like this
    # {"rahRequestStatus":{"state":"REQUEST_SUCCESSFUL"},"errorCode":"0"}
    # print(CarNetPost(session, url, '/-/rah/get-request-status'))

    # Get the remote lock/unlock status
    # After lock / unlock command it will first report in progress
    # {"errorCode":"0","rluRequestStatus":{"status":"REQUEST_IN_PROGRESS","resultData":null}}
    # You should look at the notifications until it returns the JSON like this
    # {"rahRequestStatus":{"state":"REQUEST_SUCCESSFUL"},"errorCode":"0"}
    # print(CarNetPost(session, url, '/-/vsr/get-request-status'))

    # End session properly
    response = CarNetPost(session, url, '/-/logout/revoke')
    if debug:
        print(response)
