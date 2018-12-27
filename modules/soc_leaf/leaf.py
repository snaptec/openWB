from auth import login
import requests

BASE_URL = 'https://gdcportalgw.its-mo.com/api_v181217_NE/gdc/'

class Leaf(object):
    """Make requests to the Nissan Connect API to get Leaf Info"""
    custom_sessionid  = None
    VIN = None

    def __init__(self, username=None, password=None, custom_sessionid=None, VIN=None):

        if username and password:
            self.custom_sessionid, self.VIN = login(username, password)
        elif custom_sessionid and VIN:
            self.custom_sessionid = custom_sessionid
            self.VIN = VIN
        else:
            raise Exception('Need either username & password or custom_sessionid & VIN.')

    def __getattr__(self, name):
        """
        Top secret magic.  Calling Leaf.<some_function_name>() hits <some_function_name>.php
        """

        if name.startswith('__'):
            raise AttributeError(name)

        def call(**kwargs):
            url = BASE_URL + name + '.php'
            data = {
                "RegionCode": 'NE',
                "custom_sessionid": self.custom_sessionid,
                "VIN": self.VIN
            }
            for k in kwargs:
                data[k] = kwargs[k]
            r = requests.post(url, data=data)
            r.raise_for_status()
            if not r.json()['status'] == 200:
            	raise Exception('Error making request.  Perhaps the session has expired.')
            return r.json()
        return call
