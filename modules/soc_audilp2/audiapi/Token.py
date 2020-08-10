import json
import os

import time


class Token:
    FILE = 'token.json'

    def __init__(self):
        self.access_token = ''
        self.token_type = ''
        self.expires_in = 0

    def valid(self):
        """
        Checks if this token is still valid

        :return: True if valid
        :rtype: bool
        """
        return self.expires_in > int(time.time())

    def persist(self):
        with open(self.FILE, 'w') as outfile:
            json.dump(self.__dict__, outfile)

    @staticmethod
    def parse(data, relative_timestamp=True):
        token = Token()
        token.access_token = data.get('access_token')
        token.token_type = data.get('token_type')
        raw_timestamp = data.get('expires_in')
        if relative_timestamp:
            raw_timestamp += int(time.time())
        token.expires_in = raw_timestamp
        return token

    def __str__(self):
        return 'Access token: ' + self.access_token

    @staticmethod
    def load():
        if not os.path.isfile(Token.FILE):
            return None

        with open(Token.FILE) as data_file:
            data = json.load(data_file)
            return Token.parse(data, relative_timestamp=False)
