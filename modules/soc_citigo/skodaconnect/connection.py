#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Communicate with Skoda Connect services."""
"""Fork of https://github.com/robinostlund/volkswagencarnet"""
"""Modified to utilize API calls derived from Android Apps instead of Web API"""
import re
import time
import logging
import asyncio
import hashlib
import jwt

from sys import version_info, argv
from datetime import timedelta, datetime
from urllib.parse import urljoin, parse_qs, urlparse
from json import dumps as to_json
import aiohttp
from bs4 import BeautifulSoup
from base64 import b64decode, b64encode
from skodaconnect.__version__ import __version__ as lib_version
from skodaconnect.utilities import read_config, json_loads
from skodaconnect.vehicle import Vehicle
from skodaconnect.exceptions import (
    SkodaConfigException,
    SkodaAuthenticationException,
    SkodaAccountLockedException,
    SkodaTokenExpiredException,
    SkodaException,
    SkodaEULAException,
    SkodaThrottledException,
    SkodaLoginFailedException,
    SkodaInvalidRequestException,
    SkodaRequestInProgressException
)

from aiohttp import ClientSession, ClientTimeout
from aiohttp.hdrs import METH_GET, METH_POST

from .const import (
    BRAND,
    COUNTRY,
    HEADERS_SESSION,
    HEADERS_AUTH,
    BASE_SESSION,
    BASE_AUTH,
    CLIENT,
    XCLIENT_ID,
    XAPPVERSION,
    XAPPNAME,
    USER_AGENT,
    APP_URI,
)

version_info >= (3, 0) or exit('Python 3 required')

_LOGGER = logging.getLogger(__name__)

TIMEOUT = timedelta(seconds=30)

