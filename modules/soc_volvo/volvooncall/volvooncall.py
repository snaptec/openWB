#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Communicate with VOC server."""

import logging
from datetime import timedelta
from json import dumps as to_json
from collections import OrderedDict
from sys import argv
from urllib.parse import urljoin
import asyncio

from aiohttp import ClientSession, ClientTimeout, BasicAuth
from aiohttp.hdrs import METH_GET, METH_POST

from .util import (
    json_serialize,
    is_valid_path,
    find_path,
    json_loads,
    read_config,
)

__version__ = "0.8.12"

_LOGGER = logging.getLogger(__name__)

SERVICE_URL = "https://vocapi{region}.wirelesscar.net/customerapi/rest/v3.0/"
DEFAULT_SERVICE_URL = SERVICE_URL.format(region="")

HEADERS = {
    "X-Device-Id": "Device",
    "X-OS-Type": "Android",
    "X-Originator-Type": "App",
    "X-OS-Version": "22",
    "Content-Type": "application/json",
}

TIMEOUT = timedelta(seconds=30)


class Connection:

    """Connection to the VOC server."""

    def __init__(
        self, session, username, password, service_url=None, region=None, **_
    ):
        """Initialize."""
        _LOGGER.info("%s %s %s", __name__, __version__, __file__)

        self._session = session
        self._auth = BasicAuth(username, password)
        self._service_url = (
            SERVICE_URL.format(region="-" + region)
            if region
            else service_url or DEFAULT_SERVICE_URL
        )
        self._state = {}
        _LOGGER.debug("Using service <%s>", self._service_url)
        _LOGGER.debug("User: <%s>", username)

    async def _request(self, method, url, **kwargs):
        """Perform a query to the online service."""
        try:
            _LOGGER.debug("Request for %s", url)

            async with self._session.request(
                method,
                url,
                headers=HEADERS,
                auth=self._auth,
                timeout=ClientTimeout(total=TIMEOUT.seconds),
                **kwargs
            ) as response:
                response.raise_for_status()
                res = await response.json(loads=json_loads)
                _LOGGER.debug("Received %s", res)
                return res
        except Exception as error:
            _LOGGER.warning(
                "Failure when communcating with the server: %s", error
            )
            raise

    def _make_url(self, ref, rel=None):
        return urljoin(rel or self._service_url, ref)

    async def get(self, url, rel=None):
        """Perform a query to the online service."""
        return await self._request(METH_GET, self._make_url(url, rel))

    async def post(self, url, rel=None, **data):
        """Perform a query to the online service."""
        return await self._request(
            METH_POST, self._make_url(url, rel), json=data
        )

    async def update(self, journal=False, reset=False):
        """Update status."""
        try:
            _LOGGER.info("Updating")
            if not self._state or reset:
                _LOGGER.info("Querying vehicles")
                user = await self.get("customeraccounts")
                _LOGGER.debug("Account for <%s> received", user["username"])
                self._state = {}
                for vehicle in user["accountVehicleRelations"]:
                    rel = await self.get(vehicle)
                    if rel.get("status") == "Verified":
                        url = rel["vehicle"] + "/"
                        state = await self.get("attributes", rel=url)
                        self._state.update({url: state})
                    else:
                        _LOGGER.warning("vehichle not verified")
            for vehicle in self.vehicles:
                await vehicle.update(journal=journal)
            _LOGGER.debug("State: %s", self._state)
            return True
        except (IOError, OSError, LookupError) as error:
            _LOGGER.warning("Could not query server: %s", error)

    async def update_vehicle(self, vehicle, journal=False):
        url = vehicle._url
        self._state[url].update(await self.get("status", rel=url))
        self._state[url].update(await self.get("position", rel=url))
        if journal:
            self._state[url].update(await self.get("trips", rel=url))

    @property
    def vehicles(self):
        """Return vehicle state."""
        return (Vehicle(self, url) for url in self._state)

    def vehicle(self, vin):
        """Return vehicle for given vin."""
        return next(
            (
                vehicle
                for vehicle in self.vehicles
                if vehicle.unique_id == vin.lower()
            ),
            None,
        )

    def vehicle_attrs(self, vehicle_url):
        return self._state.get(vehicle_url)


