import json
import uuid
import hashlib
import urllib.parse as urlparse
from urllib.parse import parse_qs

import parameters
import soclogging
import kiahttp
import stamps


def getUserHash():
    try:
        account = parameters.getParameter('accountName') + ':' + parameters.getParameter('accountPassword')
        hash = hashlib.md5(account.encode()).hexdigest()
    except:
        raise

    return hash


def loadAccessToken():
    try:
        f = open(parameters.getParameter('tokenFile'), 'r')
        tokenDict = json.loads(f.read())
        f.close()

        parameters.setParameter('accessToken', tokenDict['accessToken'])
        parameters.setParameter('tokenType', tokenDict['tokenType'])
        parameters.setParameter('refreshToken', tokenDict['refreshToken'])
        parameters.setParameter('deviceId', tokenDict['deviceId'])
        try:
            if tokenDict['userHash'] == getUserHash():
                parameters.setParameter('userHash', tokenDict['userHash'])
            else:
                raise

        except:
            parameters.setParameter('userHash', getUserHash())
            raise

    except:
        raise

    return


def saveAccessToken(accessToken, deviceId):
    parameters.setParameter('accessToken', accessToken['access_token'])
    parameters.setParameter('tokenType', accessToken['token_type'])
    parameters.setParameter('refreshToken', accessToken['refresh_token'])
    parameters.setParameter('deviceId', deviceId)
    parameters.setParameter('userHash', getUserHash())

    token = {}
    token['accessToken'] = accessToken['access_token']
    token['tokenType'] = accessToken['token_type']
    token['refreshToken'] = accessToken['refresh_token']
    token['deviceId'] = deviceId
    token['userHash'] = getUserHash()

    f = open(parameters.getParameter('tokenFile'), 'w')
    f.write(json.dumps(token))
    f.close()

    return


