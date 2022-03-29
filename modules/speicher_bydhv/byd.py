#!/usr/bin/env python3
import logging
from html.parser import HTMLParser
from typing import List, Tuple

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.common import req

log = logging.getLogger("BYD Battery")


class BydParser(HTMLParser):
    values = {"SOC:": 0, "Power:": 0}
    armed = None

    @staticmethod
    def parse(html: str):
        parser = BydParser()
        parser.feed(html)
        return parser.get_bat_state()

    def handle_starttag(self, tag, attrs: List[Tuple[str, str]]):
        if tag == "input" and self.armed is not None:
            for key, value in attrs:
                if key == "value":
                    self.values[self.armed] = value
                    break
            self.armed = None

    def handle_data(self, data: str):
        if data in self.values:
            self.armed = data

    def get_bat_state(self):
        return BatState(power=float(self.values["Power:"]) * 1000, soc=float(self.values["SOC:"][:-1]))


def update(bydhvip: str, bydhvuser: str, bydhvpass: str):
    '''BYD Speicher bieten zwei HTML-Seiten, auf denen Informationen abgegriffen werden können:
    /asp/Home.asp und /asp/RunData.asp. Aktuell (2022-03) ist die Leistungsangabe (Power) auf der
    RunData.asp auf ganze kW gerundet und somit für openWB nicht brauchbar.
    '''
    log.debug("Beginning update")
    bat_info = ComponentInfo(None, "BYD", "bat")
    with SingleComponentUpdateContext(bat_info):
        # response = req.get_http_session().get('http://' + bydhvip + '/asp/RunData.asp', auth=(bydhvuser, bydhvpass))
        response = req.get_http_session().get('http://' + bydhvip + '/asp/Home.asp', auth=(bydhvuser, bydhvpass))
        get_bat_value_store(1).set(BydParser.parse(response.text))
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
