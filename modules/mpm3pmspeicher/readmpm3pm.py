#!/usr/bin/python
import sys
import struct
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
sdmid = int(sys.argv[2])
pvflag = str(sys.argv[3])

client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x0004,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ekwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
# resp = client.read_input_registers(0x0004,2, unit=sdmid)
# ekwh = resp.registers[1]
ekwh = float(ekwh) /100
f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
f.write(str(ekwh))
f.close()

resp = client.read_input_registers(0x0002,4, unit=5)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 
# resp = client.read_input_registers(0x0002,2, unit=sdmid)
# ikwh = resp.registers[1]
ikwh = float(ikwh) * 10
f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
f.write(str(ikwh))
f.close()

resp = client.read_input_registers(0x0E,2, unit=sdmid)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
f = open('/var/www/html/openWB/ramdisk/speichera1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=sdmid)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
f = open('/var/www/html/openWB/ramdisk/speichera2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=sdmid)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
f = open('/var/www/html/openWB/ramdisk/speichera3', 'w')
f.write(str(lla3))
f.close()

# total watt
resp = client.read_input_registers(0x26,2, unit=sdmid)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
if ( pvflag == 0 ):
    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
    f.write(str(final))
if ( pvflag == 1 ):
    pvwatt = open('/var/www/html/openWB/ramdisk/pvwatt', 'r')
    pvwatt = pvwatt.read()
    final = ( int(final) - int(pvwatt) ) * -1
    f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
    f.write(str(final))
f.close()