def refreshAccessToken(refreshToken):
    soclogging.logDebug(2, "Refreshing access token")

    url = parameters.getParameter('baseUrl') + '/api/v1/user/oauth2/token'
    data = 'grant_type=refresh_token&redirect_uri=https://www.getpostman.com/oauth2/callback&refresh_token=' + refreshToken
    headers = {
        'Authorization': parameters.getParameter('basicToken'),
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(data)),
        'Host': parameters.getParameter('host'),
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.12.0'}

    try:
        response = kiahttp.postHTTP(url=url, headers=headers, data=data, timeout=parameters.getParameter('reqTimeout'))
    except:
        raise

    try:
        accessToken = json.loads(response)
        accessToken['refresh_token'] = refreshToken
    except:
        soclogging.logDebug(0, "Token request failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    soclogging.logDebug(2, "Access token = " + accessToken['access_token'])

    return accessToken


def getDeviceId():
    soclogging.logDebug(2, "Requesting DeviceId")

    url = parameters.getParameter('baseUrl') + '/api/v1/spa/notifications/register'

    data = {"pushRegId": parameters.getParameter('GCMSenderId'), "pushType": parameters.getParameter('PushType'), "uuid": str(uuid.uuid4())}
    headers = {
        'ccsp-service-id': parameters.getParameter('clientId'),
        'ccsp-application-id': parameters.getParameter('appId'),
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': str(len(data)),
        'Host': parameters.getParameter('host'),
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.0',
        'Stamp': stamps.getStamp()}

    try:
        response = kiahttp.postHTTP(url=url, data=data, headers=headers, timeout=parameters.getParameter('reqTimeout'))
    except:
        raise

    try:
        responseDict = json.loads(response)
        deviceId = responseDict['resMsg']['deviceId']
    except:
        soclogging.logDebug(1, "Could not receive DeviceId, invalid response")
        soclogging.logDebug(2, response)
        raise
    
    soclogging.logDebug(2, "DeviceId = " + deviceId)

    return deviceId


def getCookies():
    soclogging.logDebug(2, "Create login-session")

    url = parameters.getParameter('baseUrl') + '/api/v1/user/oauth2/authorize?response_type=code&state=test&client_id=' + \
        parameters.getParameter('clientId') + '&redirect_uri=' + \
        parameters.getParameter('baseUrl') + '/api/v1/user/oauth2/redirect'

    try:
        cookies = kiahttp.getHTTPCookies(url)
    except:
        raise
           
    url = parameters.getParameter('baseUrl') + '/api/v1/user/session'
    try:
        kiahttp.getHTTP(url=url, cookies=cookies,
                                   timeout=parameters.getParameter('reqTimeout'))
    except:
        raise
        
    url = parameters.getParameter('baseUrl') + '/api/v1/user/language'
    headers = {'Content-type': 'application/json'}
    data = {"lang": "en"}

    try:
        response = kiahttp.postHTTP(url=url, data=data, headers=headers, cookies=cookies,
                                    timeout=parameters.getParameter('reqTimeout'))
    except:
        raise
        
    url = parameters.getParameter('baseUrl') + '/api/v1/user/session'
    try:
        kiahttp.deleteHTTP(url=url, cookies=cookies,
                                   timeout=parameters.getParameter('reqTimeout'))
    except:
        raise
        
    return cookies


def getAuthCode(cookies):
    soclogging.logDebug(2, "Sending username/password")

    url = parameters.getParameter('baseUrl') + '/api/v1/user/integrationinfo'
    headers = {'Content-type': 'application/json'}

    try:
        response = kiahttp.getHTTP(url=url, headers=headers, cookies=cookies,
                                   timeout=parameters.getParameter('reqTimeout'))
    except:
        raise

    try:
        responseDict = json.loads(response)
        userId = responseDict['userId']
        serviceId = responseDict['serviceId']
        soclogging.logDebug(2, "UserId = " + userId)
        soclogging.logDebug(2, "ServiceId = " + serviceId)
    except:
        soclogging.logDebug(0, "Login failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    url = 'https://eu-account.' + parameters.getParameter('brand') + '.com/auth/realms/eu' + parameters.getParameter('brand') + 'idm/protocol/openid-connect/auth?client_id=' + parameters.getParameter(
        'authClientId') + '&scope=openid%20profile%20email%20phone&response_type=code&hkid_session_reset=true&redirect_uri=' + parameters.getParameter('baseUrl') + '/api/v1/user/integration/redirect/login&ui_locales=en&state=' + serviceId + ':' + userId
    headers = {}

    try:
        response = kiahttp.getHTTP(url=url, headers=headers, cookies=cookies,
                                   timeout=parameters.getParameter('reqTimeout'))
    except:
        raise

    left = response.find('action="') + 8
    right = response.find('"', left)
    url = response[left:right].replace('&amp;', '&')
    data = urlparse.urlencode({'username': parameters.getParameter('accountName'), 'password': parameters.getParameter(
        'accountPassword'), 'credentialId': ''})
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 Mobile/15B92 Safari/604.1'}
    cookies['AUTH_SESSION_ID'] = kiahttp.lastCookies['AUTH_SESSION_ID']

    try:
        response = kiahttp.postHTTP(url=url, data=data, headers=headers, cookies=cookies,
                                    timeout=parameters.getParameter('reqTimeout'), allow_redirects=False)
    except:
        soclogging.logDebug(0, "Login failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    url = response
    try:
        response = kiahttp.getHTTP(url=url, cookies=cookies,
                                   timeout=parameters.getParameter('reqTimeout'), allow_redirects=True)
    except:
        raise

    url = parameters.getParameter('baseUrl') + '/api/v1/user/silentsignin'
    headers = {'Content-type': 'text/plain;charset=UTF-8'}
    data = {'intUserId': ""}

    try:
        response = kiahttp.postHTTP(url=url, data=data, headers=headers, cookies=cookies,
                                    timeout=parameters.getParameter('reqTimeout'), allow_redirects=False)
        responseDict = json.loads(response)
        responseUrl = responseDict['redirectUrl']
        parsed = urlparse.urlparse(responseUrl)
        authCode = ''.join(parse_qs(parsed.query)['code'])
    except:
        soclogging.logDebug(0, "Login failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    soclogging.logDebug(2, "AuthCode = " + authCode)

    return authCode


def getAuthToken(authCode):
    soclogging.logDebug(2, "Requesting access token")

    url = parameters.getParameter('baseUrl') + '/api/v1/user/oauth2/token'
    data = 'grant_type=authorization_code&redirect_uri=' + \
        parameters.getParameter('baseUrl') + '%2Fapi%2Fv1%2Fuser%2Foauth2%2Fredirect&code=' + authCode
    headers = {
        'Authorization': parameters.getParameter('basicToken'),
        'Content-type': 'application/x-www-form-urlencoded',
        'Content-Length': str(len(data)),
        'Host': parameters.getParameter('host'),
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.12.0'}

    try:
        response = kiahttp.postHTTP(url=url, headers=headers, data=data, timeout=parameters.getParameter('reqTimeout'))
    except:
        raise

    try:
        accessToken = json.loads(response)
    except:
        soclogging.logDebug(0, "Token request failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    soclogging.logDebug(2, "Access token = " + accessToken['access_token'])

    return accessToken


def getControlToken(pin):
    soclogging.logDebug(2, "Sending PIN")

    url = parameters.getParameter('baseUrl') + '/api/v1/user/pin'
    data = {"deviceId": parameters.getParameter('deviceId'), "pin": pin}
    headers = {
        'Authorization': parameters.getParameter('tokenType') + ' ' + parameters.getParameter('accessToken'),
        'Content-type': 'application/json;charset=UTF-8',
        'Content-Length': str(len(data)),
        'Host': parameters.getParameter('host'),
        'Connection': 'close',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/3.12.0'}

    try:
        response = kiahttp.putHTTP(url=url, data=data, headers=headers, timeout=parameters.getParameter('reqTimeout'))
    except:
        raise

    try:
        responseDict = json.loads(response)
        controlToken = 'Bearer ' + responseDict['controlToken']
    except:
        soclogging.logDebug(1, "Sending PIN failed, invalid response")
        soclogging.logDebug(2, response)
        raise

    soclogging.logDebug(2, "Control token = " + controlToken)

    return controlToken


def refreshAuthToken():
    try:
        accessToken = refreshAccessToken(parameters.getParameter('refreshToken'))
        saveAccessToken(accessToken, parameters.getParameter('deviceId'))
    except:
        raise

    return


def requestNewAuthToken():
    try:
        cookies = getCookies()
        authCode = getAuthCode(cookies)
        accessToken = getAuthToken(authCode)
        deviceId = getDeviceId()
        saveAccessToken(accessToken, deviceId)
    except:
        raise

    return


def requestNewControlToken():
    try:
        controlToken = getControlToken(parameters.getParameter('accountPin'))
        parameters.setParameter('controlToken', controlToken)
    except:
        raise

    return


def updateAuthToken():
    try:
        loadAccessToken()
        refreshAuthToken()
    except:
        try:
            requestNewAuthToken()
        except:
            raise
        pass

    return