class Vehicle(object):
    """Convenience wrapper around the state returned from the server."""

    def __init__(self, conn, url):
        self._connection = conn
        self._url = url

    async def update(self, journal=False):
        await self._connection.update_vehicle(self, journal)

    @property
    def attrs(self):
        return self._connection.vehicle_attrs(self._url)

    def has_attr(self, attr):
        return is_valid_path(self.attrs, attr)

    def get_attr(self, attr):
        return find_path(self.attrs, attr)

    @property
    def unique_id(self):
        return (self.registration_number or self.vin).lower()

    @property
    def position(self):
        return self.attrs.get("position")

    @property
    def registration_number(self):
        return self.attrs.get("registrationNumber")

    @property
    def vin(self):
        return self.attrs.get("vin")

    @property
    def model_year(self):
        return self.attrs.get("modelYear")

    @property
    def vehicle_type(self):
        return self.attrs.get("vehicleType")

    @property
    def odometer(self):
        return self.attrs.get("odometer")

    @property
    def fuel_amount_level(self):
        return self.attrs.get("fuelAmountLevel")

    @property
    def distance_to_empty(self):
        return self.attrs.get("distanceToEmpty")

    @property
    def is_honk_and_blink_supported(self):
        return self.attrs.get("honkAndBlinkSupported")

    @property
    def doors(self):
        return self.attrs.get("doors")

    @property
    def windows(self):
        return self.attrs.get("windows")

    @property
    def is_lock_supported(self):
        return self.attrs.get("lockSupported")

    @property
    def is_unlock_supported(self):
        return self.attrs.get("unlockSupported")

    @property
    def is_locked(self):
        return self.attrs.get("carLocked")

    @property
    def heater(self):
        return self.attrs.get("heater")

    @property
    def is_remote_heater_supported(self):
        return self.attrs.get("remoteHeaterSupported")

    @property
    def is_preclimatization_supported(self):
        return self.attrs.get("preclimatizationSupported")

    @property
    def is_journal_supported(self):
        return self.attrs.get("journalLogSupported") and self.attrs.get(
            "journalLogEnabled"
        )

    @property
    def is_engine_running(self):
        engine_remote_start_status = (
            self.attrs.get("ERS", {}).get("status") or ""
        )
        return (
            self.attrs.get("engineRunning")
            or "on" in engine_remote_start_status
        )

    @property
    def is_engine_start_supported(self):
        return self.attrs.get("engineStartSupported") and self.attrs.get("ERS")

    async def get(self, query):
        """Perform a query to the online service."""
        return await self._connection.get(query, self._url)

    async def post(self, query, **data):
        """Perform a query to the online service."""
        return await self._connection.post(query, self._url, **data)

    async def call(self, method, **data):
        """Make remote method call."""
        try:
            res = await self.post(method, **data)

            if "service" not in res or "status" not in res:
                _LOGGER.warning("Failed to execute: %s", res["status"])
                return

            if res["status"] not in ["Queued", "Started"]:
                _LOGGER.warning("Failed to execute: %s", res["status"])
                return

            # if Queued -> wait?

            service_url = res["service"]
            res = await self.get(service_url)

            if "status" not in res:
                _LOGGER.warning("Message not delivered")
                return

            # if still Queued -> wait?

            if res["status"] not in [
                "MessageDelivered",
                "Successful",
                "Started",
            ]:
                _LOGGER.warning("Message not delivered: %s", res["status"])
                return

            _LOGGER.debug("Message delivered")
            return True
        except Exception as error:
            _LOGGER.warning("Failure to execute: %s", error)

    @staticmethod
    def any_open(doors):
        """
        >>> Vehicle.any_open({'frontLeftWindowOpen': False,
        ...                   'frontRightWindowOpen': False,
        ...                   'timestamp': 'foo'})
        False

        >>> Vehicle.any_open({'frontLeftWindowOpen': True,
        ...                   'frontRightWindowOpen': False,
        ...                   'timestamp': 'foo'})
        True
        """
        return doors and any(doors[door] for door in doors if "Open" in door)

    @property
    def any_window_open(self):
        return self.any_open(self.windows)

    @property
    def any_door_open(self):
        return self.any_open(self.doors)

    @property
    def position_supported(self):
        """Return true if vehicle has position."""
        return "position" in self.attrs

    @property
    def heater_supported(self):
        """Return true if vehicle has heater."""
        return (
            self.is_remote_heater_supported
            or self.is_preclimatization_supported
        ) and "heater" in self.attrs

    @property
    def is_heater_on(self):
        """Return status of heater."""
        return (
            self.heater_supported
            and "status" in self.heater
            and self.heater["status"] != "off"
        )

    @property
    def trips(self):
        """Return trips."""
        return self.attrs.get("trips")

    async def honk_and_blink(self):
        """Honk and blink."""
        if self.is_honk_and_blink_supported:
            await self.call("honkAndBlink")

    async def lock(self):
        """Lock."""
        if self.is_lock_supported:
            await self.call("lock")
            await self.update()
        else:
            _LOGGER.warning("Lock not supported")

    async def unlock(self):
        """Unlock."""
        if self.is_unlock_supported:
            await self.call("unlock")
            await self.update()
        else:
            _LOGGER.warning("Unlock not supported")

    async def start_engine(self):
        if self.is_engine_start_supported:
            await self.call("engine/start", runtime=15)
            await self.update()
        else:
            _LOGGER.warning("Engine start not supported.")

    async def stop_engine(self):
        if self.is_engine_start_supported:
            await self.call("engine/stop")
            await self.update()
        else:
            _LOGGER.warning("Engine stop not supported.")

    async def start_heater(self):
        """Turn on/off heater."""
        if self.is_remote_heater_supported:
            await self.call("heater/start")
            await self.update()
        elif self.is_preclimatization_supported:
            await self.call("preclimatization/start")
            await self.update()
        else:
            _LOGGER.warning("No heater or preclimatization support.")

    async def stop_heater(self):
        """Turn on/off heater."""
        if self.is_remote_heater_supported:
            await self.call("heater/stop")
            await self.update()
        elif self.is_preclimatization_supported:
            await self.call("preclimatization/stop")
            await self.update()
        else:
            _LOGGER.warning("No heater or preclimatization support.")

    def __str__(self):
        return "%s (%s/%s) %s" % (
            self.registration_number or "?",
            self.vehicle_type or "?",
            self.model_year or "?",
            self.vin or "?",
        )

    def dashboard(self, **config):
        from .dashboard import Dashboard

        return Dashboard(self, **config)

    @property
    def json(self):
        """Return JSON representation."""
        return to_json(
            OrderedDict(sorted(self.attrs.items())),
            indent=4,
            default=json_serialize,
        )


async def main():
    """Main method."""
    if "-v" in argv:
        logging.basicConfig(level=logging.INFO)
    elif "-vv" in argv:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    async with ClientSession() as session:
        connection = Connection(session, **read_config())
        if await connection.update():
            for vehicle in connection.vehicles:
                print(vehicle)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run(main())
