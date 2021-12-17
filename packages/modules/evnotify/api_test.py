import pytest
import requests_mock
from requests import HTTPError

from modules.evnotify import api

EVNOTIFY_OK_RESPONSE = '{"soc_display":35,"soc_bms":34,"last_soc":1638446395}'


def test_fetch_soc_returns_soc(requests_mock: requests_mock.mock):
    # setup
    requests_mock.get("https://app.evnotify.de/soc?akey=someKey&token=someToken", text=EVNOTIFY_OK_RESPONSE)

    # execution
    actual = api.fetch_soc("someKey", "someToken")

    # evaluation
    assert actual == 35


def test_fetch_soc_throws_if_wrong_credentials(requests_mock: requests_mock.mock):
    # In case that the credentials are wrong, EVNotify will send a 401 response. In this case we expect
    # the requests.exceptions.HTTPError to be passed through

    # setup
    requests_mock.get("https://app.evnotify.de/soc?akey=someKey&token=someToken", status_code=401)

    # execution & evaluation
    with pytest.raises(HTTPError) as exception_info:
        api.fetch_soc("someKey", "someToken")
    assert exception_info.value.response.status_code == 401


def test_fetch_soc_throws_if_evnotify_returns_illegal_json(requests_mock: requests_mock.mock):
    # setup
    requests_mock.get("https://app.evnotify.de/soc?akey=someKey&token=someToken", text="invalid json")

    # execution & evaluation
    with pytest.raises(Exception, match="Expected object with numeric property <soc_display>. Got: <invalid json>"):
        api.fetch_soc("someKey", "someToken")


def test_fetch_soc_throws_if_evnotify_returns_not_a_number(requests_mock: requests_mock.mock):
    # setup
    response = EVNOTIFY_OK_RESPONSE.replace("35", '"some string"')
    requests_mock.get("https://app.evnotify.de/soc?akey=someKey&token=someToken", text=response)

    # execution & evaluation
    with pytest.raises(Exception,
                       match="Expected object with numeric property <soc_display>. Got: <{}>".format(response)):
        api.fetch_soc("someKey", "someToken")
