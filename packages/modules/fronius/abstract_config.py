#!/usr/bin/env python3
from enum import Enum
from typing import Dict


class MeterLocation(Enum):
    # 0...grid interconnection point (primary meter)
    grid = 0
    # 1...load (primary meter)
    load = 1
    # 3...external generator (secondary meters)(multiple)
    external = 3
    # 256-511 subloads (secondary meters)(unique)
    subload = 256

    @classmethod
    def get(self, value):
        return MeterLocation(256 if value >= 256 and value <= 511 else value)


class FroniusConfiguration:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["ip_address"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return FroniusConfiguration(*values)


class Fronius:
    def __init__(self, name: str, type: str, id: int, configuration: FroniusConfiguration) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["name", "type", "id", "configuration"]
        try:
            values = [device_config[key] for key in keys]
            values = []
            for key in keys:
                if isinstance(device_config[key], Dict):
                    values.append(FroniusConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return Fronius(*values)
