import logging
import socket

log = logging.getLogger(__name__)

# OpenWB-Modul für die Anbindung von SolarView über den integrierten TCP-Server
# Details zur API: https://solarview.info/solarview-fb_Installieren.pdf
# Sende-Kommando (siehe SolarView-Dokumentation); Beispiele:
# '00*': Gesamte Anlage
# '01*': Wechselrichter 1
# '02*': Wechselrichter 2
#
# Format:   {WR,Tag,Monat,Jahr,Stunde,Minute,KDY,KMT,KYR,KT0,PAC,UDC,IDC,UDCB,IDCB,UDCC,IDCC,UDCD,IDCD,UL1,IL1,UL2,IL2,UL3,IL3,TKK},Checksum     # noqa: E501
# Beispiel: {01,09,09,2019,08,18,0000.0,00082,002617,00018691,00104,451,000.2,000,000.0,000,000.0,000,000.0,226,000.4,000,000.0,000,000.0,00},▒  # noqa: E501
#
# Bedeutung (siehe SolarView-Dokumentation):
#  KDY= Tagesertrag (kWh)
#  KMT= Monatsertrag (kWh)
#  KYR= Jahresertrag (kWh)
#  KT0= Gesamtertrag (kWh)
#  PAC= Generatorleistung in W
#  UDC, UDCB, UDCC, UDCD= Generator-Spannungen in Volt pro MPP-Tracker
#  IDC, IDCB, IDCC, IDCD= Generator-Ströme in Ampere pro MPP-Tracker
#  UL1, IL1= Netzspannung, Netzstrom Phase 1
#  UL2, IL2= Netzspannung, Netzstrom Phase 2
#  UL3, IL3= Netzspannung, Netzstrom Phase 3
#  TKK= Temperatur Wechselrichter


def request(ip_address: str, port: int, timeout: int, command: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect((ip_address, port))
        s.sendall(command.encode("ascii"))
        response = s.recv(1024).rstrip(b'\r\n')
        message = response[:-2]
        checksum = int.from_bytes(response[-1:], "big", signed=False)
        calculated_checksum = int(sum(message)) % 256
        log.debug("message: " + str(message))
        log.debug("checksum: " + str(checksum) + " calculated: " + str(calculated_checksum))
        if checksum != calculated_checksum:
            log.error("checksum failure: " + str(checksum) + " != " + str(calculated_checksum))
    return message.decode("ascii")[1:-1].split(",")
