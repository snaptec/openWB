#!/usr/bin/env python3

def get_default_config() -> dict:
    return {
        "name": "PV-Zähler an EVU-Kit",
        "type": "inverter",
        "id": 0,
        "configuration": {
            "version": 2
        }
    }
