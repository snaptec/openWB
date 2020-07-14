#!/usr/bin/env python
""" Simple Python class to access the Tesla JSON API
https://github.com/gglockner/teslajson

The Tesla JSON API is described at:
https://tesla-api.timdorr.com/

Example:

import teslajson
c = teslajson.Connection('youremail', 'yourpassword')
v = c.vehicles[0]
v.wake_up()
v.data_request('charge_state')
v.command('charge_start')
"""

try: # Python 3
    from urllib.parse import urlencode
    from urllib.request import Request, build_opener
    from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, HTTPSHandler, HTTPError, URLError
except: # Python 2
    from urllib import urlencode
    from urllib2 import Request, build_opener
    from urllib2 import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, HTTPSHandler, HTTPError, URLError
import json
import time
import warnings


class Connection(object):
    """Connection to Tesla Motors API"""

    __version__ = "1.5.0"

    def __init__(self,
                 email='',
                 password='',
                 access_token='',
                 tokens_file='',
                 tokens_file_use = True,
                 proxy_url = '',
                 proxy_user = '',
                 proxy_password = '',
                 retries = 0,
                 retry_delay = 1.5,
                 tesla_client = None,
                 debug = False):
        """Initialize connection object

        Sets the vehicles field, a list of Vehicle objects
        associated with your account

        Required parameters:
          Option 1: (will log in and get tokens using credentials)
            email: your login for teslamotors.com
            password: your password for teslamotors.com
          Option 2: (will use tokens directly and refresh tokens as needed)
            tokens_file: File containing json tokens data, will update after refresh
          Option 3: (use use specified token until it is invalid>
            access_token

          If you combine option 1&2, it will populate the tokens file
          If you combine option 1&2 with tokens_file_use=False, it will update the tokens file


        Optional parameters:
        proxy_url: URL for proxy server
        proxy_user: username for proxy server
        proxy_password: password for proxy server
        retries: Number of times we will retry command on HTTP failure beforing failing
        retry_delay: Time in seconds we will multiplicatively back off after each failure
        debug: Turn on debugging of web traffic to tesla (non-proxy case)
        """

        self.tries = retries + 1
        self.retry_delay = retry_delay
        self.proxy_url = proxy_url
        self.proxy_user = proxy_user
        self.proxy_password = proxy_password
        self.debug = debug
        self.debuglevel = 1 if debug else 0
        self.head = {}
        self.tokens_file = tokens_file
        self.tokens_file_use = tokens_file_use
        self.access_token = access_token
        self.refresh_token = None

        # Obtain URL and program access tokens from pastebin if not on CLI
        if not tesla_client:
            #from tesla_client import Tesla_Client
            #tesla_client = Tesla_Client.base_info
            tesla_client = self.__open("/raw/0a8e0xTJ", baseurl="http://pastebin.com")

        self.current_client = tesla_client['v1']

        # Validate that returned URL is going to tesla, to prevent MITM attack
        self.baseurl = self.current_client['baseurl']
        prefix='https://'
        if not self.baseurl.startswith(prefix) or '/' in self.baseurl[len(prefix):] or not self.baseurl.endswith(('.teslamotors.com','.tesla.com')):
            raise IOError("Unexpected URL (%s) from pastebin" % self.baseurl)

        # Prefix for API queries
        self.api = self.current_client['api']

        if access_token:
            self._sethead(access_token)
        else:
            self.expiration = 0 # force refresh

            self.oauth = {
                "grant_type" : "password",
                "client_id" : self.current_client['id'],
                "client_secret" : self.current_client['secret'],
                "email" : email,
                "password" : password }

        if self.tokens_file and self.tokens_file_use:
            try:
                with open(self.tokens_file, "r") as R:
                    self._update_tokens(stream=R)
            except IOError as e:
                warnings.warn("Could not open file %s: %s (pressing on in hopes of alternate authenticaiton)"%(self.tokens_file, str(e)))

        self.vehicles = [Vehicle(v, self) for v in sorted(self.get('vehicles')['response'], key=lambda d: d['id'])]



    def get(self, command):
        """Utility command to get data from API"""
        return self.post(command, None)



    def post(self, command, data={}):
        """Utility command to post data to API"""
        if time.time() > self.expiration:
            self._refresh_token()
        return self.__open("%s%s" % (self.api, command), headers=self.head, data=data)



    def _user_agent(self):
        """Set the user agent"""
        if not "User-Agent" in self.head:
            self.head["User-Agent"] = 'teslajson.py ' + self.__version__



    def _sethead(self, access_token, expiration=float('inf')):
        """Set HTTP header"""
        self.access_token = access_token
        self.expiration = expiration
        self.head = {"Authorization": "Bearer %s" % access_token}



    def _update_tokens(self, tokens=None, stream=None):
        """Update tokens from dict or json stream"""

        if stream:
            tokens = json.load(stream)

        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        self.expiration = tokens["created_at"] + tokens["expires_in"] - 86400

        self._sethead(self.access_token, expiration=self.expiration)



    def _refresh_token(self):
        """Refresh tokens using either (preset) email/password or refresh_token"""

        print("# Try to refresh tokens at %s"%str(time.time()))

        if self.refresh_token:
            self.oauth = {
                "grant_type" : "refresh_token",
                "client_id" : self.current_client['id'],
                "client_secret" : self.current_client['secret'],
                "refresh_token" : self.refresh_token }

        self.head = {}
        tokens = self.__open("/oauth/token", data=self.oauth)
        self._update_tokens(tokens=tokens)
        if self.tokens_file:
            print("# Updating tokens to %s"%str(tokens))
            with open(self.tokens_file, "w") as W:
                W.write(json.dumps(tokens))



    def __open(self, url, headers={}, data=None, baseurl=""):
        """Raw urlopen command"""

        if not baseurl:
            baseurl = self.baseurl
        self._user_agent()


        last_except = Exception
        for count in range(self.tries):
            try:
                req = Request("%s%s" % (baseurl, url), headers=headers)
                try:
                    req.data = urlencode(data).encode('utf-8') # Python 3
                except:
                    try:
                        req.add_data(urlencode(data)) # Python 2
                    except:
                        pass

                # Proxy support
                if self.proxy_url:
                    if self.proxy_user:
                        proxy = ProxyHandler({'https': 'https://%s:%s@%s' % (self.proxy_user,
                                                                             self.proxy_password,
                                                                             self.proxy_url)})
                        auth = HTTPBasicAuthHandler()
                        opener = build_opener(proxy, auth, HTTPHandler)
                    else:
                        handler = ProxyHandler({'https': self.proxy_url})
                        opener = build_opener(handler)
                else:
                    opener = build_opener(HTTPSHandler(debuglevel=self.debuglevel))

                resp = opener.open(req)
                charset = resp.info().get('charset', 'utf-8')
                break
            except (HTTPError, URLError) as e:
                last_except = e
                if self.debug:
                    print('# %d Timed out or other error for %s: %s\n'%(time.time(),type,str(e)))
                count += 1
                if count != self.tries:
                    time.sleep(count * self.retry_delay)
        else:
            raise last_except

        return json.loads(resp.read().decode(charset))




class Vehicle(dict):
    """Vehicle class, subclassed from dictionary.

    There are 3 primary methods: wake_up, data/data_request and
    command.  data_request and command both require a name to specify
    the data or command, respectively.  data gets everything. These
    names can be found in the Tesla JSON API.

    """


    def __init__(self, data, connection):
        """Initialize vehicle class

        Called automatically by the Connection class
        """
        super(Vehicle, self).__init__(data)
        self.connection = connection



    def data_all(self):
        """Get all vehicle data"""
        result = self.get('data')
        return result['response']



    def data_request(self, name):
        """Get vehicle data"""
        if name:
            result = self.get('data_request/%s' % name)
        else:
            result = self.get(name)
        return result['response']



    def wake_up(self):
        """Wake the vehicle"""
        return self.post('wake_up')



    def command(self, name, data={}):
        """Run the command for the vehicle"""
        return self.post('command/%s' % name, data)



    def get(self, command):
        """Utility command to get data from API"""
        if command:
            return self.connection.get('vehicles/%i/%s' % (self['id'], command))
        else:
            return self.connection.get('vehicles/%i' % (self['id']))



    def post(self, command, data={}):
        """Utility command to post data to API"""
        return self.connection.post('vehicles/%i/%s' % (self['id'], command), data)



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(epilog="""Example of commands and arguments
vehicles	# Get vehicle information (default command)
get		# Get basic car data
get data	# Get all data
    charge_state, climate_state, drive_state, gui_settings, vehicle_state, mobile_enabled
do wake_up, honk_horn, flash_lights, remote_state_drive ...
do speed_limit_set_limit limit_mph=65
...""")

    parser.add_argument('--email', default=None, help='Tesla email for authentication option 1')
    parser.add_argument('--password', default=None, help='Tesla password for authentication option 1')
    parser.add_argument('--tokens_file', default=None, help='File containing access token json for tesla service, authentication option 2')
    parser.add_argument('--tokens_file_use', default=True, action='store_false', help='Do not actually log in via tokens file, update only')
    parser.add_argument('--access_token', default=None, help='Access token for tesla service, authentication option 3')
    parser.add_argument('--proxy_url', default=None, help='URL for optional web proxy')
    parser.add_argument('--proxy_user', default=None, help='Username for optional web proxy')
    parser.add_argument('--proxy_password', default=None, help='Password for optional web proxy')
    parser.add_argument('--retries', default=0, type=int, help='Number of retries on failure')
    parser.add_argument('--retry_delay', default=1.5, type=float, help='Multiplicative backup on failure')
    parser.add_argument('--tesla_client', default=None, help='Override API retrevial from pastebin')
    parser.add_argument('--debug', default=False, action='store_true', help='Example debugging')
    parser.add_argument('--vid', default=None, help='Vehicle to operate on')
    parser.add_argument('--json', default=False, action='store_true', help='Output as Json object')

    parser.add_argument('command', default='vehicles', nargs='?', help='Command for program (get, do)')
    parser.add_argument('args', nargs='*', help='Command specific arguments')
    args = parser.parse_args()

    if not args.command:
        args.command = "vehicles"

    if args.command not in ('vehicles', 'get', 'do'):
        raise ValueError('Invalidate command')

    c = Connection(email=args.email, password=args.password, access_token=args.access_token, tokens_file=args.tokens_file, tokens_file_use=args.tokens_file_use, proxy_url=args.proxy_url, proxy_user=args.proxy_user, proxy_password=args.proxy_password, retries=args.retries, retry_delay=args.retry_delay, debug=args.debug)

    if args.vid is not None:
        try:
            vnum = int(args.vid)
            c.vehicles = [c.vehicles[vnum]]
        except:
            c.vehicles = filter(lambda v: v['id'] == args.vid, c.vehicles)

    if len(c.vehicles) < 1:
        raise ValueError('Invalid vehicle number or id')

    for v in c.vehicles:
        if args.command == "vehicles":
            print(v["id"])
        elif args.command == "get":
            if not args.args:
                result = v.data_request(None)
            elif args.args[0] == "data" or args.args[0] == "vehicle_data" or args.args[0] == "mobile_enabled":
                result = v.get(args.args[0])
            else:
                result = v.data_request(args.args[0])
            if args.json == True:
                print(json.dumps(result))
            else:
                print(str(result))
        elif args.command == "do":
            command = args.args[0]
            data = dict([kv.split('=',1) for kv in args.args[1:]])
            if command == "wake_up":
                result = v.wake_up()
            else:
                result = v.command(command, data)
            if args.json == True:
                print(json.dumps(result))
            else:
                print(str(result))
        else:
            raise ValueError("Unknown command %s"%args.command)