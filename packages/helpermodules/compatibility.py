from pathlib import Path


def is_ramdisk_in_use() -> bool:
    """ prüft, ob die Daten in der Ramdisk liegen (v1.x), sonst wird mit dem Broker (2.x) gearbeitet.
    """
    return (Path(__file__).resolve().parents[2] / "ramdisk" / "bootinprogress").is_file()
