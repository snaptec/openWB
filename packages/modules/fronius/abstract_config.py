#!/usr/bin/env python3
from enum import Enum


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
        return MeterLocation(256 if 256 <= value <= 511 else value)


class FroniusConfiguration:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address


class Fronius:
    def __init__(self, name: str, type: str, id: int, configuration: FroniusConfiguration) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration
