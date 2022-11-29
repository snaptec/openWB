import requests


class PowerwallHttpClient:
    def __init__(self, host: str, session: requests.Session, cookies):
        self.__base_url = "https://" + host
        self.__cookies = cookies
        self.__session = session

    def get_json(self, relative_url: str):
        url = self.__base_url + relative_url
        return self.__session.get(url, cookies=self.__cookies, verify=False, timeout=5).json()