class Connection:
    """ Connection to VW-Group Connect services """
  # Init connection class
    def __init__(self, session, username, password, fulldebug=False, interval=timedelta(minutes=5)):
        """ Initialize """
        self._session = session
        self._session_fulldebug = fulldebug
        self._session_headers = HEADERS_SESSION.copy()
        self._session_base = BASE_SESSION
        self._session_auth_headers = HEADERS_AUTH.copy()
        self._session_auth_base = BASE_AUTH
        self._session_refresh_interval = interval

        self._session_auth_ref_url = BASE_SESSION
        self._session_spin_ref_url = BASE_SESSION
        self._session_logged_in = False
        self._session_first_update = False
        self._session_auth_username = username
        self._session_auth_password = password
        self._session_tokens = {}

        self._vin = ""
        self._vehicles = []

        _LOGGER.info(f'Init Skoda Connect library, version {lib_version}')
        _LOGGER.debug(f'Using service {self._session_base}')

        self._jarCookie = ""
        self._state = {}

    def _clear_cookies(self):
        self._session._cookie_jar._cookies.clear()

  # API Login
    async def doLogin(self):
        """Login method, clean login"""
        _LOGGER.debug('Initiating new login')
        # Remove cookies and re-init headers as we are doing a new login
        self._clear_cookies()
        self._session_headers = HEADERS_SESSION.copy()
        self._session_auth_headers = HEADERS_AUTH.copy()

        # Try login against connect services
        try:
            _LOGGER.info('Connecting to Skoda native API')
            if not await self._login('skoda'):
                _LOGGER.info('Something failed')
                self._session_logged_in = False
                return False
            # Successful login to Skoda API, try VW-Group connect
            else:
                if not await self._login('connect'):
                    _LOGGER.info('Something failed')
                    self._session_logged_in = False
                    return False
        except:
            raise


        # Get list of vehicles from Skoda native API
        await self.set_token('skoda')
        skoda_vehicles = await self.get(
            'https://api.connect.skoda-auto.cz/api/v2/garage/vehicles'
        )
        if not skoda_vehicles:
            _LOGGER.debug('Skoda native API returned no cars')
        else:
            # Fetch realCarData
            realCars = await self.getRealCarData()
            for vehicle in skoda_vehicles:
                vin = vehicle.get('vin', '')
                specs = vehicle.get('specification', '')
                connectivity = []
                for service in vehicle.get('connectivities', []):
                    connectivity.append(service.get('type', ''))

                if realCars is not False:
                    for item in realCars.get('realCars', {}):
                        if item.get('vehicleIdentificationNumber', '') == vin:
                            _LOGGER.debug(f'Matched VIN with item: {item}')
                            if vehicle.get('name', False):
                                nickname = vehicle.get('name', None)
                            else:
                                nickname = item.get('nickname', None)
                            deactivated = item.get('deactivated', False)
                else:
                    nickname = None
                    deactivated = False
                capabilities = []
                for capability in vehicle.get('capabilities', []):
                    capabilities.append(capability.get('id', ''))
                vehicle = {
                    'vin': vin,
                    'connectivities': connectivity,
                    'capabilities': capabilities,
                    'specification': specs,
                    'nickname': nickname,
                    'deactivated': deactivated
                }
                _LOGGER.debug(f'Adding vehicle {vin} with connectivities: {connectivity}')
                self._vehicles.append(Vehicle(self, vehicle))

        # Check if any associated vehicle is serviced by VW-Group API
        if any('ONLINE' in car._connectivities for car in self._vehicles):
            _LOGGER.info('Vehicle is enabled for VW-Group API, requesting VW-Group API tokens.')
            # Get VW-Group API tokens
            if not await self._getAPITokens():
                self._session_logged_in = False
                return False

        # Check if any associated vehicle is a SmartLink vehicle
        if any('INCAR' in car._connectivities for car in self._vehicles):
            _LOGGER.info('Vehicle has SmartLink enabled, requesting SmartLink tokens')
            # Get SmartLink tokens
            if not await self._login('smartlink'):
                _LOGGER.info('Something failed')
                self._session_logged_in = False
                return False

        # Dump all tokens for debugging purposes
        # WARNING! Tokens can give indefinite access to your account
        if self._session_fulldebug:
            _LOGGER.debug(f'Available token {self._session_tokens}')

        # Update all vehicles data before returning
        #await self.set_token('vwg')
        self._session_logged_in = True
        await self.update()
        return True

    async def _login(self, client='connect'):
        """Login function."""
        # Helper functions
        def getNonce():
            ts = "%d" % (time.time())
            sha256 = hashlib.sha256()
            sha256.update(ts.encode())
            return (b64encode(sha256.digest()).decode('utf-8')[:-1])

        def extract_csrf(req):
            return re.compile('<meta name="_csrf" content="([^"]*)"/>').search(req).group(1)

        def extract_guest_language_id(req):
            return req.split('_')[1].lower()

        # Login starts here
        try:
            # Get OpenID config:
            self._clear_cookies()
            self._session_headers = HEADERS_SESSION.copy()
            self._session_auth_headers = HEADERS_AUTH.copy()
            if self._session_fulldebug:
                _LOGGER.debug(f'Requesting openid config')
            req = await self._session.get(
                url='https://identity.vwgroup.io/.well-known/openid-configuration'
            )
            if req.status != 200:
                return False
            response_data =  await req.json()
            authorizationEndpoint = response_data['authorization_endpoint']
            authissuer = response_data['issuer']

            # Get authorization page (login page)
            # https://identity.vwgroup.io/oidc/v1/authorize?nonce={NONCE}&state={STATE}&response_type={TOKEN_TYPES}&scope={SCOPE}&redirect_uri={APP_URI}&client_id={CLIENT_ID}
            if self._session_fulldebug:
                _LOGGER.debug(f'Get authorization page from "{authorizationEndpoint}"')
                self._session_auth_headers.pop('Referer', None)
                self._session_auth_headers.pop('Origin', None)
            try:
                req = await self._session.get(
                    url=authorizationEndpoint+\
                        '?redirect_uri='+APP_URI+\
                        '&nonce='+getNonce()+\
                        '&state='+getNonce()+\
                        '&response_type='+CLIENT[client].get('TOKEN_TYPES')+\
                        '&client_id='+CLIENT[client].get('CLIENT_ID')+\
                        '&scope='+CLIENT[client].get('SCOPE'),
                    headers=self._session_auth_headers,
                    allow_redirects=False
                )
                if req.headers.get('Location', False):
                    ref = req.headers.get('Location', '')
                    if 'error' in ref:
                        error = parse_qs(urlparse(ref).query).get('error', '')[0]
                        if 'error_description' in ref:
                            error_description = parse_qs(urlparse(ref).query).get('error_description', '')[0]
                            _LOGGER.info(f'Unable to login, {error_description}')
                        else:
                            _LOGGER.info(f'Unable to login.')
                        raise SkodaException(error)
                    else:
                        if self._session_fulldebug:
                            _LOGGER.debug(f'Got redirect to "{ref}"')
                        req = await self._session.get(
                            url=ref,
                            headers=self._session_auth_headers,
                            #allow_redirects=False
                        )
                else:
                    _LOGGER.warning(f'Unable to fetch authorization endpoint.')
                    raise SkodaException('Missing "location" header')
            except (SkodaException):
                raise
            except Exception as error:
                _LOGGER.warning('Failed to get authorization endpoint.')
                raise SkodaException(error)
            if req.status != 200:
                raise SkodaException('Fetching authorization endpoint failed')
            else:
                _LOGGER.debug('Got authorization endpoint')
            try:
                response_data = await req.text()
                responseSoup = BeautifulSoup(response_data, 'html.parser')
                mailform = dict()
                for t in responseSoup.find('form', id='emailPasswordForm').find_all('input', type='hidden'):
                    mailform[t['name']] = t['value']
                #mailform = dict([(t['name'],t['value']) for t in responseSoup.find('form', id='emailPasswordForm').find_all('input', type='hidden')])
                mailform['email'] = self._session_auth_username
                pe_url = authissuer+responseSoup.find('form', id='emailPasswordForm').get('action')
            except Exception as e:
                _LOGGER.error('Failed to extract user login form.')
                raise SkodaException(e)

            # POST email
            # https://identity.vwgroup.io/signin-service/v1/{CLIENT_ID}/login/identifier
            self._session_auth_headers['Referer'] = authorizationEndpoint
            self._session_auth_headers['Origin'] = authissuer
            req = await self._session.post(
                url = pe_url,
                headers = self._session_auth_headers,
                data = mailform
            )
            if req.status != 200:
                raise SkodaException('POST password request failed')
            try:
                response_data = await req.text()
                responseSoup = BeautifulSoup(response_data, 'html.parser')
                for t in responseSoup.find('form', id='credentialsForm').find_all('input', type='hidden'):
                    _LOGGER.debug(f'Found item: {t["name"], t["value"]}')
                pwform = dict([(t['name'],t['value']) for t in responseSoup.find('form', id='credentialsForm').find_all('input', type='hidden')])
                #pwform = dict([(t['name'],t['value']) for t in responseSoup.find('form', id='credentialsForm').find_all('input', type='hidden')])
                pwform['password'] = self._session_auth_password
                pw_url = authissuer+responseSoup.find('form', id='credentialsForm').get('action')
            except Exception as e:
                _LOGGER.error('Failed to extract password login form.')
                raise SkodaException(e)

            # POST password
            # https://identity.vwgroup.io/signin-service/v1/{CLIENT_ID}/login/authenticate
            self._session_auth_headers['Referer'] = pe_url
            self._session_auth_headers['Origin'] = authissuer
            _LOGGER.debug('Authenticating with email and password.')
            if self._session_fulldebug:
                _LOGGER.debug(f'Using login action url: "{pw_url}"')
            req = await self._session.post(
                url=pw_url,
                headers=self._session_auth_headers,
                data = pwform,
                allow_redirects=False
            )
            _LOGGER.debug('Parsing login response.')
            # Follow all redirects until we get redirected back to "our app"
            try:
                maxDepth = 10
                ref = req.headers.get('Location', None)
                while not ref.startswith(APP_URI):
                    if ref is None:
                        raise SkodaException('Login failed')
                    if 'error' in ref:
                        error = parse_qs(urlparse(ref).query).get('error', '')[0]
                        if error == 'login.error.throttled':
                            timeout = parse_qs(urlparse(ref).query).get('enableNextButtonAfterSeconds', '')[0]
                            _LOGGER.warning(f'Login failed, login is disabled for another {timeout} seconds')
                            raise SkodaAccountLockedException(f'Account is locked for another {timeout} seconds')
                        elif error == 'login.errors.password_invalid':
                            _LOGGER.warning(f'Login failed, invalid password')
                            raise SkodaAuthenticationException('Invalid credentials')
                        else:
                            _LOGGER.warning(f'Login failed: {error}')
                        raise SkodaLoginFailedException(error)
                    if 'terms-and-conditions' in ref:
                        _LOGGER.warning('You need to login to Skoda Connect online and accept the terms and conditions.')
                        raise SkodaEULAException('The terms and conditions must be accepted first at "https://www.skoda-connect.com/"')
                    if self._session_fulldebug:
                        _LOGGER.debug(f'Following redirect to "{ref}"')
                    response = await self._session.get(
                        url=ref,
                        headers=self._session_auth_headers,
                        allow_redirects=False
                    )
                    if not response.headers.get('Location', False):
                        raise SkodaAuthenticationException('User appears unauthorized')
                    ref = response.headers.get('Location', None)
                    # Set a max limit on requests to prevent forever loop
                    maxDepth -= 1
                    if maxDepth == 0:
                        raise SkodaException('Too many redirects')
            except (SkodaException, SkodaEULAException, SkodaAuthenticationException, SkodaAccountLockedException, SkodaLoginFailedException):
                raise
            except Exception as e:
                # If we get an unhandled exception it should be because we can't redirect to the APP_URI URL and thus we have our auth code
                if 'code' in ref:
                    _LOGGER.debug('Got code: %s' % ref)
                    pass
                else:
                    _LOGGER.debug(f'Exception occured while logging in.')
                    raise SkodaLoginFailedException(e)
            _LOGGER.debug('Login successful, received authorization code.')

            # Extract code and tokens
            jwt_auth_code = parse_qs(urlparse(ref).fragment).get('code')[0]
            jwt_id_token = parse_qs(urlparse(ref).fragment).get('id_token')[0]
            # Exchange Auth code and id_token for new tokens with refresh_token (so we can easier fetch new ones later)
            tokenBody = {
                'auth_code': jwt_auth_code,
                'id_token':  jwt_id_token,
                'brand': BRAND
            }
            _LOGGER.debug('Trying to fetch user identity tokens.')
            tokenURL = 'https://tokenrefreshservice.apps.emea.vwapps.io/exchangeAuthCode'
            req = await self._session.post(
                url=tokenURL,
                headers=self._session_auth_headers,
                data = tokenBody,
                allow_redirects=False
            )
            if req.status != 200:
                raise SkodaException('Token exchange failed')
            # Save tokens as "identity", theese are tokens representing the user
            self._session_tokens[client] = await req.json()
            if 'error' in self._session_tokens[client]:
                error = self._session_tokens[client].get('error', '')
                if 'error_description' in self._session_tokens[client]:
                    error_description = self._session_tokens[client].get('error_description', '')
                    raise SkodaException(f'{error} - {error_description}')
                else:
                    raise SkodaException(error)
            if self._session_fulldebug:
                for token in self._session_tokens.get(client, {}):
                    _LOGGER.debug(f'Got token {token} for client "{client}"')
            if not await self.verify_tokens(self._session_tokens[client].get('id_token', ''), client=client):
                _LOGGER.warning(f'Token for {client} could not be verified!')
            else:
                _LOGGER.debug(f'Token for {client} verified OK.')
        except (SkodaEULAException):
            _LOGGER.info('Login failed, the terms and conditions might have been updated and need to be accepted. Login to https://www.skoda-connect.com and accept the new terms before trying again')
            self._session_logged_in = False
            raise
        except (SkodaAccountLockedException):
            _LOGGER.info('Your account is locked, probably because of too many incorrect login attempts. Make sure that your account is not in use somewhere with incorrect password')
            self._session_logged_in = False
            raise
        except (SkodaAuthenticationException):
            _LOGGER.info('Invalid credentials or invalid configuration. Make sure you have entered the correct credentials')
            self._session_logged_in = False
            raise
        except (SkodaException):
            _LOGGER.error('An API error was encountered during login, try again later')
            self._session_logged_in = False
            raise
        except (TypeError):
            _LOGGER.warning(f'Login failed for {self._session_auth_username}. The server might be temporarily unavailable, try again later. If the problem persists, verify your account at https://www.skoda-connect.com')
        except Exception as error:
            _LOGGER.error(f'Login failed for {self._session_auth_username}, {error}')
            self._session_logged_in = False
            return False
        return True

    async def _getAPITokens(self):
        try:
            # Get VW Group API tokens
            # First verify that we have valid connect tokens
            try:
                if not await self.verify_tokens(self._session_tokens['connect'].get('id_token'), 'connect'):
                    _LOGGER.debug('The Connect services token is invalid')
                    raise SkodaException('Invalid connect token')
            except Exception as error:
                raise SkodaException(error)

            # https://mbboauth-1d.prd.ece.vwg-connect.com/mbbcoauth/mobile/oauth2/v1/token
            tokenBody2 =  {
                'grant_type': 'id_token',
                'token': self._session_tokens['connect']['id_token'],
                'scope': 'sc2:fal'
            }
            _LOGGER.debug('Trying to fetch api tokens.')
            req = await self._session.post(
                url='https://mbboauth-1d.prd.ece.vwg-connect.com/mbbcoauth/mobile/oauth2/v1/token',
                headers= {
                    'User-Agent': USER_AGENT,
                    'X-App-Version': XAPPVERSION,
                    'X-App-Name': XAPPNAME,
                    'X-Client-Id': XCLIENT_ID,
                },
                data = tokenBody2,
                allow_redirects=False
            )
            if req.status > 400:
                _LOGGER.debug('API token request failed.')
                raise SkodaException(f'API token request returned with status code {req.status}')
            else:
                # Save tokens as "vwg", use theese for get/posts to VW Group API
                self._session_tokens['vwg'] = await req.json()
                if 'error' in self._session_tokens['vwg']:
                    error = self._session_tokens['vwg'].get('error', '')
                    if 'error_description' in self._session_tokens['vwg']:
                        error_description = self._session_tokens['vwg'].get('error_description', '')
                        raise SkodaException(f'{error} - {error_description}')
                    else:
                        raise SkodaException(error)
                if self._session_fulldebug:
                    for token in self._session_tokens.get('vwg', {}):
                        _LOGGER.debug(f'Got token {token}')
                if not await self.verify_tokens(self._session_tokens['vwg'].get('access_token', ''), 'vwg'):
                    _LOGGER.warning('VW-Group API token could not be verified!')
                else:
                    _LOGGER.debug('VW-Group API token verified OK.')

            # Update headers for requests, defaults to using VWG token
            self._session_headers['Authorization'] = 'Bearer ' + self._session_tokens['vwg']['access_token']
        except Exception as error:
            _LOGGER.error(f'Failed to fetch VW-Group API tokens, {error}')
            self._session_logged_in = False
            return False
        return True

    async def terminate(self):
        """Log out from connect services"""
        _LOGGER.info(f'Initiating logout')
        await self.logout()

    async def logout(self):
        """Logout, revoke tokens."""
        self._session_headers.pop('Authorization', None)

        if self._session_logged_in:
            if self._session_headers.get('vwg', {}).get('access_token'):
                _LOGGER.info('Revoking API Access Token...')
                self._session_headers['token_type_hint'] = 'access_token'
                params = {"token": self._session_tokens['vwg']['access_token']}
                revoke_at = await self.post('https://mbboauth-1d.prd.ece.vwg-connect.com/mbbcoauth/mobile/oauth2/v1/revoke', data = params)
            if self._session_headers.get('vwg', {}).get('refresh_token'):
                _LOGGER.info('Revoking API Refresh Token...')
                self._session_headers['token_type_hint'] = 'refresh_token'
                params = {"token": self._session_tokens['vwg']['refresh_token']}
                revoke_rt = await self.post('https://mbboauth-1d.prd.ece.vwg-connect.com/mbbcoauth/mobile/oauth2/v1/revoke', data = params)
                self._session_headers.pop('token_type_hint', None)
            if self._session_headers.get('connect', {}).get('identity_token'):
                _LOGGER.info('Revoking Identity Access Token...')
                #params = {
                #    "token": self._session_tokens['identity']['access_token'],
                #    "brand": BRAND
                #}
                #revoke_at = await self.post('https://tokenrefreshservice.apps.emea.vwapps.io/revokeToken', data = params)
            if self._session_headers.get('connect', {}).get('refresh_token'):
                _LOGGER.info('Revoking Identity Refresh Token...')
                params = {
                    "token": self._session_tokens['connect']['refresh_token'],
                    "brand": BRAND
                }
                revoke_rt = await self.post('https://tokenrefreshservice.apps.emea.vwapps.io/revokeToken', data = params)

  # HTTP methods to API
    async def _request(self, method, url, **kwargs):
        """Perform a query to the VW-Group API"""
        _LOGGER.debug(f'HTTP {method} "{url}"')
        async with self._session.request(
            method,
            url,
            headers=self._session_headers,
            timeout=ClientTimeout(total=TIMEOUT.seconds),
            cookies=self._jarCookie,
            raise_for_status=False,
            **kwargs
        ) as response:
            response.raise_for_status()

            # Update cookie jar
            if self._jarCookie != '':
                self._jarCookie.update(response.cookies)
            else:
                self._jarCookie = response.cookies

            try:
                if response.status == 204:
                    res = {'status_code': response.status}
                elif response.status >= 200 or response.status <= 300:
                    res = await response.json(loads=json_loads)
                else:
                    res = {}
                    _LOGGER.debug(f'Not success status code [{response.status}] response: {response}')
                if 'X-RateLimit-Remaining' in response.headers:
                    res['rate_limit_remaining'] = response.headers.get('X-RateLimit-Remaining', '')
            except:
                res = {}
                _LOGGER.debug(f'Something went wrong [{response.status}] response: {response}')
                return res

            if self._session_fulldebug:
                _LOGGER.debug(f'Request for "{url}" returned with status code [{response.status}], response: {res}')
            else:
                _LOGGER.debug(f'Request for "{url}" returned with status code [{response.status}]')
            return res

    async def get(self, url, vin=''):
        """Perform a get query."""
        try:
            response = await self._request(METH_GET, self._make_url(url, vin))
            return response
        except aiohttp.client_exceptions.ClientResponseError as error:
            if error.status == 401:
                _LOGGER.warning(f'Received "unauthorized" error while fetching data: {error}')
                self._session_logged_in = False
            elif error.status == 400:
                _LOGGER.error(f'Got HTTP 400 {error}"Bad Request" from server, this request might be malformed or not implemented correctly for this vehicle')
            elif error.status == 500:
                _LOGGER.info('Got HTTP 500 from server, service might be temporarily unavailable')
            elif error.status == 502:
                _LOGGER.info('Got HTTP 502 from server, this request might not be supported for this vehicle')
            else:
                _LOGGER.error(f'Got unhandled error from server: {error.status}')
            return {'status_code': error.status}

    async def post(self, url, vin='', **data):
        """Perform a post query."""
        if data:
            return await self._request(METH_POST, self._make_url(url, vin), **data)
        else:
            return await self._request(METH_POST, self._make_url(url, vin))

  # Construct URL from request, home region and variables
    def _make_url(self, ref, vin=''):
        replacedUrl = re.sub('\$vin', vin, ref)
        if ('://' in replacedUrl):
            #already server contained in URL
            return replacedUrl
        elif 'rolesrights' in replacedUrl:
            return urljoin(self._session_spin_ref_url, replacedUrl)
        else:
            return urljoin(self._session_auth_ref_url, replacedUrl)

  # Update data for all Vehicles
    async def update(self):
        """Update status."""
        if self.logged_in == False:
            _LOGGER.debug("Connection was logged out. Initialising login.")
            if not await self._login():
                _LOGGER.warning(f'Login for {BRAND} account failed!')
                return False
        try:
            if not await self.validate_tokens:
                _LOGGER.info(f'Session expired. Initiating new login for {BRAND} account.')
                if not await self.doLogin():
                    _LOGGER.warning(f'Login for {BRAND} account failed!')
                    raise SkodaLoginFailedException(f'Login for {BRAND} account failed')

            _LOGGER.debug('Going to call vehicle updates')
            # Get all Vehicle objects and update in parallell
            updatelist = []
            for vehicle in self.vehicles:
                _LOGGER.debug(f'Adding {vehicle.vin} for data refresh')
                updatelist.append(vehicle.update())
            # Wait for all data updates to complete
            _LOGGER.debug('Calling update function for all vehicles')
            await asyncio.gather(*updatelist)

            return True
        except (IOError, OSError, LookupError, Exception) as error:
            _LOGGER.warning(f'Could not update information: {error}')
        return False

 #### Data collect functions ####
    async def getHomeRegion(self, vin):
        """Get API requests base url for VIN."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get('https://mal-1a.prd.ece.vwg-connect.com/api/cs/vds/v1/vehicles/$vin/homeRegion', vin)
            self._session_auth_ref_url = response['homeRegion']['baseUri']['content'].split('/api')[0].replace('mal-', 'fal-') if response['homeRegion']['baseUri']['content'] != 'https://mal-1a.prd.ece.vwg-connect.com/api' else 'https://msg.volkswagen.de'
            self._session_spin_ref_url = response['homeRegion']['baseUri']['content'].split('/api')[0]
            return response['homeRegion']['baseUri']['content']
        except Exception as error:
            _LOGGER.debug(f'Could not get homeregion, error {error}')
            self._session_logged_in = False
        return False

    async def getOperationList(self, vin):
        """Collect operationlist for VIN, supported/licensed functions."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get('/api/rolesrights/operationlist/v3/vehicles/$vin', vin)
            if response.get('operationList', False):
                data = response.get('operationList', {})
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch operation list, HTTP status code: {response.get("status_code")}')
                data = response
            else:
                _LOGGER.info(f'Could not fetch operation list: {response}')
                data = {'error': 'unknown'}
        except Exception as error:
            _LOGGER.warning(f'Could not fetch operation list, error: {error}')
            data = {'error': 'unknown'}
        return data

    async def getRealCarData(self):
        """Get car information from customer profile, VIN, nickname, etc."""
        if not await self.validate_tokens:
            return False
        try:
            _LOGGER.debug("Attempting extraction of subject from identity token.")
            atoken = self._session_tokens['connect']['access_token']
            subject = jwt.decode(atoken, verify=False).get('sub', None)
            await self.set_token('connect')
            response = await self.get(
                f'https://customer-profile.apps.emea.vwapps.io/v2/customers/{subject}/realCarData'
            )
            if response.get('realCars', {}):
                data = {
                    'realCars': response.get('realCars', {})
                }
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch realCarData, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch realcar data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch realCarData, error: {error}')
        return False

    async def getVehicleStatusReport(self, vin):
        """Get stored vehicle status report (Connect services)."""
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/vsr/v1/{BRAND}/{COUNTRY}/vehicles/$vin/status',
                vin = vin
            )
            if response.get('StoredVehicleDataResponse', {}).get('vehicleData', {}).get('data', {})[0].get('field', {})[0] :
                data = {
                    'StoredVehicleDataResponse': response.get('StoredVehicleDataResponse', {}),
                    'StoredVehicleDataResponseParsed': dict([(e['id'],e if 'value' in e else '') for f in [s['field'] for s in response['StoredVehicleDataResponse']['vehicleData']['data']] for e in f])
                }
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch vehicle status report, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch status data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch StoredVehicleDataResponse, error: {error}')
        return False

    async def getVehicleStatus(self, vin):
        """Get stored vehicle status (SmartLink)."""
        try:
            await self.set_token('smartlink')
            response = await self.get(f'https://api.connect.skoda-auto.cz/api/v1/vehicle-status/{vin}')
            if response:
                data = {
                    'vehicle_status': response
                }
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch vehicle status, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch vehicle status via SmartLink')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch SmartLink vehicle status, error: {error}')
        return False

    async def getTripStatistics(self, vin):
        """Get short term trip statistics."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/tripstatistics/v1/{BRAND}/{COUNTRY}/vehicles/$vin/tripdata/shortTerm?newest',
                vin = vin
            )
            if response.get('tripData', {}):
                data = {'tripstatistics': response.get('tripData', {})}
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch trip statistics, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info(f'Unhandled error while trying to fetch trip statistics')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch trip statistics, error: {error}')
        return False

    async def getPosition(self, vin):
        """Get position data."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/cf/v1/{BRAND}/{COUNTRY}/vehicles/$vin/position',
                vin = vin
            )
            if response.get('findCarResponse', {}):
                data = {
                    'findCarResponse': response.get('findCarResponse', {}),
                    'isMoving': False
                }
                return data
            elif response.get('status_code', {}):
                if response.get('status_code', 0) == 204:
                    _LOGGER.debug(f'Seems car is moving, HTTP 204 received from position')
                    data = {
                        'isMoving': True,
                        'rate_limit_remaining': 15
                    }
                    return data
                else:
                    _LOGGER.warning(f'Could not fetch position, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch positional data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch position, error: {error}')
        return False

    async def getTimers(self, vin):
        """Get departure timers."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/departuretimer/v1/{BRAND}/{COUNTRY}/vehicles/$vin/timer',
                vin = vin
            )
            if response.get('timer', {}):
                data = {'timers': response.get('timer', {})}
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch timers, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unknown error while trying to fetch data for departure timers')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch timers, error: {error}')
        return False

    async def getClimater(self, vin):
        """Get climatisation data."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/climatisation/v1/{BRAND}/{COUNTRY}/vehicles/$vin/climater',
                vin = vin
            )
            if response.get('climater', {}):
                data = {'climater': response.get('climater', {})}
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch climatisation, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch climatisation data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch climatisation, error: {error}')
        return False

    async def getCharger(self, vin):
        """Get charger data."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/batterycharge/v1/{BRAND}/{COUNTRY}/vehicles/$vin/charger',
                vin = vin
            )
            if response.get('charger', {}):
                data = {'charger': response.get('charger', {})}
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch charger, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch charger data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch charger, error: {error}')
        return False

    async def getCharging(self, vin):
        """Get charging data (New Skoda API)."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('connect')
            response = await self.get(
                'https://api.connect.skoda-auto.cz/api/v1/charging/$vin/status',
                vin = vin
            )
            if response.get('battery', {}):
                _LOGGER.debug(f'Got vehicle data {response}')
                return response
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch charging, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch charging data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch charging, error: {error}')
        return False

    async def getPreHeater(self, vin):
        """Get parking heater data."""
        if not await self.validate_tokens:
            return False
        try:
            await self.set_token('vwg')
            response = await self.get(
                f'fs-car/bs/rs/v1/{BRAND}/{COUNTRY}/vehicles/$vin/status',
                vin = vin
            )
            if response.get('statusResponse', {}):
                data = {'heating': response.get('statusResponse', {})}
                return data
            elif response.get('status_code', {}):
                _LOGGER.warning(f'Could not fetch pre-heating, HTTP status code: {response.get("status_code")}')
            else:
                _LOGGER.info('Unhandled error while trying to fetch pre-heating data')
        except Exception as error:
            _LOGGER.warning(f'Could not fetch pre-heating, error: {error}')
        return False

    async def get_request_status(self, vin, sectionId, requestId):
        """Return status of a request ID for a given section ID."""
        if self.logged_in == False:
            if not await self.doLogin():
                _LOGGER.warning(f'Login for {BRAND} account failed!')
                raise SkodaLoginFailedException(f'Login for {BRAND} account failed')
        try:
            if not await self.validate_tokens:
                _LOGGER.info(f'Session expired. Initiating new login for {BRAND} account.')
                if not await self.doLogin():
                    _LOGGER.warning(f'Login for {BRAND} account failed!')
                    raise SkodaLoginFailedException(f'Login for {BRAND} account failed')
            await self.set_token('vwg')
            if sectionId == 'climatisation':
                url = f'fs-car/bs/$sectionId/v1/{BRAND}/{COUNTRY}/vehicles/$vin/climater/actions/$requestId'
            elif sectionId == 'batterycharge':
                url = f'fs-car/bs/$sectionId/v1/{BRAND}/{COUNTRY}/vehicles/$vin/charger/actions/$requestId'
            elif sectionId == 'departuretimer':
                url = f'fs-car/bs/$sectionId/v1/{BRAND}/{COUNTRY}/vehicles/$vin/timer/actions/$requestId'
            elif sectionId == 'vsr':
                url = f'fs-car/bs/$sectionId/v1/{BRAND}/{COUNTRY}/vehicles/$vin/requests/$requestId/jobstatus'
            else:
                url = f'fs-car/bs/$sectionId/v1/{BRAND}/{COUNTRY}/vehicles/$vin/requests/$requestId/status'
            url = re.sub('\$sectionId', sectionId, url)
            url = re.sub('\$requestId', requestId, url)

            response = await self.get(url, vin)
            # Pre-heater, ???
            if response.get('requestStatusResponse', {}).get('status', False):
                result = response.get('requestStatusResponse', {}).get('status', False)
            # For electric charging, climatisation and departure timers
            elif response.get('action', {}).get('actionState', False):
                result = response.get('action', {}).get('actionState', False)
            else:
                result = 'Unknown'
            # Translate status messages to meaningful info
            if result == 'request_in_progress' or result == 'queued' or result == 'fetched':
                status = 'In progress'
            elif result == 'request_fail' or result == 'failed':
                status = 'Failed'
            elif result == 'unfetched':
                status = 'No response'
            elif result == 'request_successful' or result == 'succeeded':
                status = 'Success'
            else:
                status = result
            return status
        except Exception as error:
            _LOGGER.warning(f'Failure during get request status: {error}')
            raise SkodaException(f'Failure during get request status: {error}')

    async def get_sec_token(self, vin, spin, action):
        """Get a security token, required for certain set functions."""
        urls = {
            'lock':    '/api/rolesrights/authorization/v2/vehicles/$vin/services/rlu_v1/operations/LOCK/security-pin-auth-requested',
            'unlock':  '/api/rolesrights/authorization/v2/vehicles/$vin/services/rlu_v1/operations/UNLOCK/security-pin-auth-requested',
            'heating': '/api/rolesrights/authorization/v2/vehicles/$vin/services/rheating_v1/operations/P_QSACT/security-pin-auth-requested',
            'timer':   '/api/rolesrights/authorization/v2/vehicles/$vin/services/timerprogramming_v1/operations/P_SETTINGS_AU/security-pin-auth-requested',
            'rclima':  '/api/rolesrights/authorization/v2/vehicles/$vin/services/rclima_v1/operations/P_START_CLIMA_AU/security-pin-auth-requested'
        }
        if not spin:
            raise SkodaConfigException('SPIN is required')
        try:
            if not urls.get(action, False):
                raise SkodaException(f'Security token for "{action}" is not implemented')
            response = await self.get(self._make_url(urls.get(action), vin = vin))
            secToken = response['securityPinAuthInfo']['securityToken']
            challenge = response['securityPinAuthInfo']['securityPinTransmission']['challenge']
            spinHash = self.hash_spin(challenge, spin)
            body = {
                'securityPinAuthentication': {
                    'securityPin': {
                        'challenge': challenge,
                        'securityPinHash': spinHash
                    },
                    'securityToken': secToken
                }
            }
            self._session_headers['Content-Type'] = 'application/json'
            response = await self.post(self._make_url('/api/rolesrights/authorization/v2/security-pin-auth-completed', vin = vin), json = body)
            self._session_headers.pop('Content-Type', None)
            if response.get('securityToken', False):
                return response['securityToken']
            else:
                _LOGGER.warning('Did not receive a valid security token')
                raise SkodaException('Did not receive a valid security token')
        except Exception as error:
            _LOGGER.error(f'Could not generate security token (maybe wrong SPIN?), error: {error}')
            raise

 #### Data set functions ####
    async def dataCall(self, query, vin='', **data):
        """Function to execute actions through VW-Group API."""
        if self.logged_in == False:
            if not await self.doLogin():
                _LOGGER.warning(f'Login for {BRAND} account failed!')
                raise SkodaLoginFailedException(f'Login for {BRAND} account failed')
        try:
            if not await self.validate_tokens:
                _LOGGER.info(f'Session expired. Initiating new login for {BRAND} account.')
                if not await self.doLogin():
                    _LOGGER.warning(f'Login for {BRAND} account failed!')
                    raise SkodaLoginFailedException(f'Login for {BRAND} account failed')
            response = await self.post(query, vin=vin, **data)
            _LOGGER.debug(f'Data call returned: {response}')
            return response
        except aiohttp.client_exceptions.ClientResponseError as error:
            if error.status == 401:
                _LOGGER.error('Unauthorized')
                self._session_logged_in = False
            elif error.status == 400:
                _LOGGER.error(f'Bad request')
            elif error.status == 429:
                _LOGGER.warning('Too many requests. Further requests can only be made after the end of next trip in order to protect your vehicles battery.')
                return 429
            elif error.status == 500:
                _LOGGER.error('Internal server error, server might be temporarily unavailable')
            elif error.status == 502:
                _LOGGER.error('Bad gateway, this function may not be implemented for this vehicle')
            else:
                _LOGGER.error(f'Unhandled HTTP exception: {error}')
            #return False
        except Exception as error:
            _LOGGER.error(f'Failure to execute: {error}')
        return False

    async def setRefresh(self, vin):
        """"Force vehicle data update."""
        try:
            await self.set_token('vwg')
            response = await self.dataCall(f'fs-car/bs/vsr/v1/{BRAND}/{COUNTRY}/vehicles/$vin/requests', vin, data=None)
            if not response:
                raise SkodaException('Invalid or no response')
            elif response == 429:
                return dict({'id': None, 'state': 'Throttled', 'rate_limit_remaining': 0})
                raise SkodaThrottledException('Action rate limit reached. Start the car to reset the action limit')
            else:
                request_id = response.get('CurrentVehicleDataResponse', {}).get('requestId', 0)
                request_state = response.get('CurrentVehicleDataResponse', {}).get('requestState', 'queued')
                remaining = response.get('rate_limit_remaining', -1)
                _LOGGER.debug(f'Request to refresh data returned with state "{request_state}", request id: {request_id}, remaining requests: {remaining}')
                return dict({'id': str(request_id), 'state': request_state, 'rate_limit_remaining': remaining})
        except:
            raise
        return False

    async def setCharger(self, vin, data):
        """Start/Stop charger."""
        try:
            await self.set_token('vwg')
            response = await self.dataCall(f'fs-car/bs/batterycharge/v1/{BRAND}/{COUNTRY}/vehicles/$vin/charger/actions', vin, json = data)
            if not response:
                raise SkodaException('Invalid or no response')
            elif response == 429:
                return dict({'id': None, 'state': 'Throttled', 'rate_limit_remaining': 0})
            else:
                request_id = response.get('action', {}).get('actionId', 0)
                request_state = response.get('action', {}).get('actionState', 'unknown')
                remaining = response.get('rate_limit_remaining', -1)
                _LOGGER.debug(f'Request for charger action returned with state "{request_state}", request id: {request_id}, remaining requests: {remaining}')
                return dict({'id': str(request_id), 'state': request_state, 'rate_limit_remaining': remaining})
        except:
            raise
        return False

    async def setTimers(self, vin, data, spin):
        """Set departure timers."""
        try:
            # First get most recent departuretimer settings from server
            departuretimers = await self.getTimers(vin)
            timer = departuretimers.get('timers', {}).get('timersAndProfiles', {}).get('timerList', {}).get('timer', [])
            profile = departuretimers.get('timers', {}).get('timersAndProfiles', {}).get('timerProfileList', {}).get('timerProfile', [])
            setting = departuretimers.get('timers', {}).get('timersAndProfiles', {}).get('timerBasicSetting', [])

            # Construct Timer data
            timers = [{},{},{}]
            for i in range(0, 3):
                timers[i]['currentCalendarProvider'] = {}
                for key in timer[i]:
                    # Ignore the timestamp key
                    if key not in ['timestamp']:
                        timers[i][key] = timer[i][key]
                if timers[i].get('timerFrequency', '') == 'single':
                    timers[i]['departureTimeOfDay'] = '00:00'

            # Set charger minimum limit if action is chargelimit
            if data.get('action', None) == 'chargelimit' :
                actiontype = 'setChargeMinLimit'
                setting['chargeMinLimit'] = int(data.get('limit', 50))
            # Modify timers if action is on, off or schedule
            elif data.get('action', None) in ['on', 'off', 'schedule']:
                actiontype = 'setTimersAndProfiles'
                timerid = int(data.get('id'))-1 if data.get('id', False) else 0
                # Set timer programmed status if data contains action = on or off
                if data.get('action', None) in ['on', 'off']:
                    action = 'programmed' if data.get('action', False) else 'notProgrammed'
                # Set departure schedule
                elif data.get('action', None) == 'schedule':
                    action = 'programmed' if data.get('schedule', {}).get('enabled', False) else 'notProgrammed'
                    if data.get('schedule', {}).get('recurring', False):
                        timers[timerid]['timerFrequency'] = 'cyclic'
                        timers[timerid]['departureWeekdayMask'] = data.get('schedule', {}).get('days', 'nnnnnnn')
                        timers[timerid]['departureTimeOfDay'] = data.get('schedule', {}).get('time', '08:00')
                        timers[timerid].pop('departureDateTime', None)
                    else:
                        timers[timerid]['timerFrequency'] = 'single'
                        timers[timerid]['departureWeekdayMask'] = 'nnnnnnn'
                        timers[timerid]['departureTimeOfDay'] = '00:00'
                        timers[timerid]['departureDateTime'] = \
                            data.get('schedule', {}).get('date', '2020-01-01') + 'T' +\
                            data.get('schedule', {}).get('time', '08:00')
                # Catch uncatched scenario
                else:
                    action = 'notProgrammed'
                timers[timerid]['timerProgrammedStatus'] = action
            else:
                raise SkodaException('Unknown action for departure timer')

            # Construct Profiles data
            profiles = [{},{},{}]
            for i in range(0, 3):
                for key in profile[i]:
                    # Ignore the timestamp key
                    if key not in ['timestamp']:
                        profiles[i][key] = profile[i][key]

            # Construct basic settings
            settings = {
                'chargeMinLimit': int(setting['chargeMinLimit']),
                'heaterSource': 'electric',
                'targetTemperature': int(data['temp'])
            }
            body = {
                'action': {
                    'timersAndProfiles': {
                        'timerBasicSetting': settings,
                        'timerList': {
                            'timer': timers
                        },
                        'timerProfileList': {
                            'timerProfile': profiles
                        }
                    },
                    'type': actiontype
                }
            }
            _LOGGER.debug(f'POSTing the following timer data: {body}')
            await self.set_token('vwg')
            # Only get security token if auxiliary heater is to be enabled
            #if data.get... == 'auxiliary':
            #   self._session_headers['X-securityToken'] = await self.get_sec_token(vin = vin, spin = spin, action = 'timer')
            response = await self.dataCall(f'fs-car/bs/departuretimer/v1/{BRAND}/{COUNTRY}/vehicles/$vin/timer/actions', vin, json = body)
            self._session_headers.pop('X-securityToken', None)
            if not response:
                raise SkodaException('Invalid or no response')
            elif response == 429:
                return dict({'id': None, 'state': 'Throttled', 'rate_limit_remaining': 0})
            else:
                request_id = response.get('action', {}).get('actionId', 0)
                request_state = response.get('action', {}).get('actionState', 'unknown')
                remaining = response.get('rate_limit_remaining', -1)
                _LOGGER.debug(f'Request for departure timer action returned with state "{request_state}", request id: {request_id}, remaining requests: {remaining}')
                return dict({'id': str(request_id), 'state': request_state, 'rate_limit_remaining': remaining})
        except:
            self._session_headers.pop('X-securityToken', None)
            raise
        return False

    async def setClimater(self, vin, data, spin):
        """Execute climatisation actions."""
        try:
            await self.set_token('vwg')
            # Only get security token if auxiliary heater is to be started
            if data.get('action', {}).get('settings', {}).get('heaterSource', None) == 'auxiliary':
                self._session_headers['X-securityToken'] = await self.get_sec_token(vin = vin, spin = spin, action = 'rclima')
            response = await self.dataCall(f'fs-car/bs/climatisation/v1/{BRAND}/{COUNTRY}/vehicles/$vin/climater/actions', vin, json = data)
            self._session_headers.pop('X-securityToken', None)
            if not response:
                raise SkodaException('Invalid or no response')
            elif response == 429:
                return dict({'id': None, 'state': 'Throttled', 'rate_limit_remaining': 0})
            else:
                request_id = response.get('action', {}).get('actionId', 0)
                request_state = response.get('action', {}).get('actionState', 'unknown')
                remaining = response.get('rate_limit_remaining', -1)
                _LOGGER.debug(f'Request for climater action returned with state "{request_state}", request id: {request_id}, remaining requests: {remaining}')
                return dict({'id': str(request_id), 'state': request_state, 'rate_limit_remaining': remaining})
        except:
            self._session_headers.pop('X-securityToken', None)
            raise
        return False

    async def setPreHeater(self, vin, data, spin):
        """Petrol/diesel parking heater actions."""
        try:
            await self.set_token('vwg')
            if 'Content-Type' in self._session_headers:
                contType = self._session_headers['Content-Type']
            else:
                contType = ''
            self._session_headers['Content-Type'] = 'application/vnd.vwg.mbb.RemoteStandheizung_v2_0_2+json'
            if not 'quickstop' in data:
                self._session_headers['x-mbbSecToken'] = await self.get_sec_token(vin = vin, spin = spin, action = 'heating')
            response = await self.dataCall(f'fs-car/bs/rs/v1/{BRAND}/{COUNTRY}/vehicles/$vin/action', vin = vin, json = data)
            # Clean up headers
            self._session_headers.pop('x-mbbSecToken', None)
            self._session_headers.pop('Content-Type', None)
            if contType: self._session_headers['Content-Type'] = contType

            if not response:
                raise SkodaException('Invalid or no response')
            elif response == 429:
                return dict({'id': None, 'state': 'Throttled', 'rate_limit_remaining': 0})
            else:
                request_id = response.get('performActionResponse', {}).get('requestId', 0)
                remaining = response.get('rate_limit_remaining', -1)
                _LOGGER.debug(f'Request for parking heater is queued with request id: {request_id}, remaining requests: {remaining}')
                return dict({'id': str(request_id), 'state': None, 'rate_limit_remaining': remaining})
        except Exception as error:
            self._session_headers.pop('x-mbbSecToken', None)
            self._session_headers.pop('Content-Type', None)
            if contType: self._session_headers['Content-Type'] = contType
            raise
        return False

    async def setLock(self, vin, data, spin):
        """Remote lock and unlock actions."""
        try:
            await self.set_token('vwg')
            # Prepare data, headers and fetch security token
            if 'Content-Type' in self._session_headers:
                contType = self._session_headers['Content-Type']
            else:
                contType = ''
            if 'unlock' in data:
                self._session_headers['X-mbbSecToken'] = await self.get_sec_token(vin = vin, spin = spin, action = 'unlock')
            else:
                self._session_headers['X-mbbSecToken'] = await self.get_sec_token(vin = vin, spin = spin, action = 'lock')
            self._session_headers['Content-Type'] = 'application/vnd.vwg.mbb.RemoteLockUnlock_v1_0_0+xml'
            response = await self.dataCall(f'fs-car/bs/rlu/v1/{BRAND}/{COUNTRY}/vehicles/$vin/actions', vin, data = data)
            # Clean up headers
            self._session_headers.pop('X-mbbSecToken', None)
            self._session_headers.pop('Content-Type', None)
            if contType: self._session_headers['Content-Type'] = contType
            if not response:
                raise SkodaException('Invalid or no response')
            elif response == 429:
                return dict({'id': None, 'state': 'Throttled', 'rate_limit_remaining': 0})
            else:
                request_id = response.get('rluActionResponse', {}).get('requestId', 0)
                request_state = response.get('rluActionResponse', {}).get('requestId', 'unknown')
                remaining = response.get('rate_limit_remaining', -1)
                _LOGGER.debug(f'Request for lock action returned with state "{request_state}", request id: {request_id}, remaining requests: {remaining}')
                return dict({'id': str(request_id), 'state': request_state, 'rate_limit_remaining': remaining})
        except:
            self._session_headers.pop('X-mbbSecToken', None)
            self._session_headers.pop('Content-Type', None)
            if contType: self._session_headers['Content-Type'] = contType
            raise
        return False

 #### Token handling ####
    @property
    async def validate_tokens(self):
        """Function to validate expiry of tokens."""
        now = datetime.now()
        later = now + self._session_refresh_interval
        # Prepare identity token
        idtoken = self._session_tokens['connect'].get('id_token', '')
        id_exp = jwt.decode(idtoken, verify=False).get('exp', None)
        id_dt = datetime.fromtimestamp(int(id_exp))
        # Prepare Skoda token
        stoken = self._session_tokens['skoda'].get('id_token', '')
        st_exp = jwt.decode(stoken, verify=False).get('exp', None)
        st_dt = datetime.fromtimestamp(int(st_exp))
        # Prepare vwg acess token, if exists
        if self._session_tokens.get('vwg', False):
            atoken = self._session_tokens['vwg'].get('access_token', '')
            at_exp = jwt.decode(atoken, verify=False).get('exp', None)
            at_dt = datetime.fromtimestamp(int(at_exp))
        else:
            at_dt = later + self._session_refresh_interval
        # Prepare smartlink acess token, if exists
        if self._session_tokens.get('smartlink', False):
            sltoken = self._session_tokens['smartlink'].get('access_token', '')
            slt_exp = jwt.decode(sltoken, verify=False).get('exp', None)
            slt_dt = datetime.fromtimestamp(int(slt_exp))
        else:
            slt_dt = later + self._session_refresh_interval

        # Check if tokens have expired, or expires now
        if now >= id_dt or now >= st_dt or now >= at_dt or now >= slt_dt:
            _LOGGER.debug('Tokens have expired. Try to fetch new tokens.')
            if await self.refresh_tokens():
                _LOGGER.debug('Successfully refreshed tokens')
            else:
                return False
        # Check if tokens expires before next update
        elif later >= id_dt or later >= st_dt or later >= at_dt or later >= slt_dt:
            _LOGGER.debug('Tokens about to expire. Try to fetch new tokens.')
            if await self.refresh_tokens():
                _LOGGER.debug('Successfully refreshed tokens')
            else:
                return False
        return True

    async def verify_tokens(self, token, client='connect'):
        """Function to verify JWT against JWK(s)."""
        if client in ['connect', 'skoda', 'smartlink']:
            req = await self._session.get(url = 'https://identity.vwgroup.io/oidc/v1/keys')
            keys = await req.json()
            audience = [
                CLIENT[client].get('CLIENT_ID'),
                'VWGMBB01DELIV1',
                'https://api.vas.eu.dp15.vwg-connect.com',
                'https://api.vas.eu.wcardp.io'
            ]
        elif client == 'vwg':
            req = await self._session.get(url = 'https://mbboauth-1d.prd.ece.vwg-connect.com/mbbcoauth/public/jwk/v1')
            keys = await req.json()
            audience = 'mal.prd.ece.vwg-connect.com'
        else:
            _LOGGER.debug('Not implemented')
            return False
        try:
            pubkeys = {}
            for jwk in keys['keys']:
                kid = jwk['kid']
                if jwk['kty'] == 'RSA':
                    pubkeys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(to_json(jwk))

            token_kid = jwt.get_unverified_header(token)['kid']
            if client == 'vwg':
                token_kid = 'VWGMBB01DELIV1.' + token_kid

            pubkey = pubkeys[token_kid]
            _LOGGER.debug(f'Attempting to verify token for client {client}. Token: {token}, pubkey: {pubkey}, audience: {audience}')
            payload = jwt.decode(token, key=pubkey, algorithms=['RS256'], audience=audience)
            return True
        except Exception as error:
            _LOGGER.debug(f'Failed to verify {client} token, error: {error}')
            return False

    async def refresh_tokens(self):
        """Function to refresh tokens."""
        try:
            tHeaders = {
                'Accept-Encoding': 'gzip, deflate, br',
                #'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': USER_AGENT,
                #'X-App-Version': XAPPVERSION,
                #'X-App-Name': XAPPNAME,
                #'X-Client-Id': XCLIENT_ID
            }

            # Refresh Skoda API tokens
            skoda_body = {
                'grant_type': 'refresh_token',
                'brand': BRAND,
                'refresh_token': self._session_tokens['skoda']['refresh_token']
            }
            sresponse = await self._session.post(
                url = 'https://tokenrefreshservice.apps.emea.vwapps.io/refreshTokens',
                headers = tHeaders,
                data = skoda_body
            )
            if sresponse.status == 200:
                tokens = await sresponse.json()
                # Verify Token
                if not await self.verify_tokens(tokens['id_token'], 'skoda'):
                    _LOGGER.warning('Token could not be verified!')
                for token in tokens:
                    self._session_tokens['skoda'][token] = tokens[token]
            else:
                _LOGGER.warning('Something went wrong when refreshing Skoda API tokens.')
                return False

            # Refresh VW-Group identity tokens
            connect_body = {
                'grant_type': 'refresh_token',
                'brand': BRAND,
                'refresh_token': self._session_tokens['connect']['refresh_token']
            }
            cresponse = await self._session.post(
                url = 'https://tokenrefreshservice.apps.emea.vwapps.io/refreshTokens',
                headers = tHeaders,
                data = connect_body
            )
            if cresponse.status == 200:
                tokens = await cresponse.json()
                # Verify Token
                if not await self.verify_tokens(tokens['id_token'], 'connect'):
                    _LOGGER.warning('Token could not be verified!')
                for token in tokens:
                    self._session_tokens['connect'][token] = tokens[token]
            else:
                _LOGGER.warning('Something went wrong when refreshing VW-Group identity tokens.')
                return False

            # Refresh VW-Group API tokens
            if self._session_tokens.get('vwg', False):
                body = {
                    'grant_type': 'id_token',
                    'scope': 'sc2:fal',
                    'token': self._session_tokens['connect']['id_token']
                }
                response = await self._session.post(
                    url = 'https://mbboauth-1d.prd.ece.vwg-connect.com/mbbcoauth/mobile/oauth2/v1/token',
                    headers = tHeaders,
                    data = body,
                    allow_redirects=True
                )
                if response.status == 200:
                    tokens = await response.json()
                    if not await self.verify_tokens(tokens['access_token'], 'vwg'):
                        _LOGGER.warning('Token could not be verified!')
                    for token in tokens:
                        self._session_tokens['vwg'][token] = tokens[token]
                else:
                    resp = await response.text()
                    _LOGGER.warning(f'Something went wrong when refreshing VW-Group API tokens. {resp}')
                    return False

            # Refresh SmartLink tokens
            if self._session_tokens.get('smartlink', False):
                sl_body = {
                    'grant_type': 'refresh_token',
                    'brand': BRAND,
                    'refresh_token': self._session_tokens['smartlink']['refresh_token']
                }
                slresponse = await self._session.post(
                    url = 'https://tokenrefreshservice.apps.emea.vwapps.io/refreshTokens',
                    headers = tHeaders,
                    data = sl_body
                )
                if slresponse.status == 200:
                    tokens = await slresponse.json()
                    # Verify Token
                    if not await self.verify_tokens(tokens['id_token'], 'smartlink'):
                        _LOGGER.warning('Token could not be verified!')
                    for token in tokens:
                        self._session_tokens['smartlink'][token] = tokens[token]
                else:
                    _LOGGER.warning('Something went wrong when refreshing SmartLink tokens.')
                    return False

            return True
        except Exception as error:
            _LOGGER.warning(f'Could not refresh tokens: {error}')
            return False

    async def set_token(self, type):
        """Switch between tokens."""
        self._session_headers['Authorization'] = 'Bearer ' + self._session_tokens[type]['access_token']
        if type == 'skoda':
            self._session_headers['tokentype'] = 'IDK_TECHNICAL'
        elif type == 'connect':
            self._session_headers['tokentype'] = 'IDK_CONNECT'
        elif type == 'smartlink':
            self._session_headers['tokentype'] = 'IDK_SMARTLINK'
        else:
            self._session_headers['tokentype'] = 'MBB'
        return

 #### Class helpers ####
    @property
    def vehicles(self):
        """Return list of Vehicle objects."""
        return self._vehicles

    @property
    def logged_in(self):
        return self._session_logged_in

    def vehicle(self, vin):
        """Return vehicle object for given vin."""
        return next(
            (
                vehicle
                for vehicle in self.vehicles
                if vehicle.unique_id.lower() == vin.lower()
            ), None
        )

    def hash_spin(self, challenge, spin):
        """Convert SPIN and challenge to hash."""
        spinArray = bytearray.fromhex(spin);
        byteChallenge = bytearray.fromhex(challenge);
        spinArray.extend(byteChallenge)
        return hashlib.sha512(spinArray).hexdigest()

    @property
    async def validate_login(self):
        try:
            if not await self.validate_tokens:
                return False

            return True
        except (IOError, OSError) as error:
            _LOGGER.warning('Could not validate login: %s', error)
            return False


async def main():
    """Main method."""
    if '-v' in argv:
        logging.basicConfig(level=logging.INFO)
    elif '-vv' in argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    async with ClientSession(headers={'Connection': 'keep-alive'}) as session:
        connection = Connection(session, **read_config())
        if await connection.doLogin():
            if await connection.update():
                for vehicle in connection.vehicles:
                    print(f'Vehicle id: {vehicle}')
                    print('Supported sensors:')
                    for instrument in vehicle.dashboard().instruments:
                        print(f' - {instrument.name} (domain:{instrument.component}) - {instrument.str_state}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
