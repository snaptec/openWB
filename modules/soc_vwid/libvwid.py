# A Python class to communicate with the "We Connect ID" API.
# As there is no official API documentation, this is to a large extent inspired by
# the following PHP implementation:
# https://github.com/robske110/IDDataLogger/blob/master/src/vwid/api/MobileAppAPI.php
# Jon Petter Skagmo, 2021

import secrets
import lxml.html
import logging
import aiohttp
import asyncio
import json

# Constants
LOGIN_BASE = "https://login.apps.emea.vwapps.io"
LOGIN_HANDLER_BASE = "https://identity.vwgroup.io"
API_BASE = "https://mobileapi.apps.emea.vwapps.io"

class vwid:
	def __init__(self, session):
		self.session = session
		self.headers = {}
		self.log = logging.getLogger(__name__)

	def form_from_response(self, text):
		page = lxml.html.fromstring(text)
		elements = page.xpath('//form//input[@type="hidden"]')
		form = {x.attrib['name']: x.attrib['value'] for x in elements}
		return (form, page.forms[0].action)

	def password_form(self, text):
		page = lxml.html.fromstring(text)
		elements = page.xpath('//script')

		# Todo: Find more elegant way parse this...
		objects = {}
		for a in elements:
			if (a.text) and (a.text.find('window._IDK') != -1):
				text = a.text.strip()
				text = text[text.find('\n'):text.rfind('\n')].strip()

				for line in text.split('\n'):
					(name, val) = line.strip().split(':', 1)
					val = val.strip('\', ')
					objects[name] = val

		json_model = json.loads(objects['templateModel'])

		if ('errorCode' in json_model):
			self.log.error("Login error: %s", json_model['errorCode'])
			return False

		try:
			# Generate form
			form = {}
			form['relayState'] = json_model['relayState']
			form['hmac'] = json_model['hmac']
			form['email'] = json_model['emailPasswordForm']['email']
			form['_csrf'] = objects['csrf_token']

			# Generate URL action
			action = '/signin-service/v1/%s/%s' % (json_model['clientLegalEntityModel']['clientId'], json_model['postAction'])

			return (form, action)

		except KeyError:
			self.log.error("Missing fields in response from VW API")
			return False

	def set_vin(self, vin):
		self.vin = vin

	def set_credentials(self, username, password):
		self.username = username
		self.password = password
		
	async def connect(self, username, password):
		self.set_credentials(username, password)
		return (await self.reconnect())

	async def reconnect(self):
		# Get authorize page
		payload = {
			'nonce': secrets.token_urlsafe(12), 
			'redirect_uri': 'weconnect://authenticated'
		}

		response = await self.session.get(LOGIN_BASE + '/authorize', params=payload)
		if response.status >= 400:
			# Non 2xx response, failed
			return False

		# Fill form with email (username)
		(form, action) = self.form_from_response(await response.read())
		form['email'] = self.username
		response = await self.session.post(LOGIN_HANDLER_BASE+action, data=form)
		if response.status >= 400:
			self.log.error("Email fail")
			return False
			
		# Fill form with password
		(form, action) = self.password_form(await response.read())
		form['password'] = self.password
		url = LOGIN_HANDLER_BASE + action
		response = await self.session.post(url, data=form, allow_redirects=False)

		# Can get a 303 redirect for a "terms and conditions" page
		if (response.status == 303):
			url = response.headers['Location']
			if ("terms-and-conditions" in url):
				# Get terms and conditions page
				url = LOGIN_HANDLER_BASE + url
				response = await self.session.get(url, data=form, allow_redirects=False)

				(form, action) = self.form_from_response(await response.read())
				url = LOGIN_HANDLER_BASE + action
				response = await self.session.post(url, data=form, allow_redirects=False)

				self.log.warn("Agreed to terms and conditions")
			else:
				self.log.error("Got unknown 303 redirect")
				return False

		# Handle every single redirect and stop if the redirect
		# URL uses the weconnect adapter.
		while (True):
			url = response.headers['Location']
			if (url.split(':')[0] == "weconnect"):
				if not ('access_token' in url):
					self.log.error("Missing access token")
					return False
					# Parse query string
				query_string = url.split('#')[1]
				query = {x[0] : x[1] for x in [x.split("=") for x in query_string.split("&") ]}
				break

			if (response.status != 302):
				self.log.error("Not redirected, status %u" % response.status)
				return False

			response = await self.session.get(url, data=form, allow_redirects=False)

		self.headers = dict(response.headers)

		# Get final token
		payload = {
			'state': query['state'],
			'id_token': query['id_token'],
			'redirect_uri': "weconnect://authenticated",
			'region': "emea",
			'access_token': query["access_token"],
			'authorizationCode': query["code"]
		}
		response = await self.session.post(LOGIN_BASE + '/login/v1', json=payload)
		if response.status >= 400:
			self.log.error("Login failed")
			# Non 2xx response, failed
			return False
		self.tokens = await response.json()

		# Update header with final token
		self.headers['Authorization'] = 'Bearer %s' % self.tokens["accessToken"]

		# Success
		return True
		
	async def refresh_tokens(self):
		if not self.headers:
			return False

		# Use the refresh token
		self.headers['Authorization'] = 'Bearer %s' % self.tokens["refreshToken"]
		
		response = await self.session.get(LOGIN_BASE + '/refresh/v1', headers=self.headers)
		if response.status >= 400:
			return False
		self.tokens = await response.json()
		
		# Use the newly received access token
		self.headers['Authorization'] = 'Bearer %s' % self.tokens["accessToken"]

		return True

	async def get_status(self):
		response = await self.session.get(API_BASE + "/vehicles/" + self.vin + "/status", headers=self.headers)

		# If first attempt fails, try to refresh tokens
		if response.status >= 400:
			self.log.debug("Refreshing tokens")
			if await self.refresh_tokens():
				response = await self.session.get(API_BASE + "/vehicles/" + self.vin + "/status", headers=self.headers)
			
		# If refreshing tokens failed, try a full reconnect
		if response.status >= 400:
			self.log.info("Reconnecting")
			if await self.reconnect():
				response = await self.session.get(API_BASE + "/vehicles/" + self.vin + "/status", headers=self.headers)
			
		if response.status >= 400:
			self.log.error("Get status failed")
			return {}
			
		return (await response.json())
