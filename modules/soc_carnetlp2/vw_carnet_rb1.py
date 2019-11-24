#!/usr/bin/python
# Comment youpixel - I ran it with Python 3.7, works fine!

# Script to emulate VW CarNet web site
# Author  : Rene Boer
# Version : 1.0
# Date    : 5 Jan 2018
# Free for use & distribution
# Modified by youpixel - 2019-07-26
# 
# Modified by ElectricArtram - 2019-08-03
# fix to ensure compatibility to Python 2 and 3 (successfully tested with Python 2.7.13 and 3.5.3)

import re
import requests
import json
import sys

# Login information for the VW CarNet app
CARNET_USERNAME = sys.argv[1]
CARNET_PASSWORD = sys.argv[2]


HEADERS = { 'Accept': 'application/json, text/plain, */*',
			'Content-Type': 'application/json;charset=UTF-8',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; D5803 Build/23.5.A.1.291; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36' }


def CarNetLogin(s,email, password):
	AUTHHEADERS = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; D5803 Build/23.5.A.1.291; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36' }
	auth_base_url = "https://identity.vwgroup.io"
	base_url = "https://www.portal.volkswagen-we.com"
	landing_page_url = base_url + '/portal/en_GB/web/guest/home'
	get_login_url = base_url + '/portal/en_GB/web/guest/home/-/csrftokenhandling/get-login-url'
	complete_login_url = base_url + "/portal/web/guest/complete-login"

	# Regular expressions to extract data
	# Comment youpixel - Modified the regex a bit to match the new input values defined e.g. in def extract_login_action_url
	csrf_re = re.compile('<meta name="_csrf" content="([^"]*)"/>')
	redurl_re = re.compile('<redirect url="([^"]*)"></redirect>')
	login_action_url_re = re.compile('<formclass="content"id="emailPasswordForm"name="emailPasswordForm"method="POST"novalidate.*action="([^"]*)">')
	login_action_url2_re = re.compile('<formclass="content"id="credentialsForm"name="credentialsForm"method="POST"action="([^"]*)">')
	
	
	login_relay_state_token_re = re.compile('<inputtype="hidden"id="input_relayState"name="relayState"value="([^"]*)"/>')
	login_csrf_re = re.compile('<inputtype="hidden"id="csrf"name="_csrf"value="([^"]*)"/>')
	login_hmac_re = re.compile('<inputtype="hidden"id="hmac"name="hmac"value="([^"]*)"/>')

	authcode_re = re.compile('&code=([^"]*)')
	authstate_re = re.compile('state=([^"]*)')

	def extract_csrf(r):
		return csrf_re.search(r.text).group(1)

	def extract_login_action_url(r):
		# Comment youpixel - The form we are looking for in the output is spreaded over multiple lines. Just stripped all newlines and spaces...
		loginhtml = r.text.replace('\n', '').replace('\r', '').replace(' ', '')
		return login_action_url_re.search(loginhtml).group(1)

	def extract_login_action2_url(r):
		# Comment youpixel - Same here
		loginhtml = r.text.replace('\n', '').replace('\r', '').replace(' ', '')
		return login_action_url2_re.search(loginhtml).group(1)

	def extract_login_relay_state_token(r):
		# Comment youpixel - Same here
		loginhtml = r.text.replace('\n', '').replace('\r', '').replace(' ', '')
		return login_relay_state_token_re.search(loginhtml).group(1)

	def extract_login_hmac(r):
		# Comment youpixel - Same here
		loginhtml = r.text.replace('\n', '').replace('\r', '').replace(' ', '')
		return login_hmac_re.search(loginhtml).group(1)

	def extract_login_csrf(r):
		# Comment youpixel - Same here
		loginhtml = r.text.replace('\n', '').replace('\r', '').replace(' ', '')
		return login_csrf_re.search(loginhtml).group(1)

	def extract_code(r):
		return authcode_re.search(r).group(1)

	def build_complete_login_url(state):
		return complete_login_url + '?p_auth=' + state + '&p_p_id=33_WAR_cored5portlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_33_WAR_cored5portlet_javax.portlet.action=getLoginStatus'

	# Request landing page and get CSRF:
	#print("Requesting first CSRF from landing page (", landing_page_url, ")...", sep='')
	r = s.get(landing_page_url)
	if r.status_code != 200:
		return ""
	csrf = extract_csrf(r)
	#print("CSRF found to be '", csrf, "'", sep='')

	# Request login page and get CSRF
	AUTHHEADERS["Referer"] = base_url + '/portal'
	AUTHHEADERS["X-CSRF-Token"] = csrf
	r = s.post(get_login_url, headers=AUTHHEADERS)
	if r.status_code != 200:
		return ""
		
	#print("DEBUG AP: ", r.json().get("loginURL").get("path"))
	#login_url = json.loads(r.content).get("loginURL").get("path")
	login_url = r.json().get("loginURL").get("path")
	#print("SSO Login url found to be '", login_url, "'", sep='')

	# no redirect so we can get values we look for
	r = s.get(login_url, allow_redirects=False, headers=AUTHHEADERS)
	if r.status_code != 302:
		return ""
	login_form_url = r.headers.get("location")

	r = s.get(login_form_url, headers=AUTHHEADERS)
	if r.status_code != 200:
		return ""
	login_action_url = auth_base_url + extract_login_action_url(r)

	login_relay_state_token = extract_login_relay_state_token(r)
	hmac_token = extract_login_hmac(r)
	login_csrf = extract_login_csrf(r)
	
	# Login with user details
	del AUTHHEADERS["X-CSRF-Token"]
	AUTHHEADERS["Referer"] = login_form_url
	AUTHHEADERS["Content-Type"] = "application/x-www-form-urlencoded"

	# Comment youpixel - Sending E-Mail address for login and get URL of second step
	post_data = {
		'email': email,
		'relayState': login_relay_state_token,
		'_csrf': login_csrf,
		'hmac': hmac_token,
	}
	r = s.post(login_action_url, data=post_data, headers=AUTHHEADERS, allow_redirects=True)
	if r.status_code != 200:
		return ""
	
	AUTHHEADERS["Referer"] = login_action_url
	AUTHHEADERS["Content-Type"] = "application/x-www-form-urlencoded"
	
	login_action_url2 = auth_base_url + extract_login_action2_url(r)
	login_relay_state_token = extract_login_relay_state_token(r)
	hmac_token = extract_login_hmac(r)
	login_csrf = extract_login_csrf(r)
	
	# Comment youpixel - Completing the authentication by entering password. HMAC is new. Relay state and CSRF stays same!
	post_data = {
		'email': email,
		'password': password,
		'relayState': login_relay_state_token,
		'_csrf': login_csrf,
		'hmac': hmac_token,
		'login': 'true'
	}
	r = s.post(login_action_url2, data=post_data, headers=AUTHHEADERS, allow_redirects=True)
	if r.status_code != 200:
		return ""

	
	# Now we are going through 4 redirect pages, before finally landing on complete-login page.
	# Allow redirects to happen
	ref2_url = r.headers.get("location")	
	
	#print(ref2_url)
	#print("Successfully login through the vw auth system. Now proceeding through to the we connect portal.", ref2_url)

#	state = extract_state(ref_url2)
	# load ref page
	#r = s.get(ref2_url, headers=AUTHHEADERS, allow_redirects=True)
	#if r.status_code != 200:
	#	return ""

	#print("OK2")

	portlet_code = extract_code(r.url)
	
	state = extract_csrf(r)

	# Extract csrf and use in new url as post
	# We need to include post data
	# _33_WAR_cored5portlet_code=

	# We need to POST to
	# https://www.portal.volkswagen-we.com/portal/web/guest/complete-login?p_auth=cF3xgdcf&p_p_id=33_WAR_cored5portlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_33_WAR_cored5portlet_javax.portlet.action=getLoginStatus
	# To get the csrf for the final json requests
	# We also need the base url for json requests as returned by the 302 location. This is the location from the redirect

	AUTHHEADERS["Referer"] = ref2_url
	post_data = {
		'_33_WAR_cored5portlet_code': portlet_code
	}
	#print("Complete_url_login: ", build_complete_login_url(state))
	r = s.post(build_complete_login_url(state), data=post_data, allow_redirects=False, headers=AUTHHEADERS)
	if r.status_code != 302:
		return ""
	base_json_url = r.headers.get("location")
	r = s.get(base_json_url, headers=AUTHHEADERS)
	#We have a new CSRF
	csrf = extract_csrf(r)
	# done!!!! we are in at last
	# Update headers for requests
	HEADERS["Referer"] = base_json_url
	HEADERS["X-CSRF-Token"] = csrf
	#print("Login successful. Base_json_url is found as", base_json_url)
	return base_json_url

	
def CarNetPost(s,url_base,command):
	print(command)
	r = s.post(url_base + command, headers=HEADERS)
	return r.text
	
def CarNetPostAction(s,url_base,command,data):
	print(command)
	r = s.post(url_base + command, json=data, headers=HEADERS)
	return r.text

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
	url = CarNetLogin(s,CARNET_USERNAME,CARNET_PASSWORD)
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
	
