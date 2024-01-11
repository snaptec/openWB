import json

import requests
import soclogging

lastCookies = {}
lastUrl = ""


def getHTTP(url='', headers='', cookies='', timeout=30, allow_redirects=True):
    global lastCookies
    global lastUrl

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=timeout, allow_redirects=allow_redirects)
    except requests.Timeout as err:
        soclogging.logDebug(1, "Connection Timeout")
        raise
    except:
        soclogging.logDebug(1, "HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        lastCookies = response.cookies.get_dict()
        return response.text
    elif response.status_code == 302:
        return response.headers['Location']
    else:
        try:
            responseDict = json.loads(response.text)
            if response.status_code == 400 or response.status_code == 408 or response.status_code == 503:
                errorString = "[" + responseDict['resCode'] + "] " + responseDict['resMsg']
            else:
                errorString = "[" + responseDict['errCode'] + "] " + responseDict['errMsg']
        except:
            errorString = "[XXXX] Unidentified Error" + " " + response.text
        soclogging.logDebug(1, 'Request failed, StatusCode: ' + str(response.status_code) + ', Error: ' + errorString)
        raise RuntimeError

    return


def putHTTP(url='', data='', headers='', cookies='', timeout=30):
    try:
        if isinstance(data, dict):
            response = requests.put(url, json=data, headers=headers, cookies=cookies, timeout=timeout)
        else:
            response = requests.put(url, data=data, headers=headers, cookies=cookies, timeout=timeout)
    except requests.Timeout as err:
        soclogging.logDebug(1, "Connection Timeout")
        raise
    except:
        soclogging.logDebug(1, "HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        return response.text
    else:
        try:
            responseDict = json.loads(response.text)
            if response.status_code == 408:
                errorString = "[" + responseDict['resCode'] + "] " + responseDict['resMsg']
            else:
                errorString = "[" + responseDict['errCode'] + "] " + responseDict['errMsg']
        except:
            errorString = "[XXXX] Unidentified Error"
        soclogging.logDebug(1, 'Request failed, StatusCode: ' + str(response.status_code) + ', Error: ' + errorString)
        raise RuntimeError

    return
    
def deleteHTTP(url='', headers='', cookies='', timeout=30):
    try:
        response = requests.delete(url, headers=headers, cookies=cookies, timeout=timeout)
    except requests.Timeout as err:
        soclogging.logDebug(1, "Connection Timeout")
        raise
    except:
        soclogging.logDebug(1, "HTTP Error")
        raise

    return


def postHTTP(url='', data='', headers='', cookies='', timeout=30, allow_redirects=True):
    global lastCookies
    global lastUrl

    try:
        if isinstance(data, dict):
            response = requests.post(url, json=data, headers=headers, cookies=cookies,
                                     timeout=timeout, allow_redirects=allow_redirects)
        else:
            response = requests.post(url, data=data, headers=headers, cookies=cookies,
                                     timeout=timeout, allow_redirects=allow_redirects)
    except requests.Timeout as err:
        soclogging.logDebug(1, "Connection Timeout")
        raise
    except:
        soclogging.logDebug(1, "HTTP Error")
        raise

    if response.status_code == 200 or response.status_code == 204:
        lastUrl = response.url
        return response.text
    elif response.status_code == 302:
        return response.headers['Location']
    else:
        try:
            responseDict = json.loads(response.text)
            if response.status_code == 408:
                errorString = "[" + responseDict['resCode'] + "] " + responseDict['resMsg']
            else:
                errorString = "[" + responseDict['errCode'] + "] " + responseDict['errMsg']
        except:
            errorString = "[XXXX] Unidentified Error"
        soclogging.logDebug(1, 'Request failed, StatusCode: ' + str(response.status_code) + ', Error: ' + errorString)
        raise RuntimeError

    return


def getHTTPCookies(url):
    try:
        session = requests.Session()
        response = session.get(url)
    except requests.Timeout as err:
        soclogging.logDebug(1, "Connection Timeout")
        raise

    if response.status_code == 200:
        cookies = session.cookies.get_dict()
    else:
        soclogging.logDebug(1, "Receiving cookies failed, StatusCode: " + str(response.status_code))
        raise

    return cookies
