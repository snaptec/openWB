from pathlib import Path

RAMDSIK_PATH = Path(__file__).resolve().parents[2] / "ramdisk"


def is_ramdisk_in_use() -> bool:
    """ prüft, ob die Daten in der Ramdisk liegen (v1.x), sonst wird mit dem Broker (2.x) gearbeitet.
    """
    return (RAMDSIK_PATH / "bootinprogress").is_file()
