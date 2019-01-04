#!/usr/bin/python
# Script to emulate VW CarNet web site
# Author  : Rene Boer
# Version : 1.0
# Date    : 5 Jan 2018
# Free for use & distribution

import re
import requests
import json
import sys
from urlparse import urlsplit

# Login information for the VW CarNet app
carnetuser = sys.argv[1]
carnetpass = sys.argv[2]


HEADERS = { 'Accept': 'application/json, text/plain, */*',
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; D5803 Build/23.5.A.1.291; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36' }


def CarNetLogin(s,email, password):
	AUTHHEADERS = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; D5803 Build/23.5.A.1.291; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36' }
	auth_base = "https://security.volkswagen.com"
	base = "https://www.volkswagen-car-net.com"

	# Regular expressions to extract data
	csrf_re = re.compile('<meta name="_csrf" content="([^"]*)"/>')
	redurl_re = re.compile('<redirect url="([^"]*)"></redirect>')
	viewstate_re = re.compile('name="javax.faces.ViewState" id="j_id1:javax.faces.ViewState:0" value="([^"]*)"')
	authcode_re = re.compile('code=([^"]*)&')
	authstate_re = re.compile('state=([^"]*)')
    
	def extract_csrf(r):
		return csrf_re.search(r.text).group(1)

	def extract_redirect_url(r):
		return redurl_re.search(r.text).group(1)

	def extract_view_state(r):
		return viewstate_re.search(r.text).group(1)

	def extract_code(r):
		return authcode_re.search(r).group(1)

	def extract_state(r):
		return authstate_re.search(r).group(1)

	# Request landing page and get CSFR:
	r = s.get(base + '/portal/en_GB/web/guest/home')
	if r.status_code != 200:
		return ""
	csrf = extract_csrf(r)
	#print(csrf)
	
	# Request login page and get CSRF
	AUTHHEADERS["Referer"] = base + '/portal'
	AUTHHEADERS["X-CSRF-Token"] = csrf
	r = s.post(base + '/portal/web/guest/home/-/csrftokenhandling/get-login-url',headers=AUTHHEADERS)
	if r.status_code != 200:
		return ""
	responseData = json.loads(r.content)
	lg_url = responseData.get("loginURL").get("path")
	#print(lg_url)
	# no redirect so we can get values we look for
	r = s.get(lg_url, allow_redirects=False, headers=AUTHHEADERS)
	if r.status_code != 302:
		return ""
	ref_url = r.headers.get("location")
	#print(ref_url)
	
	# now get actual login page and get session id and ViewState
	r = s.get(ref_url, headers=AUTHHEADERS)
	if r.status_code != 200:
		return ""
	view_state = extract_view_state(r)
	#print(view_state)

	# Login with user details
	AUTHHEADERS["Faces-Request"] = "partial/ajax"
	AUTHHEADERS["Referer"] = ref_url
	AUTHHEADERS["X-CSRF-Token"] = ''

	post_data = {
		'loginForm': 'loginForm',
		'loginForm:email': email,
		'loginForm:password': password,
		'loginForm:j_idt19': '',
		'javax.faces.ViewState': view_state,
		'javax.faces.source': 'loginForm:submit',
		'javax.faces.partial.event': 'click',
		'javax.faces.partial.execute': 'loginForm:submit loginForm',
		'javax.faces.partial.render': 'loginForm',
		'javax.faces.behavior.event': 'action',
		'javax.faces.partial.ajax': 'true'
	}
	r = s.post(auth_base + '/ap-login/jsf/login.jsf', data=post_data, headers=AUTHHEADERS)
	if r.status_code != 200:
		return ""
	ref_url = extract_redirect_url(r).replace('&amp;', '&')
	#print(ref_url)
	# redirect to link from login and extract state and code values
	r = s.get(ref_url, allow_redirects=False, headers=AUTHHEADERS)
	if r.status_code != 302:
		return ""
	ref_url2 = r.headers.get("location")
	#print(ref_url2)
	code = extract_code(ref_url2)
	state = extract_state(ref_url2)
	# load ref page
	r = s.get(ref_url2, headers=AUTHHEADERS)
	if r.status_code != 200:
		return ""

	AUTHHEADERS["Faces-Request"] = ""
	AUTHHEADERS["Referer"] = ref_url2
	post_data = {
		'_33_WAR_cored5portlet_code': code,
		'_33_WAR_cored5portlet_landingPageUrl': ''
	}
	r = s.post(base + urlsplit(ref_url2).path + '?p_auth=' + state + '&p_p_id=33_WAR_cored5portlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_33_WAR_cored5portlet_javax.portlet.action=getLoginStatus', data=post_data, allow_redirects=False, headers=AUTHHEADERS)
	if r.status_code != 302:
		return ""
	ref_url3 = r.headers.get("location")
	#print(ref_url3)
	r = s.get(ref_url3, headers=AUTHHEADERS)
	#We have a new CSRF
	csrf = extract_csrf(r)
	# done!!!! we are in at last
	# Update headers for requests
	HEADERS["Referer"] = ref_url3
	HEADERS["X-CSRF-Token"] = csrf
	return ref_url3
	
def CarNetPost(s,url_base,command):
	print(command)
	r = s.post(url_base + command, headers=HEADERS)
	return r.content
	
def CarNetPostAction(s,url_base,command,data):
	print(command)
	r = s.post(url_base + command, json=data, headers=HEADERS)
	return r.content

def retrieveCarNetInfo(s,url_base):
	print(CarNetPost(s,url_base, '/-/msgc/get-new-messages'))
	print(CarNetPost(s,url_base, '/-/vsr/request-vsr'))
	print(CarNetPost(s,url_base, '/-/vsr/get-vsr'))
	print(CarNetPost(s,url_base, '/-/cf/get-location'))
	print(CarNetPost(s,url_base, '/-/vehicle-info/get-vehicle-details'))
	print(CarNetPost(s,url_base, '/-/emanager/get-emanager'))
	return 0

def startCharge(s,url_base):
	post_data = {
		'triggerAction': True,
		'batteryPercent': '100'
	}
	print(CarNetPostAction(s,url_base, '/-/emanager/charge-battery', post_data))
	return 0

def stopCharge(s,url_base):
	post_data = {
		'triggerAction': False,
		'batteryPercent': '99'
	}
	print(CarNetPostAction(s,url_base, '/-/emanager/charge-battery', post_data))
	return 0

def startClimat(s,url_base):  
	post_data = {
		'triggerAction': True,
		'electricClima': True
	}
	print(CarNetPostAction(s,url_base, '/-/emanager/trigger-climatisation', post_data))
	return 0

def stopClimat(s,url_base):
	post_data = {
		'triggerAction': False,
		'electricClima': True
	}
	print(CarNetPostAction(s,url_base, '/-/emanager/trigger-climatisation', post_data))
	return 0

def startWindowMelt(s,url_base):
	post_data = {
		'triggerAction': True
	}
	print(CarNetPostAction(s,url_base, '/-/emanager/trigger-windowheating', post_data))
	return 0

def stopWindowMelt(s,url_base):
	post_data = {
		'triggerAction': False
	}
	print(CarNetPostAction(s,url_base, '/-/emanager/trigger-windowheating', post_data))
	return 0
	
	
if __name__ == "__main__":
	s = requests.Session()
	url = CarNetLogin(s,carnetuser,carnetpass)
	if url == '':
		print("Failed to login")
		sys.exit()

	if len(sys.argv) != 2:
		retrieveCarNetInfo(s,url)
	else:
		if(sys.argv[1] == "startCharge"):
			startCharge(s,url)
		elif(sys.argv[1] == "stopCharge"):
			stopCharge(s,url)
		elif(sys.argv[1] == "startClimat"):
			startClimat(s,url)
		elif(sys.argv[1] == "stopClimat"):
			stopClimat(s,url)
		elif(sys.argv[1] == "startWindowMelt"):
			startWindowMelt(s,url)
		elif(sys.argv[1] == "stopWindowMelt"):
			stopWindowMelt(s,url)
		# Below is the flow the web app is using to determine when action really started
		# You should look at the notifications until it returns a status JSON like this
		# {"errorCode":"0","actionNotificationList":[{"actionState":"SUCCEEDED","actionType":"STOP","serviceType":"RBC","errorTitle":null,"errorMessage":null}]}
		print(CarNetPost(s,url, '/-/msgc/get-new-messages'))
		print(CarNetPost(s,url, '/-/emanager/get-notifications'))
		print(CarNetPost(s,url, '/-/msgc/get-new-messages'))
		print(CarNetPost(s,url, '/-/emanager/get-emanager'))
	
