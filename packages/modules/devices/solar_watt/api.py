from typing import Dict


def parse_value(response: Dict, key: str) -> float:
    for item in response["result"]["items"]:
        for tag_key, tag_value in item['tagValues'].items():
            if key == tag_key:
                return tag_value["value"]
    else:
        raise ValueError("Wert " + key + " nicht in Antwort enthalten.")
