#!/usr/bin/python

#
# Functions, definitions and classes to access RCT POWER
# Implementation based on RCT Power Serial Communication Protocol (doc version 1.13)
#

import sys
import getopt
import socket
import select
import struct
import binascii
import time
import operator

class rct_id():
    # data types
    t_unknown = 0
    t_bool = 1
    t_uint8 = 2
    t_int8 = 3
    t_uint16 = 4
    t_int16 = 5
    t_uint32 = 6
    t_int32 = 7
    t_enum = 8
    t_float = 9
    t_string = 10
    
    def __init__(self, msgid, idx, name, data_type, desc=''):
        self.id = msgid
        self.idx = idx
        self.data_type = data_type
        self.name = name
        self.desc = desc
        
    def get_idx(entry):
        return entry.idx
        
    def get_id(entry):
        return entry.id
        
    def get_name(entry):
        return entry.name
        

# local variables
id_tab = []
bVerbose = False
host = 'localhost'
port = 8899
receive_timeout = 2.0
search_id = 0
search_name = None

def sort_by_id():
    id_tab.sort(key=operator.attrgetter('id'))

def sort_by_name():
    id_tab.sort(key=operator.attrgetter('name'))

# find a table entry by using the 32 bit ID
def find_by_id(id):
    for l in id_tab:
        if l.id == id:
            return l
    
    return None

# find a table entry by using the 32 bit ID and return the data type
def get_type_by_id(id):
    obj = find_by_id(id)
    if obj is None:
        return rct_id.t_unknown
    
    return obj.data_type
    

# decode a value according to the id data type
def decode_value(id, data):
    try:
        data_type = get_type_by_id(id)
        if data_type == rct_id.t_bool:
            value = struct.unpack(">B", data)[0]
            if value != 0:
                return True
            else:
                return False
        elif data_type == rct_id.t_uint8:
            return struct.unpack(">B", data)[0]
        elif data_type == rct_id.t_int8:
            return struct.unpack(">b", data)[0]
        elif data_type == rct_id.t_uint16:
            return struct.unpack(">H", data)[0]
        elif data_type == rct_id.t_int16:
            return struct.unpack(">h", data)[0]
        elif data_type == rct_id.t_uint32:
            return struct.unpack(">I", data)[0]
        elif data_type == rct_id.t_int32:
            return struct.unpack(">i", data)[0]
        elif data_type == rct_id.t_enum:
            return struct.unpack(">H", data)[0]
        elif data_type == rct_id.t_float:
            return struct.unpack(">f", data)[0]
        elif data_type == rct_id.t_string:
            return hexdump(data, 512)
        else:
            return 0
    except:
        return 0

# encode a value according to the id data type
def encode_value(id, value):
    data_type = get_type_by_id(id)
    return encode_by_type(data_type)


# encode a value according to the id data type
def encode_by_type(data_type, value):
    if data_type == rct_id.t_bool:
        if value != 0:
            value = True
        else:
            value = False
        return struct.pack(">B", value)
    elif data_type == rct_id.t_uint8:
        value = struct.unpack('<B', struct.pack('<b', value))[0]
        return struct.pack(">B", value)
    elif data_type == rct_id.t_int8:
        return struct.pack(">b", value)
    elif data_type == rct_id.t_uint16:
        value = struct.unpack('<H', struct.pack('<h', value))[0]
        return struct.pack(">H", value)
    elif data_type == rct_id.t_int16:
        return struct.pack(">h", value)
    elif data_type == rct_id.t_uint32:
        value = struct.unpack('<I', struct.pack('<i', value))[0]
        return struct.pack(">I", value)
    elif data_type == rct_id.t_int32:
        return struct.pack(">i", value)
    elif data_type == rct_id.t_enum:
        value = struct.unpack('<H', struct.pack('<h', value))[0]
        return struct.pack(">H", value)
    elif data_type == rct_id.t_float:
        return struct.pack(">f", value)
    elif data_type == rct_id.t_string:
        return bytes(value)
        # return struct.pack("s", value)
    else:
        return None


########################################## FRAME
start_token = '+'
escape_token = '-'

# commands
cmd_read = 0x01
cmd_write = 0x02
cmd_long_write = 0x03
cmd_response = 0x05
cmd_long_response = 0x06
cmd_extension = 0x3C

HEADER_WITH_LENGTH = 1 + 1 + 2      # frame length for header, command and 2 byte length
FRAME_TYPE_STANDARD = 4             # standard frame with id
FRAME_TYPE_PLANT = 8                # plant frame with id and address
FRAME_CRC16_LENGTH = 2              # nr of bytes for CRC16 field


# frame class
default_frame_type=FRAME_TYPE_STANDARD
class Frame:
    def __init__(self, frame_type=default_frame_type):
        self.FrameComplete = False
        self.CRCOk = False
        self.command = 0
        self.address = 0        # for plant communication only
        self.id = 0
        self.data = ''
        self.stream = ''
        self.frame_type = frame_type
        self.bEscapeMode = False
        self.EscapeCount = 0


    # consume a data fragment until frame is complete
    # The function returns the number of consumed bytes in data
    def consume(self, data):
        i = 0;
        for c in data:
            i += 1
            
            # sync to start_token
            if len(self.stream) == 0:
                if c == start_token:
                    self.stream += c
                continue
                
            if self.bEscapeMode:
                self.bEscapeMode = False
            else:
                if c == escape_token:
                    self.bEscapeMode = True                  # escape mode -> set mode and don't add byte
                    self.EscapeCount += 1                    # just for debugging
                    continue

            # add byte to receive stream
            self.stream += c
            
            # when minimum frame size is received, decode the length and check completness of frame
            if len(self.stream) >= HEADER_WITH_LENGTH:
                if len(self.stream) == HEADER_WITH_LENGTH:
                    cmd = struct.unpack("B", self.stream[1])[0]
                    if cmd == cmd_long_response or cmd == cmd_long_write:
                        self.FrameLength = struct.unpack(">H", self.stream[2:4])[0] + 2     # 2 byte length MSBF
                    else:
                        self.FrameLength = struct.unpack(">B", self.stream[2])[0] + 1       # 1 byte length
                        
                    self.FrameLength += 2                                                   # 2 bytes header
                else:
                    if len(self.stream) == self.FrameLength + FRAME_CRC16_LENGTH:
                        self.FrameComplete = True
                        self.decode()
                        return i
        return i
    
    
    # decode a stream and store the values in the frame
    def decode(self):
        crc16_pos = len(self.stream)-2
        self.crc16 = struct.unpack(">H", self.stream[crc16_pos:crc16_pos+2])[0]
        if self.crc16 == self.CRC16(self.stream[1:crc16_pos]):
            self.CRCOk = True
            self.command = struct.unpack(">B", self.stream[1])[0]
            if self.command == cmd_long_response or self.command == cmd_long_write:
                data_length = struct.unpack(">H", self.stream[2:4])[0] # 2 byte length MSBF
                idx = 4
            else:
                data_length = struct.unpack(">B", self.stream[2])[0]   # 1 byte length
                idx = 3
    
            data_length -= self.frame_type                             # substract frame type specific length
    
            self.id = struct.unpack(">I", self.stream[idx:idx+4])[0]
            self.id_obj = find_by_id(self.id)
            idx += 4
            if self.frame_type == FRAME_TYPE_PLANT:
                self.address = struct.unpack(">I", self.stream[idx:idx+4])[0]
                idx += 4
            self.data = self.stream[idx:idx+data_length]
            self.data_dump = binascii.hexlify(self.data)                # just for debugging
            idx += data_length

            # decode data using id and id data type
            if data_length > 0 and (self.command == cmd_response or self.command == cmd_long_response or self.command == cmd_write or self.command == cmd_long_write):
                self.value = decode_value(self.id, self.data) 
        
    # encode a transmit stream using the frame values    
    def encode(self):
        self.id_obj = find_by_id(self.id)

        # build a byte stream
        buf = b""
        buf += struct.pack('B', self.command)
        
        if self.command == cmd_long_write or self.command == cmd_long_response:
            buf += struct.pack('>H', self.frame_type+len(self.data))  # 2 bytes
        else:
            buf += struct.pack('>B', self.frame_type+len(self.data))  # 1 byte

        if self.frame_type == FRAME_TYPE_PLANT:
            buf += struct.pack('>I', self.address)                    # 4 bytes
            
        buf += struct.pack('>I', self.id)                             # 4 bytes
        buf += self.data                                              # N byte
        crc16 = self.CRC16(buf)
        buf += struct.pack('>H', crc16)                               # 2 bytes

        # prepare output buffer and inject escape (=stop) token where necessary
        self.EscapeCount = 0
        self.stream = bytearray()
        self.addToStream(struct.pack('c', start_token))        # 1 byte
        self.addToStream(buf)

    # add a byte array to the stream and consider adding escape token in case of start or escape/stop token
    def response(self, rsp):
        self.data = encode_value(self.id, rsp) 
            
    # add a byte array to the stream and consider adding escape token in case of start or escape/stop token
    def addToStream(self, data):
        for c in data:
            if c == start_token or c == escape_token:
                if len(self.stream) > 0:
                    self.EscapeCount += 1                    # just for debugging
                    self.stream += escape_token
            
            self.stream += c

    # calculate the CRC16 for the passed data stream
    def CRC16(self, data):
        bitrange = xrange(8) # 8 Bits
        crcsum = 0xFFFF
        polynom  = 0x1021 #CCITT Polynom

        # skip start token
        Buffer = bytearray(data)
        if len(data) & 0x01:
            Buffer.append(0)
            
        for byte in Buffer:
            crcsum ^= byte << 8
            for bit in bitrange: # Loop for 8 bits 
                crcsum <<= 1
                if crcsum & 0x7FFF0000:
                    #~~ overflow in bit 16
                    crcsum = (crcsum & 0x0000FFFF) ^ polynom
        return crcsum

    # prepare a frame and set alle class compontents
    def prepare(self, command, id, address, value = None):
        obj = find_by_id(id)
        if obj is None:
            self.FrameComplete = False
        else:
            self.FrameComplete = True
            self.command = command
            self.address = address
            self.id = obj.id
            if command == cmd_read:
                self.data = ''
            else:
                if value is not None:
                    self.data = encode_by_type(obj.data_type, value)


# helper function to print and error
def errlog(*args):
    sys.stderr.write(' '.join(map(str,args)) + '\n')
    
# helper function to print debug messages
def dbglog(*args):
    if bVerbose == True:
        sys.stdout.write(' '.join(map(str,args)) + '\n')
        
    return bVerbose
        
# helper function to connect to the server (e.g. the RCT power device)
def connect_to_server():
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((host, port))
        dbglog('connect to ', host, 'port', port)
        return clientsocket
    except:
        errlog('unable to connect to', host, 'port', port)
        return None

# send a frame to RCT
def send(clientsocket, cmd, id, address=0, value=0):
    frame = Frame()
    frame.prepare(cmd, id, address, value)
    frame.encode()
    clientsocket.send(frame.stream)
    return frame

# this function reads from the socket.
# Note: unexpected bytes within buf are discarded. 
#       According to the spec it should not happen and should not be a problem
def receive(sock, id = 0, timeout = receive_timeout):
    response = Frame()
    while True:
        try:
            ready_to_read, ready_to_write, err_detect = select.select([sock,], [], [sock,], timeout)
        except select.error:
            return None

        if ready_to_read:    
            buf = sock.recv(512)
            if len(buf) > 0:
                i = response.consume(buf)
                if response.FrameComplete and response.CRCOk == True:
                    if id > 0 and id != response.id:
                        #errlog('response id', id, 'doesn\'t fit to the requested id ', response.id)
                        #errlog(hexdump(buf))
                        return None
                    else:
                        return response
                else:
                    # frame incomplete or CRC error
                    #errlog(hexdump(buf))
                    return None

        else:
            # timeout
            return None

# send a read request and wait for the response
def read(clientsocket, id, address = 0, timeout = receive_timeout):
    if clientsocket is not None:
        # repeat until the correct response has been received
        while(True):
            frame = send(clientsocket, cmd_read, id, address)
        
            response = receive(clientsocket, id, timeout)
            if response is not None:
                return response.value
    
def close(clientsocket):
    clientsocket.close()
        
def hexdump(src, length=16):
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    addr = True
    if length > len(src):
        length = len(src)
        addr = False
    for c in xrange(0, len(src), length):
        chars = src[c:c+length]
        hex = ' '.join(["%02x" % ord(x) for x in chars])
        printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        if addr == True:
            lines.append("%04x  %-*s  %s" % (c, length*3, hex, printable))
        else:
            lines.append("%-*s  %s" % (length*3, hex, printable))
            
        if c + length < len(src):
            lines.append("\n")

    return ''.join(lines)
    
# setup the rct_id table with id and expected data type          
def init(argv):
    global bVerbose
    global host
    global port
    global search_id
    global search_name
    global param_len
    global desc_len

    # parse command line arguments
    try:
        options, remainder = getopt.getopt(argv[1:], 'p:i:v', ['port=', 'ip=', 'verbose', 'id=', 'name='])
    except getopt.GetoptError as err:
        # print help information and exit:
        errlog(err) # will print something like "option -a not recognized"
        errlog('usage: ', argv[0], '[--ip_addr=<host>] [--verbose] [--port=<portnr>] [--id=0xXXXXXXXX|--name=<string>] ')
        sys.exit(-1)
    
    for opt, arg in options:
        if opt in ('-p', '--port'):
            port = int(arg, base=10)
        elif opt in ('-i', '--ip'):
            host = arg
        elif opt in ('--id'):
            search_id = int(arg, base=16)
        elif opt in ('--name'):
            search_name = arg
        elif opt in ('-v', '--verbose'):
            bVerbose = True

    id_tab_setup()
    param_len = 0;
    desc_len = 0;
    for obj in id_tab:
        if len(obj.name) > param_len:
            param_len = len(obj.name)
        if len(obj.desc) > desc_len:
            desc_len = len(obj.desc)

    sort_by_name()

def id_tab_setup():
    # add all known id's with name, data type, description and unit to the id table
    id_tab.append(rct_id(0x0104EB6A,   0, 'rb485.f_grid[2]',                                  rct_id.t_float,   'Grid phase 3 frequency [Hz]'))
    id_tab.append(rct_id(0x011F41DB,   1, 'power_mng.schedule[0]',                            rct_id.t_string,  'power_mng.schedule[0]'))
    id_tab.append(rct_id(0x016109E1,   2, 'grid_mon[0].u_over.time',                          rct_id.t_float,   'Max. voltage switch-off time level 1 [s]'))
    id_tab.append(rct_id(0x01676FA6,   3, 'battery.cells_stat[3]',                            rct_id.t_string,  'battery.cells_stat[3]'))
    id_tab.append(rct_id(0x019C0B60,   4, 'cs_neg[2]',                                        rct_id.t_float,   'Miltiply value of the current sensor 2 by'))
    id_tab.append(rct_id(0x02247588,   5, 'battery_placeholder[0].cells_stat[2].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[2].u_min.value'))
    id_tab.append(rct_id(0x031A6110,   6, 'energy.e_ext_month',                               rct_id.t_float,   'External month energy [Wh]'))
    id_tab.append(rct_id(0x035E64EA,   7, 'battery_placeholder[0].module_sn[5]',              rct_id.t_string,  'Module 5 Serial Number'))
    id_tab.append(rct_id(0x039BDE11,   8, 'hw_test.state',                                    rct_id.t_uint8,   'hw_test.state'))
    id_tab.append(rct_id(0x03A39CA2,   9, 'g_sync.p_ac_load[0]',                              rct_id.t_float,   'Load household phase 1 [W]'))
    id_tab.append(rct_id(0x03D9C51F,  10, 'battery.cells_stat[0].u_max.value',                rct_id.t_float,   'battery.cells_stat[0].u_max.value'))
    id_tab.append(rct_id(0x040385DB,  11, 'common_control_bits',                              rct_id.t_uint32,  'Bit coded function'))
    id_tab.append(rct_id(0x048C9D69,  12, 'battery_placeholder[0].cells_stat[1].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[1].u_min.value'))
    id_tab.append(rct_id(0x04EAAA98,  13, 'nsm.f_low_entry',                                  rct_id.t_float,   'Entry frequency for P(f) under-frequency mode [Hz]'))
    id_tab.append(rct_id(0x0528D1D8,  14, 'frt.u_min[2]',                                     rct_id.t_float,   'Point 3 voltage [V]'))
    id_tab.append(rct_id(0x056162CA,  15, 'battery.cells_stat[4].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[4].u_min.time'))
    id_tab.append(rct_id(0x056417DF,  16, 'battery.cells_stat[3].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[3].t_max.index'))
    id_tab.append(rct_id(0x058F1759,  17, 'hw_test.bt_power[6]',                              rct_id.t_float,   'hw_test.bt_power[6]'))
    id_tab.append(rct_id(0x05C7CFB1,  18, 'logger.day_egrid_load_log_ts',                     rct_id.t_int32,   'logger.day_egrid_load_log_ts'))
    id_tab.append(rct_id(0x064A60FE,  19, 'battery.cells_stat[4].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[4].t_max.index'))
    id_tab.append(rct_id(0x064E4340,  20, 'logger.minutes_ubat_log_ts',                       rct_id.t_int32,   'logger.minutes_ubat_log_ts'))
    id_tab.append(rct_id(0x06A9FFA2,  21, 'battery.charged_amp_hours',                        rct_id.t_float,   'Total charge flow into battery [Ah]'))
    id_tab.append(rct_id(0x06E03755,  22, 'wifi.ip',                                          rct_id.t_string,  'IP Address'))
    id_tab.append(rct_id(0x071B5514,  23, 'battery_placeholder[0].cells_stat[3].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[3].t_max.index'))
    id_tab.append(rct_id(0x07367B64,  24, 'rb485.phase_marker',                               rct_id.t_int16,   'Next phase after phase 1 in Power Switch'))
    id_tab.append(rct_id(0x073C7E5D,  25, 'battery_placeholder[0].max_cell_temperature',      rct_id.t_float,   'battery_placeholder[0].max_cell_temperature'))
    id_tab.append(rct_id(0x074B1EF5,  26, 'battery_placeholder[0].cells_stat[3].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[3].u_max.index'))
    id_tab.append(rct_id(0x077692DE,  27, 'battery.cells_stat[4].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[4].u_max.index'))
    id_tab.append(rct_id(0x07C61FAD,  28, 'adc.u_ref_1_5v[0]',                                rct_id.t_uint16,  'Reference voltage 1 [V]'))
    id_tab.append(rct_id(0x08679611,  29, 'net.id',                                           rct_id.t_uint32,  'net.id'))
    id_tab.append(rct_id(0x086C75B0,  30, 'battery.stack_software_version[3]',                rct_id.t_uint32,  'Software version stack 3'))
    id_tab.append(rct_id(0x0875C906,  31, 'hw_test.bt_time[2]',                               rct_id.t_float,   'hw_test.bt_time[2]'))
    id_tab.append(rct_id(0x08E81725,  32, 'battery_placeholder[0].cells_stat[0].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[0].t_max.value'))
    id_tab.append(rct_id(0x095AFAA8,  33, 'logger.minutes_ul3_log_ts',                        rct_id.t_int32,   'logger.minutes_ul3_log_ts'))
    id_tab.append(rct_id(0x09923C1E,  35, 'battery.cells_stat[3].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[3].t_min.index'))
    id_tab.append(rct_id(0x0A04CA7F,  36, 'g_sync.u_zk_n_avg',                                rct_id.t_float,   'Negative buffer capacitor voltage [V]'))
    id_tab.append(rct_id(0x0AA372CE,  37, 'p_rec_req[1]',                                     rct_id.t_float,   'Required battery to grid power [W]'))
    id_tab.append(rct_id(0x0AFDD6CF,  38, 'acc_conv.i_acc_lp_fast',                           rct_id.t_float,   'Battery current [A]'))
    id_tab.append(rct_id(0x0B94A673,  39, 'battery_placeholder[0].cells_stat[6].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[6].t_min.time'))
    id_tab.append(rct_id(0x0BA16A10,  40, 'wifi.sockb_protocol',                              rct_id.t_enum,    'Network mode'))
    id_tab.append(rct_id(0x0C2A7286,  41, 'battery_placeholder[0].cells_resist[0]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[0]'))
    id_tab.append(rct_id(0x0C3815C2,  42, 'net.load_reduction',                               rct_id.t_float,   'net.load_reduction'))
    id_tab.append(rct_id(0x0C588B75,  43, 'energy.e_ext_day_sum',                             rct_id.t_float,   'energy.e_ext_day_sum'))
    id_tab.append(rct_id(0x0CB5D21B,  44, 'dc_conv.dc_conv_struct[1].p_dc_lp',                rct_id.t_float,   'Solar generator B power [W]'))
    id_tab.append(rct_id(0x0CBA34B9,  45, 'nsm.u_q_u[3]',                                     rct_id.t_float,   ''))
    id_tab.append(rct_id(0x0CC4BDAA,  46, 'detect_phase_shift_enable',                        rct_id.t_bool,    'Enable active island detection'))
    id_tab.append(rct_id(0x0CFA8BC4,  47, 'battery.stack_cycles[1]',                          rct_id.t_uint16,  'battery.stack_cycles[1]'))
    id_tab.append(rct_id(0x0D658831,  48, 'i_bottom_max',                                     rct_id.t_float,   'i_bottom_max'))
    id_tab.append(rct_id(0x0DACF21B,  49, 'battery.cells_stat[4]',                            rct_id.t_string,  'battery.cells_stat[4]'))
    id_tab.append(rct_id(0x0DBD5E77,  50, 'battery_placeholder[0].cells_stat[6].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[6].u_min.index'))
    id_tab.append(rct_id(0x0DE3D20D,  51, 'battery.status2',                                  rct_id.t_int32,   'Battery extra status'))
    id_tab.append(rct_id(0x0DF164DE,  52, 'logger.day_eb_log_ts',                             rct_id.t_int32,   'logger.day_eb_log_ts'))
    id_tab.append(rct_id(0x0DF45696,  53, 'io_board.io1_polarity',                            rct_id.t_bool,    'Inverted signal on input I/O 1'))
    id_tab.append(rct_id(0x0E0505B4,  54, 'flash_rtc.time_stamp_set',                         rct_id.t_uint32,  'Set date/time'))
    id_tab.append(rct_id(0x0E4AA301,  55, 'battery_placeholder[0].cells_stat[6].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[6].u_max.index'))
    id_tab.append(rct_id(0x0E799A56,  56, 'io_board.rse_table[0]',                            rct_id.t_float,   'K4..K1: 0000'))
    id_tab.append(rct_id(0x0EC64BA7,  57, 'battery_placeholder[0].stack_software_version[3]', rct_id.t_uint32,  'Software version stack 3'))
    id_tab.append(rct_id(0x0EF60C7E,  58, 'battery.cells_stat[3].u_max.value',                rct_id.t_float,   'battery.cells_stat[3].u_max.value'))
    id_tab.append(rct_id(0x0F28E2E1,  59, 'energy.e_ext_total_sum',                           rct_id.t_float,   'energy.e_ext_total_sum'))
    id_tab.append(rct_id(0x0FA29566,  60, 'logger.minutes_ub_log_ts',                         rct_id.t_int32,   'logger.minutes_ub_log_ts'))
    id_tab.append(rct_id(0x0FB40090,  61, 'io_board.check_rs485_result',                      rct_id.t_uint8,   'io_board.check_rs485_result'))
    id_tab.append(rct_id(0x1025B491,  62, 'battery_placeholder[0].maximum_discharge_current', rct_id.t_float,   'Max. discharge current [A]'))
    id_tab.append(rct_id(0x10842019,  63, 'nsm.cos_phi_p[3][1]',                              rct_id.t_float,   'Point 4 [cos(. )] (positive = overexcited)'))
    id_tab.append(rct_id(0x1089ACA9,  64, 'nsm.u_q_u[0]',                                     rct_id.t_float,   'Low voltage min. point [V]'))
    id_tab.append(rct_id(0x108FC93D,  65, 'max_phase_shift',                                  rct_id.t_float,   'Max. phase shift from 120? position [degrees]'))
    id_tab.append(rct_id(0x10970E9D,  66, 'energy.e_ac_month',                                rct_id.t_float,   'Month energy [Wh]'))
    id_tab.append(rct_id(0x1156DFD0,  67, 'power_mng.battery_power',                          rct_id.t_float,   'Battery discharge power [W]'))
    id_tab.append(rct_id(0x120EC3B4,  68, 'battery.cells_stat[4].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[4].u_min.index'))
    id_tab.append(rct_id(0x126ABC86,  69, 'energy.e_grid_load_month',                         rct_id.t_float,   'Month energy grid load [Wh]'))
    id_tab.append(rct_id(0x132AA71E,  70, 'logger.minutes_temp2_log_ts',                      rct_id.t_int32,   'logger.minutes_temp2_log_ts'))
    id_tab.append(rct_id(0x1348AB07,  71, 'battery.cells[4]',                                 rct_id.t_string,  'battery.cells[4]'))
    id_tab.append(rct_id(0x147E8E26,  72, 'g_sync.p_ac[1]',                                   rct_id.t_float,   'AC2'))
    id_tab.append(rct_id(0x14C0E627,  73, 'wifi.password',                                    rct_id.t_string,  'WiFi password'))
    id_tab.append(rct_id(0x14FCA232,  74, 'nsm.rpm_lock_out_power',                           rct_id.t_float,   'Reactive Power Mode lock-out power [P/Pn]'))
    id_tab.append(rct_id(0x15AB1A61,  75, 'power_mng.schedule[2]',                            rct_id.t_string,  'power_mng.schedule[2]'))
    id_tab.append(rct_id(0x162491E8,  76, 'battery.module_sn[5]',                             rct_id.t_string,  'Module 5 Serial Number'))
    id_tab.append(rct_id(0x1639B2D8,  77, 'battery_placeholder[0].cells_stat[4].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[4].u_max.index'))
    id_tab.append(rct_id(0x16A1F844,  78, 'battery.bms_sn',                                   rct_id.t_string,  'BMS Serial Number'))
    id_tab.append(rct_id(0x16AF2A92,  79, 'db.power_board.Current_Mean',                      rct_id.t_float,   'db.power_board.Current_Mean'))
    id_tab.append(rct_id(0x16B28CCA,  80, 'adc.u_ref_1_5v[1]',                                rct_id.t_uint16,  'Reference voltage 2 [V]'))
    id_tab.append(rct_id(0x16ED8F8F,  81, 'partition[1].last_id',                             rct_id.t_int32,   'partition[1].last_id'))
    id_tab.append(rct_id(0x173D81E4,  82, 'rb485.version_boot',                               rct_id.t_uint32,  'Power Switch bootloader version'))
    id_tab.append(rct_id(0x1781CD31,  83, 'battery_placeholder[0].soh',                       rct_id.t_float,   'SOH (State of Health)'))
    id_tab.append(rct_id(0x17E3AF97,  84, 'db.power_board.adc_p9V_meas',                      rct_id.t_float,   'db.power_board.adc_p9V_meas'))
    id_tab.append(rct_id(0x18469762,  85, 'battery_placeholder[0].cells_stat[0].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[0].u_max.value'))
    id_tab.append(rct_id(0x18BD807D,  86, 'battery_placeholder[0].cells_stat[4].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[4].t_min.index'))
    id_tab.append(rct_id(0x18D1E9E0,  87, 'battery.cells_stat[5].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[5].u_max.index'))
    id_tab.append(rct_id(0x18F98B6D,  88, 'battery.cells_stat[3].u_min.value',                rct_id.t_float,   'battery.cells_stat[3].u_min.value'))
    id_tab.append(rct_id(0x19608C98,  89, 'partition[3].last_id',                             rct_id.t_int32,   'partition[3].last_id'))
    id_tab.append(rct_id(0x19B814F2,  90, 'logger.year_egrid_feed_log_ts',                    rct_id.t_int32,   'logger.year_egrid_feed_log_ts'))
    id_tab.append(rct_id(0x1ABA3EE8,  91, 'p_rec_req[0]',                                     rct_id.t_float,   'Required compensation power [W]'))
    id_tab.append(rct_id(0x1AC87AA0,  92, 'g_sync.p_ac_load_sum_lp',                          rct_id.t_float,   'Load household - external Power[W]'))
    id_tab.append(rct_id(0x1B39A3A3,  93, 'battery.bms_power_version',                        rct_id.t_uint32,  'Software version BMS Power'))
    id_tab.append(rct_id(0x1B5445C4,  94, 'io_board.check_rse_result',                        rct_id.t_uint16,  'io_board.check_rse_result'))
    id_tab.append(rct_id(0x1BFA5A33,  95, 'energy.e_grid_load_total_sum',                     rct_id.t_float,   'energy.e_grid_load_total_sum'))
    id_tab.append(rct_id(0x1C4A665F,  96, 'grid_pll[0].f',                                    rct_id.t_float,   'Grid frequency [Hz]'))
    id_tab.append(rct_id(0x1D0623D6,  97, 'wifi.dns_address',                                 rct_id.t_string,  'DNS address'))
    id_tab.append(rct_id(0x1D2994EA,  98, 'power_mng.soc_charge_power',                       rct_id.t_float,   ''))
    id_tab.append(rct_id(0x1D49380A,  99, 'logger.minutes_eb_log_ts',                         rct_id.t_int32,   'logger.minutes_eb_log_ts'))
    id_tab.append(rct_id(0x1D83D2A5, 100, 'battery_placeholder[0].cells[4]',                  rct_id.t_string,  'battery_placeholder[0].cells[4]'))
    id_tab.append(rct_id(0x1E0EB397, 101, 'battery_placeholder[0].cells_stat[6].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[6].u_max.value'))
    id_tab.append(rct_id(0x1E5FCA70, 102, 'battery.maximum_charge_current',                   rct_id.t_float,   'Max. charge current [A]'))
    id_tab.append(rct_id(0x1F44C23A, 103, 'battery_placeholder[0].cells_stat[1].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[1].t_min.index'))
    id_tab.append(rct_id(0x1F73B6A4, 104, 'battery.cells_stat[3].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[3].t_max.time'))
    id_tab.append(rct_id(0x1F9CBBF2, 105, 'db.power_board.Calibr_Value_Mean',                 rct_id.t_float,   'db.power_board.Calibr_Value_Mean'))
    id_tab.append(rct_id(0x1FA192E3, 106, 'battery_placeholder[0].cells_resist[4]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[4]'))
    id_tab.append(rct_id(0x1FB3A602, 107, 'battery_placeholder[0].cells_stat[2].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[2].t_max.value'))
    id_tab.append(rct_id(0x1FEB2F67, 108, 'switch_on_cond.u_min',                             rct_id.t_float,   'Min. voltage'))
    id_tab.append(rct_id(0x2082BFB6, 109, 'hw_test.bt_time[9]',                               rct_id.t_float,   'hw_test.bt_time[9]'))
    id_tab.append(rct_id(0x20A3A91F, 110, 'battery_placeholder[0].module_sn[4]',              rct_id.t_string,  'Module 4 Serial Number'))
    id_tab.append(rct_id(0x20FD4419, 111, 'prim_sm.island_next_repeat_timeout',               rct_id.t_float,   'Next island trial timeout [s]'))
    id_tab.append(rct_id(0x21879805, 112, 'logger.minutes_eac1_log_ts',                       rct_id.t_int32,   'logger.minutes_eac1_log_ts'))
    id_tab.append(rct_id(0x21961B58, 113, 'battery.current',                                  rct_id.t_float,   'Battery current [A]'))
    id_tab.append(rct_id(0x21E1A802, 114, 'energy.e_dc_month_sum[1]',                         rct_id.t_float,   'energy.e_dc_month_sum[1]'))
    id_tab.append(rct_id(0x21EE7CBB, 115, 'rb485.u_l_grid[2]',                                rct_id.t_float,   'Grid phase 3 voltage [V]'))
    id_tab.append(rct_id(0x2266DCB8, 116, 'flash_rtc.rtc_mcc_quartz_max_diff',                rct_id.t_float,   'Maximum allowed quartz frequency difference between RTC and Microcontroller [ppm]'))
    id_tab.append(rct_id(0x226A23A4, 117, 'dc_conv.dc_conv_struct[0].u_target',               rct_id.t_float,   'MPP on input A [V]'))
    id_tab.append(rct_id(0x2295401F, 118, 'battery_placeholder[0].cells_stat[3].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[3].u_max.time'))
    id_tab.append(rct_id(0x22CC80C6, 119, 'frt.u_min_end',                                    rct_id.t_float,   'FRT end undervoltage threshold [V]'))
    id_tab.append(rct_id(0x234B4736, 120, 'fault[1].flt',                                     rct_id.t_uint32,  'Error bit field 2'))
    id_tab.append(rct_id(0x234DD4DF, 121, 'switch_on_cond.f_min',                             rct_id.t_float,   'Min. frequency'))
    id_tab.append(rct_id(0x235E0DF5, 122, 'battery_placeholder[0].stack_software_version[1]', rct_id.t_uint32,  'Software version stack 1'))
    id_tab.append(rct_id(0x236D2178, 123, 'frt.t_min[1]',                                     rct_id.t_float,   'Point 2 time [s]'))
    id_tab.append(rct_id(0x23D4A386, 124, 'battery_placeholder[0].cells_stat[0]',             rct_id.t_string,  'battery_placeholder[0].cells_stat[0]'))
    id_tab.append(rct_id(0x23E55DA0, 125, 'battery.cells_stat[5]',                            rct_id.t_string,  'battery.cells_stat[5]'))
    id_tab.append(rct_id(0x23F525DE, 126, 'net.command',                                      rct_id.t_uint16,  'net.command'))
    id_tab.append(rct_id(0x24150B85, 127, 'g_sync.u_zk_sum_mov_avg',                          rct_id.t_float,   'Actual DC link voltage [V]'))
    id_tab.append(rct_id(0x241CFA0A, 128, 'battery_placeholder[0].min_cell_temperature',      rct_id.t_float,   'battery_placeholder[0].min_cell_temperature'))
    id_tab.append(rct_id(0x241F1F98, 129, 'energy.e_dc_day_sum[1]',                           rct_id.t_float,   'energy.e_dc_day_sum[1]'))
    id_tab.append(rct_id(0x24AC4CBB, 130, 'battery_placeholder[0].cells_resist[6]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[6]'))
    id_tab.append(rct_id(0x2545E22D, 131, 'g_sync.u_l_rms[2]',                                rct_id.t_float,   'AC voltage phase 3 [V]'))
    id_tab.append(rct_id(0x257B5945, 132, 'battery.cells_stat[2].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[2].u_min.index'))
    id_tab.append(rct_id(0x257B7612, 133, 'battery.module_sn[3]',                             rct_id.t_string,  'Module 3 Serial Number'))
    id_tab.append(rct_id(0x26260419, 134, 'nsm.cos_phi_p[1][0]',                              rct_id.t_float,   'Point 2 [P/Pn]'))
    id_tab.append(rct_id(0x26363AAE, 135, 'battery.cells_stat[1].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[1].t_max.index'))
    id_tab.append(rct_id(0x265EACF6, 136, 'battery.cells_stat[2].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[2].t_max.time'))
    id_tab.append(rct_id(0x26EFFC2F, 137, 'energy.e_grid_feed_year',                          rct_id.t_float,   'Year energy grid feed-in [Wh]'))
    id_tab.append(rct_id(0x2703A771, 138, 'cs_struct.is_tuned',                               rct_id.t_bool,    'Current sensors are tuned'))
    id_tab.append(rct_id(0x27116260, 139, 'battery_placeholder[0].cells_stat[5].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[5].u_min.value'))
    id_tab.append(rct_id(0x27650FE2, 140, 'rb485.version_main',                               rct_id.t_uint32,  'Power Switch software version'))
    id_tab.append(rct_id(0x2788928C, 141, 'g_sync.p_ac_load[1]',                              rct_id.t_float,   'Load household phase 2 [W]'))
    id_tab.append(rct_id(0x27BE51D9, 142, 'g_sync.p_ac_sc[0]',                                rct_id.t_float,   'Grid power phase 1 [W]'))
    id_tab.append(rct_id(0x27C39CEA, 143, 'battery.stack_cycles[6]',                          rct_id.t_uint16,  'battery.stack_cycles[6]'))
    id_tab.append(rct_id(0x27C828F4, 144, 'energy.e_grid_feed_total_sum',                     rct_id.t_float,   'energy.e_grid_feed_total_sum'))
    id_tab.append(rct_id(0x27EC8487, 145, 'performance_free[0]',                              rct_id.t_uint32,  'performance_free[0]'))
    id_tab.append(rct_id(0x2848A1EE, 146, 'grid_offset',                                      rct_id.t_float,   'grid_offset'))
    id_tab.append(rct_id(0x29BDA75F, 147, 'display_struct.brightness',                        rct_id.t_uint8,   'Display brightness'))
    id_tab.append(rct_id(0x29CA60F8, 148, 'io_board.rse_table[10]',                           rct_id.t_float,   'K4..K1: 1010'))
    id_tab.append(rct_id(0x2A30A97E, 149, 'battery.stack_cycles[5]',                          rct_id.t_uint16,  'battery.stack_cycles[5]'))
    id_tab.append(rct_id(0x2A449E89, 150, 'logger.year_log_ts',                               rct_id.t_int32,   'logger.year_log_ts'))
    id_tab.append(rct_id(0x2AACCAA7, 151, 'battery.max_cell_voltage',                         rct_id.t_float,   ''))
    id_tab.append(rct_id(0x2AE703F2, 152, 'energy.e_dc_day[0]',                               rct_id.t_float,   'Solar generator A day energy [Wh]'))
    id_tab.append(rct_id(0x2BC1E72B, 153, 'battery.discharged_amp_hours',                     rct_id.t_float,   'Total charge flow from battery [Ah]'))
    id_tab.append(rct_id(0x2E06172D, 154, 'net.net_tunnel_id',                                rct_id.t_uint32,  'net.net_tunnel_id'))
    id_tab.append(rct_id(0x2E0C6220, 155, 'io_board.home_relay_sw_off_delay',                 rct_id.t_float,   'Switching off delay [s]'))
    id_tab.append(rct_id(0x2E9F3C50, 156, 'battery_placeholder[0].cells_stat[0].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[0].t_max.index'))
    id_tab.append(rct_id(0x2ED89924, 157, 'db.power_board.afi_t300',                          rct_id.t_float,   'AFI 300 mA switching off time [s]'))
    id_tab.append(rct_id(0x2ED8A639, 158, 'battery_placeholder[0].cells_stat[2].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[2].u_min.time'))
    id_tab.append(rct_id(0x2F0A6B15, 159, 'logger.month_ea_log_ts',                           rct_id.t_int32,   'logger.month_ea_log_ts'))
    id_tab.append(rct_id(0x2F3C1D7D, 160, 'energy.e_load_day',                                rct_id.t_float,   'Household day energy [Wh]'))
    id_tab.append(rct_id(0x2F84A0A9, 161, 'battery_placeholder[0].cells[2]',                  rct_id.t_string,  'battery_placeholder[0].cells[2]'))
    id_tab.append(rct_id(0x3044195F, 162, 'grid_mon[1].u_under.time',                         rct_id.t_float,   'Min. voltage switch-off time level 2 [s]'))
    id_tab.append(rct_id(0x31413485, 163, 'battery_placeholder[0].cells_stat[5].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[5].u_min.index'))
    id_tab.append(rct_id(0x314C13EB, 164, 'battery_placeholder[0].cells_stat[5].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[5].u_max.value'))
    id_tab.append(rct_id(0x315D1490, 165, 'power_mng.bat_empty_full',                         rct_id.t_uint8,   'Bit 0 - battery was empty, bit 1 - battery was full'))
    id_tab.append(rct_id(0x31ED1B75, 166, 'modbus.mode',                                      rct_id.t_enum,    'RS485 working mode'))
    id_tab.append(rct_id(0x32CD0DB3, 167, 'nsm.cos_phi_p[0][1]',                              rct_id.t_float,   'Point 1 [cos(. )] (positive = overexcited)'))
    id_tab.append(rct_id(0x32DCA605, 168, 'frt.u_max[0]',                                     rct_id.t_float,   'Point 1 voltage [V]'))
    id_tab.append(rct_id(0x331D0689, 169, 'battery.cells_stat[2].t_max.value',                rct_id.t_float,   'battery.cells_stat[2].t_max.value'))
    id_tab.append(rct_id(0x336415EA, 170, 'battery.cells_stat[0].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[0].t_max.time'))
    id_tab.append(rct_id(0x3390CC2F, 171, 'switch_on_cond.test_time_fault',                   rct_id.t_float,   'Switching on time after any grid fault [s]'))
    id_tab.append(rct_id(0x33F76B78, 172, 'nsm.p_u[0][1]',                                    rct_id.t_float,   'Point 1 voltage [V]'))
    id_tab.append(rct_id(0x34A164E7, 173, 'battery.cells_stat[0]',                            rct_id.t_string,  'battery.cells_stat[0]'))
    id_tab.append(rct_id(0x34E33726, 174, 'battery.cells_stat[2].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[2].u_max.index'))
    id_tab.append(rct_id(0x34ECA9CA, 175, 'logger.year_eb_log_ts',                            rct_id.t_int32,   'logger.year_eb_log_ts'))
    id_tab.append(rct_id(0x3500F1E8, 176, 'net.index',                                        rct_id.t_int8,    'net.index'))
    id_tab.append(rct_id(0x3503B92D, 177, 'battery.cells_stat[3].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[3].u_max.time'))
    id_tab.append(rct_id(0x3515F4A0, 178, 'nsm.p_u[3][1]',                                    rct_id.t_float,   'Point 4 voltage [V]'))
    id_tab.append(rct_id(0x360BDE8A, 179, 'nsm.startup_grad',                                 rct_id.t_float,   'Startup gradient [P/(Pn*s)]'))
    id_tab.append(rct_id(0x36214C57, 180, 'net.prev_k',                                       rct_id.t_float,   'net.prev_k'))
    id_tab.append(rct_id(0x362346D4, 181, 'switch_on_cond.max_rnd_test_time_fault',           rct_id.t_float,   'Max additional random switching on time after any grid fault [s]'))
    id_tab.append(rct_id(0x3623D82A, 182, 'prim_sm.island_flag',                              rct_id.t_uint16,  'Grid-separated'))
    id_tab.append(rct_id(0x365D12DA, 183, 'p_rec_req[2]',                                     rct_id.t_float,   'Required Pac [W]'))
    id_tab.append(rct_id(0x36A9E9A6, 184, 'power_mng.use_grid_power_enable',                  rct_id.t_bool,    'Utilize external Inverter energy'))
    id_tab.append(rct_id(0x374B5DD6, 185, 'battery_placeholder[0].cells_stat[6].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[6].u_min.time'))
    id_tab.append(rct_id(0x37F9D5CA, 186, 'fault[0].flt',                                     rct_id.t_uint32,  'Error bit field 1'))
    id_tab.append(rct_id(0x381B8BF9, 187, 'battery.soh',                                      rct_id.t_float,   'SOH (State of Health)'))
    id_tab.append(rct_id(0x383A3614, 188, 'db.power_board.afi_i60',                           rct_id.t_float,   'AFI 60 mA threshold [A]'))
    id_tab.append(rct_id(0x38789061, 189, 'nsm.f_low_rise_grad_storage',                      rct_id.t_float,   'Power rise gradient for P(f) under-frequency mode with battery [1/Pn*Hz]'))
    id_tab.append(rct_id(0x3903A5E9, 190, 'flash_rtc.flag_time_auto_switch',                  rct_id.t_bool,    'Automatically adjust clock for daylight saving time'))
    id_tab.append(rct_id(0x3906A1D0, 191, 'logger.minutes_eext_log_ts',                       rct_id.t_int32,   'logger.minutes_eext_log_ts'))
    id_tab.append(rct_id(0x392D1BEE, 192, 'wifi.connect_to_server',                           rct_id.t_uint8,   'wifi.connect_to_server'))
    id_tab.append(rct_id(0x39AD4639, 193, 'battery_placeholder[0].cells_stat[5].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[5].u_min.time'))
    id_tab.append(rct_id(0x3A0EA5BE, 194, 'power_spring_up',                                  rct_id.t_float,   'power_spring_up'))
    id_tab.append(rct_id(0x3A3050E6, 195, 'grid_lt.threshold',                                rct_id.t_float,   'Max. voltage [V]'))
    id_tab.append(rct_id(0x3A35D491, 196, 'battery_placeholder[0].cells_stat[2].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[2].u_max.value'))
    id_tab.append(rct_id(0x3A444FC6, 197, 'g_sync.s_ac_lp[0]',                                rct_id.t_float,   'Apparent power phase 1 [VA]'))
    id_tab.append(rct_id(0x3A7D5F53, 198, 'battery.cells_stat[1].u_max.value',                rct_id.t_float,   'battery.cells_stat[1].u_max.value'))
    id_tab.append(rct_id(0x3A873343, 199, 'energy.e_ac_day_sum',                              rct_id.t_float,   'energy.e_ac_day_sum'))
    id_tab.append(rct_id(0x3A9D2680, 200, 'energy.e_ext_year_sum',                            rct_id.t_float,   'energy.e_ext_year_sum'))
    id_tab.append(rct_id(0x3AA565FC, 201, 'net.package',                                      rct_id.t_string,  'net.package'))
    id_tab.append(rct_id(0x3AFEF139, 202, 'prim_sm.is_thin_layer',                            rct_id.t_bool,    'Thin-film solar module'))
    id_tab.append(rct_id(0x3B0C6A53, 203, 'bat_mng_struct.profile_pdc_max',                   rct_id.t_string,  'bat_mng_struct.profile_pdc_max'))
    id_tab.append(rct_id(0x3B5F6B9D, 204, 'rb485.f_wr[0]',                                    rct_id.t_float,   ''))
    id_tab.append(rct_id(0x3B7FCD47, 205, 'fault[2].flt',                                     rct_id.t_uint32,  'Error bit field 3'))
    id_tab.append(rct_id(0x3BA1B77B, 206, 'battery.cells_stat[3].t_min.value',                rct_id.t_float,   'battery.cells_stat[3].t_min.value'))
    id_tab.append(rct_id(0x3C24F3E8, 207, 'inv_struct.cosinus_phi',                           rct_id.t_float,   'cos .'))
    id_tab.append(rct_id(0x3C705F61, 208, 'io_board.rse_table[8]',                            rct_id.t_float,   'K4..K1: 1000'))
    id_tab.append(rct_id(0x3C87C4F5, 209, 'energy.e_grid_feed_day',                           rct_id.t_float,   'Day energy grid feed-in [Wh]'))
    id_tab.append(rct_id(0x3CA8E8D0, 210, 'hw_test.bt_time[0]',                               rct_id.t_float,   'hw_test.bt_time[0]'))
    id_tab.append(rct_id(0x3CB1EF01, 211, 'grid_mon[0].u_under.threshold',                    rct_id.t_float,   'Min. voltage level 1 [V]'))
    id_tab.append(rct_id(0x3D789979, 212, 'hw_test.bt_power[7]',                              rct_id.t_float,   'hw_test.bt_power[7]'))
    id_tab.append(rct_id(0x3DBCC6B4, 213, 'io_board.rse_table[6]',                            rct_id.t_float,   'K4..K1: 0110'))
    id_tab.append(rct_id(0x3E25C391, 214, 'bat_mng_struct.bat_calib_soc_thresh',              rct_id.t_float,   'Part of max historical SOC for battery calibration in advance'))
    id_tab.append(rct_id(0x3E722B43, 215, 'grid_mon[1].f_under.threshold',                    rct_id.t_float,   'Min. frequency level 2 [Hz]'))
    id_tab.append(rct_id(0x3E728842, 216, 'power_spring_bat',                                 rct_id.t_float,   'power_spring_bat'))
    id_tab.append(rct_id(0x3EFEB931, 217, 'db.power_board.relays_state',                      rct_id.t_uint16,  'db.power_board.relays_state'))
    id_tab.append(rct_id(0x3F98F58A, 218, 'battery.cells_stat[5].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[5].t_max.index'))
    id_tab.append(rct_id(0x400F015B, 219, 'g_sync.p_acc_lp',                                  rct_id.t_float,   'Battery power [W]'))
    id_tab.append(rct_id(0x4077335D, 220, 'g_sync.s_ac_lp[1]',                                rct_id.t_float,   'Apparent power phase 2 [VA]'))
    id_tab.append(rct_id(0x40B07CA4, 221, 'power_mng.schedule[6]',                            rct_id.t_string,  'power_mng.schedule[6]'))
    id_tab.append(rct_id(0x40FF01B7, 222, 'battery.cells[6]',                                 rct_id.t_string,  'battery.cells[6]'))
    id_tab.append(rct_id(0x41744E11, 223, 'frt.u_min[0]',                                     rct_id.t_float,   'Point 1 voltage [V]'))
    id_tab.append(rct_id(0x41B11ECF, 224, 'battery.cells_stat[3].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[3].u_min.index'))
    id_tab.append(rct_id(0x428CCF46, 225, 'battery.cells_stat[5].u_min.value',                rct_id.t_float,   'battery.cells_stat[5].u_min.value'))
    id_tab.append(rct_id(0x431509D1, 226, 'logger.month_eload_log_ts',                        rct_id.t_int32,   'logger.month_eload_log_ts'))
    id_tab.append(rct_id(0x43257820, 227, 'g_sync.p_ac[0]',                                   rct_id.t_float,   'AC1'))
    id_tab.append(rct_id(0x437B8122, 228, 'rb485.available',                                  rct_id.t_bool,    'Power Switch is available'))
    id_tab.append(rct_id(0x4397D078, 229, 'nsm.cos_phi_p[1][1]',                              rct_id.t_float,   'Point 2 [cos(. )] (positive = overexcited)'))
    id_tab.append(rct_id(0x43CD0B6F, 230, 'nsm.pf_delay',                                     rct_id.t_float,   'Delay time after P(f) [s]'))
    id_tab.append(rct_id(0x43F16F7E, 231, 'flash_state',                                      rct_id.t_uint16,  'Flash state'))
    id_tab.append(rct_id(0x43FF47C3, 232, 'db.power_board.afi_t60',                           rct_id.t_float,   'AFI 60 mA switching off time [s]'))
    id_tab.append(rct_id(0x442A3409, 233, 'battery.cells_stat[4].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[4].t_min.time'))
    id_tab.append(rct_id(0x4443C661, 234, 'battery.cells_stat[0].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[0].t_max.index'))
    id_tab.append(rct_id(0x44D4C533, 235, 'energy.e_grid_feed_total',                         rct_id.t_float,   'Total energy grid feed-in [Wh]'))
    id_tab.append(rct_id(0x4539A6D4, 236, 'can_bus.bms_update_response[0]',                   rct_id.t_uint32,  'can_bus.bms_update_response[0]'))
    id_tab.append(rct_id(0x465DDB50, 237, 'battery_placeholder[0].cells_stat[2].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[2].t_min.value'))
    id_tab.append(rct_id(0x46635546, 238, 'net.n_descendants',                                rct_id.t_int8,    'Number of descendant slaves'))
    id_tab.append(rct_id(0x4686E044, 239, 'battery_placeholder[0].cells_stat[1].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[1].u_min.index'))
    id_tab.append(rct_id(0x46892579, 240, 'flash_param.write_cycles',                         rct_id.t_uint32,  'Write cycles of flash parameters'))
    id_tab.append(rct_id(0x46C3625D, 241, 'battery_placeholder[0].cells_stat[2]',             rct_id.t_string,  'battery_placeholder[0].cells_stat[2]'))
    id_tab.append(rct_id(0x474F80D5, 242, 'iso_struct.Rn',                                    rct_id.t_float,   'Insulation resistance on negative DC input [Ohm]'))
    id_tab.append(rct_id(0x4764F9EE, 243, 'battery_placeholder[0].cells_stat[3].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[3].t_max.value'))
    id_tab.append(rct_id(0x47A1DACA, 244, 'power_mng.schedule[8]',                            rct_id.t_string,  'power_mng.schedule[8]'))
    id_tab.append(rct_id(0x485AD749, 245, 'g_sync.u_ptp_rms[1]',                              rct_id.t_float,   'Phase to phase voltage 2 [V]'))
    id_tab.append(rct_id(0x488052BA, 246, 'logger.minutes_ul2_log_ts',                        rct_id.t_int32,   'logger.minutes_ul2_log_ts'))
    id_tab.append(rct_id(0x48D73FA5, 247, 'g_sync.i_dr_lp[2]',                                rct_id.t_float,   'Current phase 3 (average) [A]'))
    id_tab.append(rct_id(0x494FE156, 248, 'power_spring_offset',                              rct_id.t_float,   'power_spring_offset'))
    id_tab.append(rct_id(0x495BF0B6, 249, 'energy.e_dc_year_sum[0]',                          rct_id.t_float,   'energy.e_dc_year_sum[0]'))
    id_tab.append(rct_id(0x4992E65A, 250, 'update_is_allowed_id',                             rct_id.t_uint8,   'update_is_allowed_id'))
    id_tab.append(rct_id(0x4A61BAEE, 251, 'nsm.p_u[3][0]',                                    rct_id.t_float,   'Point 4 P/Pn'))
    id_tab.append(rct_id(0x4AAEB0D2, 252, 'battery_placeholder[0].cells_stat[1]',             rct_id.t_string,  'battery_placeholder[0].cells_stat[1]'))
    id_tab.append(rct_id(0x4AE96C12, 253, 'dc_conv.dc_conv_struct[1].mpp.mpp_step',           rct_id.t_float,   'MPP search step on input B [V]'))
    id_tab.append(rct_id(0x4B51A539, 254, 'battery.prog_sn',                                  rct_id.t_string,  'battery.prog_sn'))
    id_tab.append(rct_id(0x4BC0F974, 255, 'buf_v_control.power_reduction_max_solar',          rct_id.t_float,   'Solar plant peak power [Wp]'))
    id_tab.append(rct_id(0x4BE02BB7, 256, 'energy.e_load_day_sum',                            rct_id.t_float,   'energy.e_load_day_sum'))
    id_tab.append(rct_id(0x4C12C4C7, 257, 'cs_neg[1]',                                        rct_id.t_float,   ''))
    id_tab.append(rct_id(0x4C14CC7C, 258, 'logger.year_ea_log_ts',                            rct_id.t_int32,   'logger.year_ea_log_ts'))
    id_tab.append(rct_id(0x4C2A7CDC, 259, 'nsm.cos_phi_p[2][1]',                              rct_id.t_float,   'Point 3 [cos(. )] (positive = overexcited)'))
    id_tab.append(rct_id(0x4C374958, 260, 'nsm.startup_grad_after_fault',                     rct_id.t_float,   'Startup gradient after fault [P/(Pn*s)]'))
    id_tab.append(rct_id(0x4CB7C0DC, 261, 'battery.min_cell_voltage',                         rct_id.t_float,   'battery.min_cell_voltage'))
    id_tab.append(rct_id(0x4D684EF2, 262, 'battery_placeholder[0].cells[0]',                  rct_id.t_string,  'battery_placeholder[0].cells[0]'))
    id_tab.append(rct_id(0x4D985F33, 263, 'battery.cells_stat[5].u_max.value',                rct_id.t_float,   'battery.cells_stat[5].u_max.value'))
    id_tab.append(rct_id(0x4DB1B91E, 264, 'switch_on_cond.f_max',                             rct_id.t_float,   'Max. frequency'))
    id_tab.append(rct_id(0x4DC372A0, 265, 'battery_placeholder[0].cells_stat[4].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[4].u_max.value'))
    id_tab.append(rct_id(0x4E04DD55, 266, 'battery.soc_update_since',                         rct_id.t_float,   'battery.soc_update_since'))
    id_tab.append(rct_id(0x4E0C56F2, 267, 'flash_rtc.rtc_mcc_quartz_ppm_difference',          rct_id.t_float,   'Quartz frequency difference between RTC and Microcontroller [ppm]'))
    id_tab.append(rct_id(0x4E2B42A4, 268, 'hw_test.bt_power[0]',                              rct_id.t_float,   'hw_test.bt_power[0]'))
    id_tab.append(rct_id(0x4E3CB7F8, 269, 'phase_3_mode',                                     rct_id.t_bool,    '3-phase feed in'))
    id_tab.append(rct_id(0x4E49AEC5, 270, 'g_sync.p_ac_sum',                                  rct_id.t_float,   'Real power [W]'))
    id_tab.append(rct_id(0x4E699086, 271, 'battery.module_sn[4]',                             rct_id.t_string,  'Module 4 Serial Number'))
    id_tab.append(rct_id(0x4E77B2CE, 272, 'hw_test.bt_cycle',                                 rct_id.t_uint8,   'hw_test.bt_cycle'))
    id_tab.append(rct_id(0x4E9D95A6, 273, 'logger.year_eext_log_ts',                          rct_id.t_int32,   'logger.year_eext_log_ts'))
    id_tab.append(rct_id(0x4EE8DB78, 274, 'energy.e_load_year_sum',                           rct_id.t_float,   'energy.e_load_year_sum'))
    id_tab.append(rct_id(0x4F330E08, 275, 'io_board.io2_usage',                               rct_id.t_enum,    'Digital I/O 2 usage'))
    id_tab.append(rct_id(0x4F735D10, 276, 'db.temp2',                                         rct_id.t_float,   'Heat sink (battery actuator) temperature [?C]'))
    id_tab.append(rct_id(0x4FC53F19, 277, 'battery_placeholder[0].module_sn[3]',              rct_id.t_string,  'Module 3 Serial Number'))
    id_tab.append(rct_id(0x4FEDC1BE, 278, 'battery_placeholder[0].cells_stat[5].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[5].t_min.value'))
    id_tab.append(rct_id(0x4FF8CCE2, 279, 'battery_placeholder[0].stack_software_version[5]', rct_id.t_uint32,  'Software version stack 5'))
    id_tab.append(rct_id(0x501A162D, 280, 'battery.cells_resist[5]',                          rct_id.t_string,  'battery.cells_resist[5]'))
    id_tab.append(rct_id(0x50514732, 281, 'battery.cells_stat[6].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[6].u_min.index'))
    id_tab.append(rct_id(0x508FCE78, 282, 'adc.u_ref_1_5v[3]',                                rct_id.t_uint16,  'Reference voltage 4 [V]'))
    id_tab.append(rct_id(0x50B441C1, 283, 'logger.minutes_ea_log_ts',                         rct_id.t_int32,   'logger.minutes_ea_log_ts'))
    id_tab.append(rct_id(0x5151D84C, 284, 'prim_sm.island_reset_retrials_counter_time',       rct_id.t_float,   'Reset island trials counter in [min] (by 0 not used)'))
    id_tab.append(rct_id(0x518C7BBE, 285, 'battery.cells_stat[5].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[5].u_min.time'))
    id_tab.append(rct_id(0x51E5377D, 286, 'battery_placeholder[0].stack_cycles[1]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[1]'))
    id_tab.append(rct_id(0x5293B668, 287, 'logger.minutes_soc_log_ts',                        rct_id.t_int32,   'logger.minutes_soc_log_ts'))
    id_tab.append(rct_id(0x53656F42, 288, 'battery_placeholder[0].cells_stat[2].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[2].u_max.index'))
    id_tab.append(rct_id(0x537C719F, 289, 'battery.cells_stat[0].t_max.value',                rct_id.t_float,   'battery.cells_stat[0].t_max.value'))
    id_tab.append(rct_id(0x53886C09, 290, 'wifi.connect_to_service',                          rct_id.t_uint8,   'wifi.connect_to_service'))
    id_tab.append(rct_id(0x53EF7649, 291, 'nsm.p_u[0][0]',                                    rct_id.t_float,   'Point 1 P/Pn'))
    id_tab.append(rct_id(0x5411CE1B, 292, 'logger.minutes_ul1_log_ts',                        rct_id.t_int32,   'logger.minutes_ul1_log_ts'))
    id_tab.append(rct_id(0x5438B68E, 293, 'grid_mon[1].u_over.threshold',                     rct_id.t_float,   'Max. voltage level 2 [V]'))
    id_tab.append(rct_id(0x54829753, 294, 'p_rec_lim[1]',                                     rct_id.t_float,   'Max. battery to grid power [W]'))
    id_tab.append(rct_id(0x54B4684E, 295, 'g_sync.u_l_rms[1]',                                rct_id.t_float,   'AC voltage phase 2 [V]'))
    id_tab.append(rct_id(0x54DBC202, 296, 'io_board.rse_table[12]',                           rct_id.t_float,   'K4..K1: 1100'))
    id_tab.append(rct_id(0x554D8FEE, 297, 'logger.minutes_eac2_log_ts',                       rct_id.t_int32,   'logger.minutes_eac2_log_ts'))
    id_tab.append(rct_id(0x5570401B, 298, 'battery.stored_energy',                            rct_id.t_float,   'Total energy flow into battery [Wh]'))
    id_tab.append(rct_id(0x55C22966, 299, 'g_sync.s_ac[2]',                                   rct_id.t_float,   'Apparent power phase 3 [VA]'))
    id_tab.append(rct_id(0x55DDF7BA, 300, 'battery.max_cell_temperature',                     rct_id.t_float,   'battery.max_cell_temperature'))
    id_tab.append(rct_id(0x5673D737, 301, 'wifi.connect_to_wifi',                             rct_id.t_bool,    'wifi.connect_to_wifi'))
    id_tab.append(rct_id(0x57429627, 302, 'wifi.authentication_method',                       rct_id.t_string,  'WiFi authentication method'))
    id_tab.append(rct_id(0x576D2A08, 303, 'battery_placeholder[0].cells_stat[3].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[3].t_min.time'))
    id_tab.append(rct_id(0x57945EE4, 304, 'battery_placeholder[0].maximum_charge_current',    rct_id.t_float,   'Max. charge current [A]'))
    id_tab.append(rct_id(0x58378BD0, 305, 'hw_test.bt_time[3]',                               rct_id.t_float,   'hw_test.bt_time[3]'))
    id_tab.append(rct_id(0x5847E59E, 306, 'battery.maximum_charge_voltage_constant_u',        rct_id.t_float,   'Max. charge voltage [V]'))
    id_tab.append(rct_id(0x5867B3BE, 307, 'io_board.rse_table[2]',                            rct_id.t_float,   'K4..K1: 0010'))
    id_tab.append(rct_id(0x58C1A946, 308, 'io_board.check_state',                             rct_id.t_uint8,   'io_board.check_state'))
    id_tab.append(rct_id(0x592B13DF, 309, 'power_mng.schedule[4]',                            rct_id.t_string,  'power_mng.schedule[4]'))
    id_tab.append(rct_id(0x59358EB2, 310, 'power_mng.maximum_charge_voltage',                 rct_id.t_float,   ''))
    id_tab.append(rct_id(0x5939EC5D, 311, 'battery.module_sn[6]',                             rct_id.t_string,  'Module 6 Serial Number'))
    id_tab.append(rct_id(0x5952E5E6, 312, 'wifi.mask',                                        rct_id.t_string,  'Netmask'))
    id_tab.append(rct_id(0x5A120CE4, 313, 'battery.cells_stat[1].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[1].t_max.time'))
    id_tab.append(rct_id(0x5A316247, 314, 'wifi.mode',                                        rct_id.t_string,  'WiFi mode'))
    id_tab.append(rct_id(0x5A9EEFF0, 315, 'battery.stack_cycles[4]',                          rct_id.t_uint16,  'battery.stack_cycles[4]'))
    id_tab.append(rct_id(0x5AF50FD7, 316, 'battery.cells_stat[4].t_min.value',                rct_id.t_float,   'battery.cells_stat[4].t_min.value'))
    id_tab.append(rct_id(0x5B10CE81, 317, 'power_mng.is_heiphoss',                            rct_id.t_uint8,   'HeiPhoss mode'))
    id_tab.append(rct_id(0x5BA122A5, 318, 'battery.stack_cycles[2]',                          rct_id.t_uint16,  'battery.stack_cycles[2]'))
    id_tab.append(rct_id(0x5BB8075A, 319, 'dc_conv.dc_conv_struct[1].u_sg_lp',                rct_id.t_float,   'Solar generator B voltage [V]'))
    id_tab.append(rct_id(0x5BD2DB45, 320, 'io_board.io1_s0_imp_per_kwh',                      rct_id.t_int16,   'Number of impulses per kWh for S0 signal on I/O 1'))
    id_tab.append(rct_id(0x5C93093B, 321, 'battery_placeholder[0].status2',                   rct_id.t_int32,   'Battery extra status'))
    id_tab.append(rct_id(0x5CD75669, 322, 'db.power_board.afi_t150',                          rct_id.t_float,   'AFI 150 mA switching off time [s]'))
    id_tab.append(rct_id(0x5D0CDCF0, 323, 'p_rec_available[2]',                               rct_id.t_float,   'Available Pac [W]'))
    id_tab.append(rct_id(0x5D1B0835, 324, 'net.use_network_filter',                           rct_id.t_bool,    'net.use_network_filter'))
    id_tab.append(rct_id(0x5D34D09D, 325, 'logger.month_egrid_load_log_ts',                   rct_id.t_int32,   'logger.month_egrid_load_log_ts'))
    id_tab.append(rct_id(0x5E540FB2, 326, 'net.update_slaves',                                rct_id.t_bool,    'Activate aut. update slaves'))
    id_tab.append(rct_id(0x5E942C62, 327, 'dc_conv.dc_conv_struct[1].mpp.fixed_voltage',      rct_id.t_float,   'Fixed voltage Solar generator B [V]'))
    id_tab.append(rct_id(0x5EE03C45, 328, 'io_board.alarm_home_relay_mode',                   rct_id.t_enum,    'Multifunctional relay usage'))
    id_tab.append(rct_id(0x5EF54372, 329, 'battery_placeholder[0].cells_stat[0].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[0].u_max.index'))
    id_tab.append(rct_id(0x5F33284E, 330, 'prim_sm.state',                                    rct_id.t_uint8,   'Inverter status'))
    id_tab.append(rct_id(0x6002891F, 331, 'g_sync.p_ac_sc_sum',                               rct_id.t_float,   'Grid power (ext. sensors) [W]'))
    id_tab.append(rct_id(0x60435F1C, 332, 'battery_placeholder[0].cells[6]',                  rct_id.t_string,  'battery_placeholder[0].cells[6]'))
    id_tab.append(rct_id(0x60749E5E, 333, 'battery.cells_stat[6].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[6].u_min.time'))
    id_tab.append(rct_id(0x60A9A532, 334, 'logger.day_eext_log_ts',                           rct_id.t_int32,   'logger.day_eext_log_ts'))
    id_tab.append(rct_id(0x612F7EAB, 335, 'g_sync.s_ac[1]',                                   rct_id.t_float,   'Apparent power phase 2 [VA]'))
    id_tab.append(rct_id(0x61EAC702, 336, 'battery.cells_stat[0].t_min.value',                rct_id.t_float,   'battery.cells_stat[0].t_min.value'))
    id_tab.append(rct_id(0x6213589B, 337, 'battery.cells_stat[6].u_min.value',                rct_id.t_float,   'battery.cells_stat[6].u_min.value'))
    id_tab.append(rct_id(0x6279F2A3, 338, 'db.power_board.version_boot',                      rct_id.t_uint32,  'PIC bootloader software version'))
    id_tab.append(rct_id(0x62B8940B, 339, 'dc_conv.start_voltage',                            rct_id.t_float,   'Inverter DC-voltage start value [V]'))
    id_tab.append(rct_id(0x62D645D9, 340, 'battery.cells[5]',                                 rct_id.t_string,  'battery.cells[5]'))
    id_tab.append(rct_id(0x62FBE7DC, 341, 'energy.e_grid_load_total',                         rct_id.t_float,   'Total energy grid load [Wh]'))
    id_tab.append(rct_id(0x63476DBE, 342, 'g_sync.u_ptp_rms[0]',                              rct_id.t_float,   'Phase to phase voltage 1 [V]'))
    id_tab.append(rct_id(0x6383DEA9, 343, 'battery_placeholder[0].cells_stat[1].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[1].t_max.value'))
    id_tab.append(rct_id(0x6388556C, 344, 'battery.stack_software_version[0]',                rct_id.t_uint32,  'Software version stack 0'))
    id_tab.append(rct_id(0x6445D856, 345, 'battery.cells_stat[1].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[1].u_min.index'))
    id_tab.append(rct_id(0x6476A836, 346, 'dc_conv.dc_conv_struct[0].mpp.enable_scan',        rct_id.t_bool,    'Enable rescan for global MPP on solar generator A'))
    id_tab.append(rct_id(0x649B10DA, 347, 'battery.cells_resist[0]',                          rct_id.t_string,  'battery.cells_resist[0]'))
    id_tab.append(rct_id(0x650C1ED7, 348, 'g_sync.i_dr_eff[1]',                               rct_id.t_float,   'Current phase 2 [A]'))
    id_tab.append(rct_id(0x652B7536, 349, 'battery_placeholder[0].cells_stat[3].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[3].t_min.index'))
    id_tab.append(rct_id(0x6599E3D3, 350, 'power_mng.schedule[3]',                            rct_id.t_string,  'power_mng.schedule[3]'))
    id_tab.append(rct_id(0x65A44A98, 351, 'flash_mem',                                        rct_id.t_string,  'flash_mem'))
    id_tab.append(rct_id(0x65B624AB, 352, 'energy.e_grid_feed_month',                         rct_id.t_float,   'Month energy grid feed-in [Wh]'))
    id_tab.append(rct_id(0x65EED11B, 353, 'battery.voltage',                                  rct_id.t_float,   'Battery voltage [V]'))
    id_tab.append(rct_id(0x663F1452, 354, 'power_mng.n_batteries',                            rct_id.t_uint8,   'power_mng.n_batteries'))
    id_tab.append(rct_id(0x664A1326, 355, 'io_board.rse_table[14]',                           rct_id.t_float,   'K4..K1: 1110'))
    id_tab.append(rct_id(0x669D02FE, 356, 'logger.minutes_eac_log_ts',                        rct_id.t_int32,   'logger.minutes_eac_log_ts'))
    id_tab.append(rct_id(0x6709A2F4, 357, 'energy.e_ac_year_sum',                             rct_id.t_float,   'energy.e_ac_year_sum'))
    id_tab.append(rct_id(0x672552DC, 358, 'power_mng.bat_calib_days_in_advance',              rct_id.t_uint8,   'Battery calibration days in advance'))
    id_tab.append(rct_id(0x6743CCCE, 359, 'battery_placeholder[0].cells_stat[6].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[6].t_max.index'))
    id_tab.append(rct_id(0x675776B1, 360, 'dc_conv.dc_conv_struct[1].u_target',               rct_id.t_float,   'MPP on input B [V]'))
    id_tab.append(rct_id(0x67BF3003, 361, 'display_struct.display_dir',                       rct_id.t_bool,    'Rotate display'))
    id_tab.append(rct_id(0x67C0A2F5, 362, 'net.slave_p_total',                                rct_id.t_float,   'net.slave_p_total'))
    id_tab.append(rct_id(0x682CDDA1, 363, 'power_mng.battery_type',                           rct_id.t_enum,    ''))
    id_tab.append(rct_id(0x6830F6E4, 364, 'io_board.rse_table[9]',                            rct_id.t_float,   'K4..K1: 1001'))
    id_tab.append(rct_id(0x68BA92E1, 365, 'io_board.io2_s0_imp_per_kwh',                      rct_id.t_int16,   'Number of impulses per kWh for S0 signal on I/O 2'))
    id_tab.append(rct_id(0x68BC034D, 366, 'parameter_file',                                   rct_id.t_string,  'Norm'))
    id_tab.append(rct_id(0x68EEFD3D, 367, 'energy.e_dc_total[1]',                             rct_id.t_float,   'Solar generator B total energy [Wh]'))
    id_tab.append(rct_id(0x690C32D2, 368, 'battery_placeholder[0].module_sn[0]',              rct_id.t_string,  'Module 0 Serial Number'))
    id_tab.append(rct_id(0x6974798A, 369, 'battery.stack_software_version[6]',                rct_id.t_uint32,  'Software version stack 6'))
    id_tab.append(rct_id(0x69AA598A, 370, 'can_bus.requested_id',                             rct_id.t_int32,   'can_bus.requested_id'))
    id_tab.append(rct_id(0x69B8FF28, 371, 'battery.cells[2]',                                 rct_id.t_string,  'battery.cells[2]'))
    id_tab.append(rct_id(0x6B5A56C2, 372, 'logger.month_eb_log_ts',                           rct_id.t_int32,   'logger.month_eb_log_ts'))
    id_tab.append(rct_id(0x6BA10831, 373, 'db.power_board.afi_i30',                           rct_id.t_float,   'AFI 30 mA threshold [A]'))
    id_tab.append(rct_id(0x6BBDC7C8, 374, 'line_mon.u_max',                                   rct_id.t_float,   'Max line voltage [V]'))
    id_tab.append(rct_id(0x6BFF1AF4, 375, 'hw_test.bt_power[2]',                              rct_id.t_float,   'hw_test.bt_power[2]'))
    id_tab.append(rct_id(0x6C03F5ED, 376, 'battery_placeholder[0].bms_power_version',         rct_id.t_uint32,  'Software version BMS Power'))
    id_tab.append(rct_id(0x6C10E96A, 377, 'battery_placeholder[0].cells_stat[0].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[0].u_min.time'))
    id_tab.append(rct_id(0x6C243F71, 378, 'modbus.address',                                   rct_id.t_uint8,   'RS485 address'))
    id_tab.append(rct_id(0x6C2D00E4, 379, 'io_board.rse_table[1]',                            rct_id.t_float,   'K4..K1: 0001'))
    id_tab.append(rct_id(0x6C44F721, 380, 'i_dc_max',                                         rct_id.t_float,   'Max. DC-component of Iac [A]'))
    id_tab.append(rct_id(0x6CFCD774, 381, 'energy.e_dc_year_sum[1]',                          rct_id.t_float,   'energy.e_dc_year_sum[1]'))
    id_tab.append(rct_id(0x6D5318C8, 382, 'cs_map[1]',                                        rct_id.t_uint8,   'Associate current sensor 1 with phase L'))
    id_tab.append(rct_id(0x6D639C25, 383, 'battery_placeholder[0].cells_stat[0].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[0].t_min.value'))
    id_tab.append(rct_id(0x6D7C0BF4, 384, 'wifi.sockb_port',                                  rct_id.t_int32,   'Port'))
    id_tab.append(rct_id(0x6DB1FDDC, 385, 'battery.cells_stat[4].u_min.value',                rct_id.t_float,   'battery.cells_stat[4].u_min.value'))
    id_tab.append(rct_id(0x6DCC4097, 386, 'net.master_timeout',                               rct_id.t_float,   'net.master_timeout'))
    id_tab.append(rct_id(0x6E1C5B78, 387, 'g_sync.p_ac_lp[1]',                                rct_id.t_float,   'AC power phase 2 [W]'))
    id_tab.append(rct_id(0x6E24632E, 388, 'battery.cells_stat[5].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[5].u_max.time'))
    id_tab.append(rct_id(0x6E3336A8, 389, 'battery_placeholder[0].cells_stat[5].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[5].t_max.index'))
    id_tab.append(rct_id(0x6E491B50, 390, 'battery.maximum_charge_voltage',                   rct_id.t_float,   'Max. charge voltage [V]'))
    id_tab.append(rct_id(0x6F3876BC, 391, 'logger.error_log_time_stamp',                      rct_id.t_int32,   'Time stamp for error log reading'))
    id_tab.append(rct_id(0x6FB2E2BF, 392, 'db.power_board.afi_i150',                          rct_id.t_float,   'AFI 150 mA threshold [A]'))
    id_tab.append(rct_id(0x6FD36B32, 393, 'rb485.f_wr[1]',                                    rct_id.t_float,   'Power Storage phase 2 frequency [Hz]'))
    id_tab.append(rct_id(0x6FF4BD55, 394, 'energy.e_ext_month_sum',                           rct_id.t_float,   'energy.e_ext_month_sum'))
    id_tab.append(rct_id(0x701A0482, 395, 'dc_conv.dc_conv_struct[0].enabled',                rct_id.t_bool,    'Solar generator A connected'))
    id_tab.append(rct_id(0x70349444, 396, 'battery.cells_stat[1].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[1].t_min.index'))
    id_tab.append(rct_id(0x70A2AF4F, 397, 'battery.bat_status',                               rct_id.t_int32,   'battery.bat_status'))
    id_tab.append(rct_id(0x70BD7C46, 398, 'logger.year_eac_log_ts',                           rct_id.t_int32,   'logger.year_eac_log_ts'))
    id_tab.append(rct_id(0x70E28322, 399, 'grid_mon[0].f_under.time',                         rct_id.t_float,   'Min. frequency switch-off time level 1 [s]'))
    id_tab.append(rct_id(0x71196579, 400, 'battery.cells_stat[5].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[5].t_min.index'))
    id_tab.append(rct_id(0x71277E71, 401, 'frt.u_min_begin',                                  rct_id.t_float,   'FRT begin undervoltage threshold [V]'))
    id_tab.append(rct_id(0x71465EAF, 402, 'nsm.cos_phi_ts',                                   rct_id.t_float,   'Time const for filter [s]'))
    id_tab.append(rct_id(0x715C84A1, 403, 'adc.u_ref_1_5v[2]',                                rct_id.t_uint16,  'Reference voltage 3 [V]'))
    id_tab.append(rct_id(0x71765BD8, 404, 'battery.status',                                   rct_id.t_int32,   'Battery status'))
    id_tab.append(rct_id(0x71B70DCE, 405, 'hw_test.bt_power[4]',                              rct_id.t_float,   'hw_test.bt_power[4]'))
    id_tab.append(rct_id(0x71CB0B57, 406, 'battery.cells_resist[1]',                          rct_id.t_string,  'battery.cells_resist[1]'))
    id_tab.append(rct_id(0x71E10B51, 407, 'g_sync.p_ac_lp[0]',                                rct_id.t_float,   'AC power phase 1 [W]'))
    id_tab.append(rct_id(0x7232F7AF, 408, 'nsm.apm',                                          rct_id.t_enum,    'nsm.apm'))
    id_tab.append(rct_id(0x7268CE4D, 409, 'battery.inv_cmd',                                  rct_id.t_uint32,  'battery.inv_cmd'))
    id_tab.append(rct_id(0x72ACC0BF, 410, 'logger.minutes_ua_log_ts',                         rct_id.t_int32,   'logger.minutes_ua_log_ts'))
    id_tab.append(rct_id(0x7301A5A7, 411, 'flash_rtc.time_stamp_factory',                     rct_id.t_uint32,  'Production date'))
    id_tab.append(rct_id(0x73489528, 412, 'battery.module_sn[2]',                             rct_id.t_string,  'Module 2 Serial Number'))
    id_tab.append(rct_id(0x73E3ED49, 413, 'prim_sm.island_max_trials',                        rct_id.t_uint16,  'Max island trials'))
    id_tab.append(rct_id(0x742966A6, 414, 'db.power_board.afi_i300',                          rct_id.t_float,   'AFI 300 mA threshold [A]'))
    id_tab.append(rct_id(0x74FD4609, 415, 'battery.cells_stat[2]',                            rct_id.t_string,  'battery.cells_stat[2]'))
    id_tab.append(rct_id(0x751E80CA, 416, 'prim_sm.island_reset_retrials_operation_time',     rct_id.t_float,   ''))
    id_tab.append(rct_id(0x75898A45, 417, 'battery_placeholder[0].cells_stat[5].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[5].t_max.time'))
    id_tab.append(rct_id(0x75AE19ED, 418, 'hw_test.hw_switch_time',                           rct_id.t_float,   'hw_test.hw_switch_time'))
    id_tab.append(rct_id(0x7689BE6A, 419, 'io_board.home_relay_sw_on_delay',                  rct_id.t_float,   'Switching on delay [s]'))
    id_tab.append(rct_id(0x76C9A0BD, 420, 'logger.minutes_soc_targ_log_ts',                   rct_id.t_int32,   'logger.minutes_soc_targ_log_ts'))
    id_tab.append(rct_id(0x76CAA9BF, 421, 'wifi.encryption_algorithm',                        rct_id.t_string,  'wifi.encryption_algorithm'))
    id_tab.append(rct_id(0x770A6E7C, 422, 'battery.cells_stat[0].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[0].u_max.index'))
    id_tab.append(rct_id(0x777DC0EB, 423, 'iso_struct.r_min',                                 rct_id.t_float,   'Minimum allowed insulation resistance [Ohm]'))
    id_tab.append(rct_id(0x77A9480F, 424, 'battery_placeholder[0].minimum_discharge_voltage', rct_id.t_float,   'Min. discharge voltage [V]'))
    id_tab.append(rct_id(0x77DD4364, 425, 'hw_test.bt_time[5]',                               rct_id.t_float,   'hw_test.bt_time[5]'))
    id_tab.append(rct_id(0x77E5CEF1, 426, 'battery_placeholder[0].stack_software_version[0]', rct_id.t_uint32,  'Software version stack 0'))
    id_tab.append(rct_id(0x78228507, 427, 'battery_placeholder[0].stack_cycles[6]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[6]'))
    id_tab.append(rct_id(0x7839EBCB, 428, 'battery_placeholder[0].cells_stat[3].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[3].u_min.time'))
    id_tab.append(rct_id(0x7924ABD9, 429, 'inverter_sn',                                      rct_id.t_string,  'Serial number'))
    id_tab.append(rct_id(0x792897C9, 430, 'battery_placeholder[0].cells_stat[4].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[4].t_min.time'))
    id_tab.append(rct_id(0x792A7B79, 431, 'io_board.s0_direction',                            rct_id.t_enum,    'S0 inputs single or bidirectional'))
    id_tab.append(rct_id(0x7940547B, 432, 'inv_struct.force_dh',                              rct_id.t_bool,    'inv_struct.force_dh'))
    id_tab.append(rct_id(0x7946D888, 433, 'i_dc_slow_time',                                   rct_id.t_float,   'Time for slow DC-component of Iac [s]'))
    id_tab.append(rct_id(0x79C0A724, 434, 'energy.e_ac_total_sum',                            rct_id.t_float,   'energy.e_ac_total_sum'))
    id_tab.append(rct_id(0x79D7D617, 435, 'battery_placeholder[0].current',                   rct_id.t_float,   'Battery current [A]'))
    id_tab.append(rct_id(0x79E66CDF, 436, 'battery_placeholder[0].cells_stat[6].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[6].t_min.index'))
    id_tab.append(rct_id(0x7A5C91F8, 437, 'nsm.p_u[1][0]',                                    rct_id.t_float,   'Point 2 P/Pn'))
    id_tab.append(rct_id(0x7A67E33B, 438, 'can_bus.bms_update_response[1]',                   rct_id.t_uint32,  'can_bus.bms_update_response[1]'))
    id_tab.append(rct_id(0x7A9091EA, 439, 'rb485.u_l_grid[1]',                                rct_id.t_float,   'Grid phase 2 voltage [V]'))
    id_tab.append(rct_id(0x7AB9B045, 440, 'energy.e_dc_month[1]',                             rct_id.t_float,   'Solar generator B month energy [Wh]'))
    id_tab.append(rct_id(0x7AE87E39, 441, 'partition[2].last_id',                             rct_id.t_int32,   'partition[2].last_id'))
    id_tab.append(rct_id(0x7AF0AD03, 442, 'power_mng.schedule[9]',                            rct_id.t_string,  'power_mng.schedule[9]'))
    id_tab.append(rct_id(0x7AF779C1, 443, 'nsm.pu_mode',                                      rct_id.t_bool,    'P(U) mode 0: Pn 1: Pload'))
    id_tab.append(rct_id(0x7B1F7FBE, 444, 'wifi.gateway',                                     rct_id.t_string,  'Gateway'))
    id_tab.append(rct_id(0x7B8E811E, 445, 'battery_placeholder[0].cells_stat[6]',             rct_id.t_string,  'battery_placeholder[0].cells_stat[6]'))
    id_tab.append(rct_id(0x7BF3886B, 446, 'battery_placeholder[0].stack_cycles[2]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[2]'))
    id_tab.append(rct_id(0x7C0827C5, 447, 'partition[5].last_id',                             rct_id.t_int32,   'partition[5].last_id'))
    id_tab.append(rct_id(0x7C556C7A, 448, 'io_board.io2_polarity',                            rct_id.t_bool,    'Inverted signal on input I/O 2'))
    id_tab.append(rct_id(0x7C78CBAC, 449, 'g_sync.q_ac_sum_lp',                               rct_id.t_float,   'Reactive power [var]'))
    id_tab.append(rct_id(0x7C863EDB, 450, 'battery_placeholder[0].cells[3]',                  rct_id.t_string,  'battery_placeholder[0].cells[3]'))
    id_tab.append(rct_id(0x7D839AE6, 451, 'battery_placeholder[0].cells_resist[2]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[2]'))
    id_tab.append(rct_id(0x7DA7D8B6, 452, 'db.power_board.version_main',                      rct_id.t_uint32,  'PIC software version'))
    id_tab.append(rct_id(0x7DDE352B, 453, 'wifi.sockb_ip',                                    rct_id.t_string,  'wifi.sockb_ip'))
    id_tab.append(rct_id(0x7E096024, 454, 'energy.e_load_total_sum',                          rct_id.t_float,   'energy.e_load_total_sum'))
    id_tab.append(rct_id(0x7E590128, 455, 'battery.cells_stat[0].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[0].u_max.time'))
    id_tab.append(rct_id(0x7E75B17A, 456, 'nsm.q_u_max_u_high_rel',                           rct_id.t_float,   'Qmax at upper voltage level relative to Smax (positive = overexcited)'))
    id_tab.append(rct_id(0x7F42BB82, 457, 'battery.cells_stat[6].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[6].u_max.index'))
    id_tab.append(rct_id(0x7F813D73, 458, 'fault[3].flt',                                     rct_id.t_uint32,  'Error bit field 4'))
    id_tab.append(rct_id(0x7FF6252C, 459, 'battery.cells_stat[5].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[5].t_max.time'))
    id_tab.append(rct_id(0x804A3266, 460, 'battery.cells_stat[6].u_max.value',                rct_id.t_float,   'battery.cells_stat[6].u_max.value'))
    id_tab.append(rct_id(0x80835476, 461, 'db.power_board.adc_p5V_W_meas',                    rct_id.t_float,   'db.power_board.adc_p5V_W_meas'))
    id_tab.append(rct_id(0x8128228D, 462, 'battery_placeholder[0].cells_stat[1].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[1].u_max.value'))
    id_tab.append(rct_id(0x812E5ADD, 463, 'energy.e_dc_total_sum[1]',                         rct_id.t_float,   'energy.e_dc_total_sum[1]'))
    id_tab.append(rct_id(0x8160539D, 464, 'battery.cells_stat[4].t_max.value',                rct_id.t_float,   'battery.cells_stat[4].t_max.value'))
    id_tab.append(rct_id(0x81AE960B, 465, 'energy.e_dc_month[0]',                             rct_id.t_float,   'Solar generator A month energy [Wh]'))
    id_tab.append(rct_id(0x81AF854E, 466, 'nsm.pu_use',                                       rct_id.t_bool,    'P(U) active'))
    id_tab.append(rct_id(0x82258C01, 467, 'cs_neg[0]',                                        rct_id.t_float,   'Miltiply value of the current sensor 0 by'))
    id_tab.append(rct_id(0x82CD1525, 468, 'grid_mon[1].u_under.threshold',                    rct_id.t_float,   'Min. voltage level 2 [V]'))
    id_tab.append(rct_id(0x82E3C121, 469, 'g_sync.q_ac[1]',                                   rct_id.t_float,   ''))
    id_tab.append(rct_id(0x8320B84C, 470, 'io_board.rse_data_delay',                          rct_id.t_float,   'Delay for new K4..K1 data [s]'))
    id_tab.append(rct_id(0x8352F9DD, 471, 'battery_placeholder[0].cells_stat[4].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[4].t_min.value'))
    id_tab.append(rct_id(0x83A5333A, 472, 'nsm.cos_phi_p[0][0]',                              rct_id.t_float,   'Point 1 [P/Pn]'))
    id_tab.append(rct_id(0x83BBEF0B, 473, 'frt.u_max_begin',                                  rct_id.t_float,   'FRT begin overvoltage threshold [V]'))
    id_tab.append(rct_id(0x84ABE3D8, 474, 'energy.e_grid_feed_year_sum',                      rct_id.t_float,   'energy.e_grid_feed_year_sum'))
    id_tab.append(rct_id(0x85886E2E, 475, 'p_rec_lim[0]',                                     rct_id.t_float,   'Max. compensation power [W]'))
    id_tab.append(rct_id(0x8594D11E, 476, 'battery_placeholder[0].module_sn[6]',              rct_id.t_string,  'Module 6 Serial Number'))
    id_tab.append(rct_id(0x86782D58, 477, 'hw_test.bt_power[9]',                              rct_id.t_float,   'hw_test.bt_power[9]'))
    id_tab.append(rct_id(0x867DEF7D, 478, 'energy.e_grid_load_day',                           rct_id.t_float,   'Day energy grid load [Wh]'))
    id_tab.append(rct_id(0x872F380B, 479, 'io_board.load_set',                                rct_id.t_float,   'Dummy household load [W]'))
    id_tab.append(rct_id(0x87E4387A, 480, 'current_sensor_max',                               rct_id.t_float,   'Power Sensor current range [A]'))
    id_tab.append(rct_id(0x8822EF35, 481, 'battery_placeholder[0].stack_software_version[2]', rct_id.t_uint32,  'Software version stack 2'))
    id_tab.append(rct_id(0x883DE9AB, 482, 'g_sync.s_ac_lp[2]',                                rct_id.t_float,   'Apparent power phase 3 [VA]'))
    id_tab.append(rct_id(0x885BB57E, 483, 'battery.cells_stat[6].t_min.value',                rct_id.t_float,   'battery.cells_stat[6].t_min.value'))
    id_tab.append(rct_id(0x887D43C4, 484, 'g_sync.i_dr_lp[0]',                                rct_id.t_float,   'Current phase 1 (average) [A]'))
    id_tab.append(rct_id(0x889DC27F, 485, 'battery.cells_stat[0].u_min.value',                rct_id.t_float,   'battery.cells_stat[0].u_min.value'))
    id_tab.append(rct_id(0x88BBF8CB, 486, 'battery.cells_stat[5].t_min.value',                rct_id.t_float,   'battery.cells_stat[5].t_min.value'))
    id_tab.append(rct_id(0x88C9707B, 487, 'io_board.rse_table[15]',                           rct_id.t_float,   'K4..K1: 1111'))
    id_tab.append(rct_id(0x88DEBCFE, 488, 'nsm.q_u_max_u_high',                               rct_id.t_float,   'Qmax at upper voltage level [var] (positive = overexcited)'))
    id_tab.append(rct_id(0x88DFDE8B, 489, 'frt.u_max_end',                                    rct_id.t_float,   'FRT end overvoltage threshold [V]'))
    id_tab.append(rct_id(0x88F36D45, 490, 'io_board.rse_data',                                rct_id.t_uint8,   'Actual K4..K1 data'))
    id_tab.append(rct_id(0x89B21223, 491, 'frt.t_max[0]',                                     rct_id.t_float,   'Point 1 time [s]'))
    id_tab.append(rct_id(0x89B25F4B, 492, 'battery.stack_cycles[3]',                          rct_id.t_uint16,  'battery.stack_cycles[3]'))
    id_tab.append(rct_id(0x89EE3EB5, 493, 'g_sync.i_dr_eff[0]',                               rct_id.t_float,   'Current phase 1 [A]'))
    id_tab.append(rct_id(0x8A18539B, 494, 'g_sync.u_zk_sum_avg',                              rct_id.t_float,   'DC link voltage [V]'))
    id_tab.append(rct_id(0x8AFD1410, 495, 'battery_placeholder[0].stack_cycles[4]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[4]'))
    id_tab.append(rct_id(0x8B4BE168, 496, 'battery_placeholder[0].soc',                       rct_id.t_float,   'SOC (State of charge)'))
    id_tab.append(rct_id(0x8B9FF008, 497, 'battery.soc_target',                               rct_id.t_float,   'Target SOC'))
    id_tab.append(rct_id(0x8BB08839, 498, 'battery.cells_stat[6].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[6].t_min.time'))
    id_tab.append(rct_id(0x8C6E28E4, 499, 'battery_placeholder[0].cells_stat[2].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[2].t_max.time'))
    id_tab.append(rct_id(0x8CA00014, 500, 'wifi.result',                                      rct_id.t_int8,    'WiFi result'))
    id_tab.append(rct_id(0x8D33B6BC, 501, 'nsm.f_low_exit',                                   rct_id.t_float,   'Exit frequency for P(f) under-frequency mode [Hz]'))
    id_tab.append(rct_id(0x8D8E19F7, 502, 'line_mon.u_min',                                   rct_id.t_float,   'Min line voltage [V]'))
    id_tab.append(rct_id(0x8DD1C728, 503, 'dc_conv.dc_conv_struct[1].mpp.enable_scan',        rct_id.t_bool,    'Enable rescan for global MPP on solar generator B'))
    id_tab.append(rct_id(0x8DFFDD33, 504, 'battery.cells_stat[3].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[3].u_min.time'))
    id_tab.append(rct_id(0x8E41FC47, 505, 'iso_struct.Rp',                                    rct_id.t_float,   'Insulation resistance on positive DC input [Ohm]'))
    id_tab.append(rct_id(0x8EBF9574, 506, 'power_mng.soc_min_island',                         rct_id.t_float,   'Min SOC target (island)'))
    id_tab.append(rct_id(0x8EC23427, 507, 'battery.cells_stat[4].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[4].u_max.time'))
    id_tab.append(rct_id(0x8EC4116E, 508, 'display_struct.blink',                             rct_id.t_bool,    'Display blinking enable'))
    id_tab.append(rct_id(0x8EF6FBBD, 509, 'battery.cells[1]',                                 rct_id.t_string,  'battery.cells[1]'))
    id_tab.append(rct_id(0x8EF9C9B8, 510, 'battery.cells_stat[6].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[6].t_max.time'))
    id_tab.append(rct_id(0x8F0FF9F3, 511, 'p_rec_available[1]',                               rct_id.t_float,   'Available battery to grid power [W]'))
    id_tab.append(rct_id(0x8FC89B10, 512, 'com_service',                                      rct_id.t_enum,    'COM service'))
    id_tab.append(rct_id(0x902AFAFB, 513, 'battery.temperature',                              rct_id.t_float,   'Battery temperature [?C]'))
    id_tab.append(rct_id(0x903FE89E, 514, 'hw_test.bt_time[8]',                               rct_id.t_float,   'hw_test.bt_time[8]'))
    id_tab.append(rct_id(0x905F707B, 515, 'rb485.f_wr[2]',                                    rct_id.t_float,   'Power Storage phase 3 frequency [Hz]'))
    id_tab.append(rct_id(0x9061EA7B, 516, 'grid_lt.granularity',                              rct_id.t_float,   'Resolution'))
    id_tab.append(rct_id(0x907CD1DF, 517, 'wifi.connect_service_max_duration',                rct_id.t_int32,   'Service connection max duration [s]'))
    id_tab.append(rct_id(0x90832471, 518, 'battery.cells_stat[1].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[1].u_max.time'))
    id_tab.append(rct_id(0x9095FD74, 519, 'battery_placeholder[0].cells[5]',                  rct_id.t_string,  'battery_placeholder[0].cells[5]'))
    id_tab.append(rct_id(0x90B53336, 520, 'temperature.sink_temp_power_reduction',            rct_id.t_float,   'Heat sink temperature target [?C]'))
    id_tab.append(rct_id(0x90C2AC13, 521, 'battery_placeholder[0].stack_cycles[3]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[3]'))
    id_tab.append(rct_id(0x90F123FA, 522, 'io_board.io1_usage',                               rct_id.t_enum,    ''))
    id_tab.append(rct_id(0x915CD4A4, 523, 'grid_mon[1].f_over.threshold',                     rct_id.t_float,   'Max. frequency level 2 [Hz]'))
    id_tab.append(rct_id(0x91617C58, 524, 'g_sync.p_ac_grid_sum_lp',                          rct_id.t_float,   'Total grid power [W]'))
    id_tab.append(rct_id(0x917E3622, 525, 'energy.e_ext_year',                                rct_id.t_float,   'External year energy [Wh]'))
    id_tab.append(rct_id(0x91C325D9, 526, 'battery.cells_stat[0].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[0].t_min.time'))
    id_tab.append(rct_id(0x91FB68CD, 527, 'battery.cells_stat[6].t_max.value',                rct_id.t_float,   'battery.cells_stat[6].t_max.value'))
    id_tab.append(rct_id(0x920AFF34, 528, 'battery_placeholder[0].cells_stat[1].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[1].t_max.index'))
    id_tab.append(rct_id(0x9214A00C, 529, 'hw_test.booster_test_index',                       rct_id.t_uint8,   'hw_test.booster_test_index'))
    id_tab.append(rct_id(0x921997EE, 530, 'logger.month_egrid_feed_log_ts',                   rct_id.t_int32,   'logger.month_egrid_feed_log_ts'))
    id_tab.append(rct_id(0x9247DB99, 531, 'logger.minutes_egrid_load_log_ts',                 rct_id.t_int32,   'logger.minutes_egrid_load_log_ts'))
    id_tab.append(rct_id(0x929394B7, 532, 'svnversion_last_known',                            rct_id.t_string,  'svnversion_last_known'))
    id_tab.append(rct_id(0x92BC682B, 533, 'g_sync.i_dr_eff[2]',                               rct_id.t_float,   'Current phase 3 [A]'))
    id_tab.append(rct_id(0x933F9A24, 534, 'grid_mon[0].f_over.time',                          rct_id.t_float,   'Max. frequency switch-off time level 1 [s]'))
    id_tab.append(rct_id(0x934E64E9, 535, 'switch_on_cond.u_max',                             rct_id.t_float,   'Max. voltage'))
    id_tab.append(rct_id(0x9350FE02, 536, 'frt.u_max[2]',                                     rct_id.t_float,   'Point 3 voltage [V]'))
    id_tab.append(rct_id(0x93971C36, 537, 'frt.t_max[2]',                                     rct_id.t_float,   'Point 3 time [s]'))
    id_tab.append(rct_id(0x93C0C2E2, 538, 'power_mng.bat_calib_reqularity',                   rct_id.t_uint32,  'Battery calibration interval [days]'))
    id_tab.append(rct_id(0x93E6918D, 539, 'nsm.f_exit',                                       rct_id.t_float,   'Exit frequency for P(f) over-frequency mode [Hz]'))
    id_tab.append(rct_id(0x93F976AB, 540, 'rb485.u_l_grid[0]',                                rct_id.t_float,   'Grid phase 1 voltage [V]'))
    id_tab.append(rct_id(0x940569AC, 541, 'hw_test.bt_time[6]',                               rct_id.t_float,   'hw_test.bt_time[6]'))
    id_tab.append(rct_id(0x947DDC38, 542, 'battery_placeholder[0].cells_stat[0].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[0].t_min.index'))
    id_tab.append(rct_id(0x9486134F, 543, 'battery_placeholder[0].cells_stat[1].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[1].t_max.time'))
    id_tab.append(rct_id(0x9558AD8A, 544, 'rb485.f_grid[0]',                                  rct_id.t_float,   'Grid phase1 frequency [Hz]'))
    id_tab.append(rct_id(0x959930BF, 545, 'battery.soc',                                      rct_id.t_float,   'SOC (State of charge)'))
    id_tab.append(rct_id(0x95E1E844, 546, 'battery_placeholder[0].cells_stat[2].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[2].t_min.time'))
    id_tab.append(rct_id(0x961C8261, 547, 'battery_placeholder[0].cells_stat[4].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[4].u_max.time'))
    id_tab.append(rct_id(0x96629BB9, 548, 'can_bus.bms_update_state',                         rct_id.t_uint8,   'can_bus.bms_update_state'))
    id_tab.append(rct_id(0x9680077F, 549, 'nsm.cos_phi_p[2][0]',                              rct_id.t_float,   'Point 3 [P/Pn]'))
    id_tab.append(rct_id(0x96E32D11, 550, 'flash_param.erase_cycles',                         rct_id.t_uint32,  'Erase cycles of flash parameter'))
    id_tab.append(rct_id(0x972B3029, 551, 'power_mng.stop_discharge_voltage_buffer',          rct_id.t_float,   'Stop discharge voltage buffer [V]'))
    id_tab.append(rct_id(0x97997C93, 552, 'power_mng.soc_max',                                rct_id.t_float,   'Max SOC target'))
    id_tab.append(rct_id(0x97DC2ECB, 553, 'battery_placeholder[0].cells[1]',                  rct_id.t_string,  'battery_placeholder[0].cells[1]'))
    id_tab.append(rct_id(0x97E203F9, 554, 'power_mng.is_grid',                                rct_id.t_bool,    'power_mng.is_grid'))
    id_tab.append(rct_id(0x97E3A6F2, 555, 'power_mng.u_acc_lp',                               rct_id.t_float,   'Battery voltage (inverter) [V]'))
    id_tab.append(rct_id(0x980C5525, 556, 'battery_placeholder[0].max_cell_voltage',          rct_id.t_float,   'battery_placeholder[0].max_cell_voltage'))
    id_tab.append(rct_id(0x98ACC1B8, 557, 'io_board.rse_table[4]',                            rct_id.t_float,   'K4..K1: 0100'))
    id_tab.append(rct_id(0x99396810, 558, 'battery.module_sn[1]',                             rct_id.t_string,  'Module 1 Serial Number'))
    id_tab.append(rct_id(0x993C06F6, 559, 'battery.cells_resist[3]',                          rct_id.t_string,  'battery.cells_resist[3]'))
    id_tab.append(rct_id(0x9981F1AC, 560, 'db.power_board.adc_m9V_meas',                      rct_id.t_float,   'db.power_board.adc_m9V_meas'))
    id_tab.append(rct_id(0x99EE89CB, 561, 'power_mng.power_lim_src_index',                    rct_id.t_enum,    'Power limit source'))
    id_tab.append(rct_id(0x9A33F9B7, 562, 'power_mng.schedule[5]',                            rct_id.t_string,  'power_mng.schedule[5]'))
    id_tab.append(rct_id(0x9A51A23B, 563, 'logger.log_rate',                                  rct_id.t_uint16,  'Data log resolution [s]'))
    id_tab.append(rct_id(0x9A67600D, 564, 'p_rec_lim[2]',                                     rct_id.t_float,   'Pac max. [W]'))
    id_tab.append(rct_id(0x9AAA9CAA, 565, 'battery_placeholder[0].stack_cycles[5]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[5]'))
    id_tab.append(rct_id(0x9B92023F, 566, 'io_board.rse_table[7]',                            rct_id.t_float,   'K4..K1: 0111'))
    id_tab.append(rct_id(0x9C75BD89, 567, 'frt.t_min[0]',                                     rct_id.t_float,   'Point 1 time [s]'))
    id_tab.append(rct_id(0x9C8FE559, 568, 'pas.period',                                       rct_id.t_uint32,  'pas.period'))
    id_tab.append(rct_id(0x9D785E8C, 569, 'battery.bms_software_version',                     rct_id.t_uint32,  'Software version BMS Master'))
    id_tab.append(rct_id(0x9DC927AA, 570, 'bat_mng_struct.profile_load',                      rct_id.t_string,  'bat_mng_struct.profile_load'))
    id_tab.append(rct_id(0x9E1A88F5, 571, 'dc_conv.dc_conv_struct[0].mpp.fixed_voltage',      rct_id.t_float,   'Fixed voltage Solar generator A [V]'))
    id_tab.append(rct_id(0x9E314430, 572, 'battery.cells_stat[2].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[2].u_max.time'))
    id_tab.append(rct_id(0x9F52F968, 573, 'power_mng.feed_asymmetrical',                      rct_id.t_bool,    'Allow asymmetrical feed'))
    id_tab.append(rct_id(0xA10D9A4B, 574, 'battery.min_cell_temperature',                     rct_id.t_float,   'battery.min_cell_temperature'))
    id_tab.append(rct_id(0xA1266D6B, 575, 'line_mon.time_lim',                                rct_id.t_float,   ''))
    id_tab.append(rct_id(0xA12BE39C, 576, 'energy.e_load_month_sum',                          rct_id.t_float,   'energy.e_load_month_sum'))
    id_tab.append(rct_id(0xA12E9B43, 577, 'phase_marker',                                     rct_id.t_int16,   'Next phase after phase 1'))
    id_tab.append(rct_id(0xA1D2B565, 578, 'wifi.service_port',                                rct_id.t_int32,   'wifi.service_port'))
    id_tab.append(rct_id(0xA23FE8B9, 579, 'battery_placeholder[0].cells_stat[6].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[6].t_min.value'))
    id_tab.append(rct_id(0xA2F87161, 580, 'battery_placeholder[0].cells_stat[0].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[0].u_max.time'))
    id_tab.append(rct_id(0xA305214D, 581, 'logger.buffer',                                    rct_id.t_string,  'logger.buffer'))
    id_tab.append(rct_id(0xA3393749, 582, 'io_board.check_start',                             rct_id.t_uint8,   'io_board.check_start'))
    id_tab.append(rct_id(0xA33D0954, 583, 'nsm.q_u_hysteresis',                               rct_id.t_bool,    'Curve with hysteresis'))
    id_tab.append(rct_id(0xA3E48B21, 584, 'battery.cells_stat[2].t_min.value',                rct_id.t_float,   'battery.cells_stat[2].t_min.value'))
    id_tab.append(rct_id(0xA40906BF, 585, 'battery.stack_software_version[4]',                rct_id.t_uint32,  'Software version stack 4'))
    id_tab.append(rct_id(0xA5044DCD, 586, 'nsm.p_u[2][0]',                                    rct_id.t_float,   'Point 3 P/Pn'))
    id_tab.append(rct_id(0xA5341F4A, 587, 'energy.e_grid_feed_month_sum',                     rct_id.t_float,   'energy.e_grid_feed_month_sum'))
    id_tab.append(rct_id(0xA54C4685, 588, 'battery.stack_software_version[1]',                rct_id.t_uint32,  'Software version stack 1'))
    id_tab.append(rct_id(0xA59C8428, 589, 'energy.e_ext_total',                               rct_id.t_float,   'External total energy [Wh]'))
    id_tab.append(rct_id(0xA60082A9, 590, 'logger.minutes_egrid_feed_log_ts',                 rct_id.t_int32,   'logger.minutes_egrid_feed_log_ts'))
    id_tab.append(rct_id(0xA616B022, 591, 'battery.soc_target_low',                           rct_id.t_float,   'SOC target low'))
    id_tab.append(rct_id(0xA6271C2E, 592, 'grid_mon[0].u_over.threshold',                     rct_id.t_float,   'Max. voltage level 1 [V]'))
    id_tab.append(rct_id(0xA6871A4D, 593, 'battery.cells_stat[4].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[4].t_min.index'))
    id_tab.append(rct_id(0xA6C4FD4A, 594, 'battery.stack_cycles[0]',                          rct_id.t_uint16,  'battery.stack_cycles[0]'))
    id_tab.append(rct_id(0xA7447FC4, 595, 'temperature.bat_temp_power_reduction',             rct_id.t_float,   'Battery actuator temperature target [?C]'))
    id_tab.append(rct_id(0xA76AE9CA, 596, 'relays.bits_real',                                 rct_id.t_uint16,  'relays.bits_real'))
    id_tab.append(rct_id(0xA7C708EB, 597, 'logger.minutes_eload_log_ts',                      rct_id.t_int32,   'logger.minutes_eload_log_ts'))
    id_tab.append(rct_id(0xA7DBD28C, 598, 'battery.cells_stat[2].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[2].t_max.index'))
    id_tab.append(rct_id(0xA7F4123B, 599, 'battery_placeholder[0].stack_software_version[6]', rct_id.t_uint32,  'Software version stack 6'))
    id_tab.append(rct_id(0xA7FA5C5D, 600, 'power_mng.u_acc_mix_lp',                           rct_id.t_float,   'Battery voltage [V]'))
    id_tab.append(rct_id(0xA7FE5C0C, 601, 'battery.cells_stat[2].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[2].t_min.index'))
    id_tab.append(rct_id(0xA81176D0, 602, 'battery_placeholder[0].cells_stat[1].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[1].u_min.time'))
    id_tab.append(rct_id(0xA83F291F, 603, 'battery_placeholder[0].cells_stat[6].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[6].u_min.value'))
    id_tab.append(rct_id(0xA8FEAEB9, 604, 'battery_placeholder[0].cells_resist[5]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[5]'))
    id_tab.append(rct_id(0xA9033880, 605, 'battery.used_energy',                              rct_id.t_float,   'Total energy flow from battery [Wh]'))
    id_tab.append(rct_id(0xA95AD038, 606, 'grid_mon[0].f_under.threshold',                    rct_id.t_float,   'Min. frequency level 1 [Hz]'))
    id_tab.append(rct_id(0xA95EE214, 607, 'power_mng.model.bat_power_change',                 rct_id.t_float,   'power_mng.model.bat_power_change'))
    id_tab.append(rct_id(0xA9CF517D, 608, 'power_spring_down',                                rct_id.t_float,   'power_spring_down'))
    id_tab.append(rct_id(0xAA911BEE, 609, 'battery_placeholder[0].cells_stat[4].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[4].t_max.value'))
    id_tab.append(rct_id(0xAA9AA253, 610, 'dc_conv.dc_conv_struct[1].p_dc',                   rct_id.t_float,   'Solar generator B power [W]'))
    id_tab.append(rct_id(0xAACAC898, 611, 'battery.cells_stat[4].t_max.time',                 rct_id.t_uint32,  'battery.cells_stat[4].t_max.time'))
    id_tab.append(rct_id(0xAACE057A, 612, 'io_board.io1_s0_min_duration',                     rct_id.t_float,   'Minimum S0 signal duration on I/O 1 [s]'))
    id_tab.append(rct_id(0xABA015FC, 613, 'battery_placeholder[0].module_sn[1]',              rct_id.t_string,  'Module 1 Serial Number'))
    id_tab.append(rct_id(0xAC2E2A56, 614, 'io_board.rse_table[5]',                            rct_id.t_float,   'K4..K1: 0101'))
    id_tab.append(rct_id(0xACF7666B, 615, 'battery.efficiency',                               rct_id.t_float,   'Battery efficiency (used energy / stored energy)'))
    id_tab.append(rct_id(0xAE99F87A, 616, 'battery_placeholder[0].cells_stat[5].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[5].t_min.time'))
    id_tab.append(rct_id(0xAEF76FA1, 617, 'power_mng.minimum_discharge_voltage',              rct_id.t_float,   'Min. battery discharge voltage [V]'))
    id_tab.append(rct_id(0xAF64D0FE, 618, 'energy.e_dc_year[0]',                              rct_id.t_float,   'Solar generator A year energy [Wh]'))
    id_tab.append(rct_id(0xB0041187, 619, 'g_sync.u_sg_avg[1]',                               rct_id.t_float,   'Solar generator B voltage [V]'))
    id_tab.append(rct_id(0xB0307591, 620, 'db.power_board.status',                            rct_id.t_uint16,  'Power board status'))
    id_tab.append(rct_id(0xB082C4D7, 621, 'hw_test.bt_power[5]',                              rct_id.t_float,   'hw_test.bt_power[5]'))
    id_tab.append(rct_id(0xB0EBE75A, 622, 'battery.minimum_discharge_voltage',                rct_id.t_float,   'Min. discharge voltage [V]'))
    id_tab.append(rct_id(0xB0FA4D23, 623, 'acc_conv.i_charge_max',                            rct_id.t_float,   'Max. battery converter charge current [A]'))
    id_tab.append(rct_id(0xB130B8D6, 624, 'battery_placeholder[0].cells_stat[1].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[1].t_min.time'))
    id_tab.append(rct_id(0xB1D1BE71, 625, 'osci_struct.cmd_response_time',                    rct_id.t_float,   'osci_struct.cmd_response_time'))
    id_tab.append(rct_id(0xB1D465C7, 626, 'battery_placeholder[0].cells_stat[4].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[4].u_min.value'))
    id_tab.append(rct_id(0xB1EF67CE, 627, 'energy.e_ac_total',                                rct_id.t_float,   'Total energy [Wh]'))
    id_tab.append(rct_id(0xB20D1AD6, 628, 'logger.day_egrid_feed_log_ts',                     rct_id.t_int32,   ''))
    id_tab.append(rct_id(0xB221BCFA, 629, 'g_sync.p_ac_sc[2]',                                rct_id.t_float,   'Grid power phase 3 [W]'))
    id_tab.append(rct_id(0xB228EC94, 630, 'battery_placeholder[0].cells_stat[3].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[3].t_max.time'))
    id_tab.append(rct_id(0xB238942F, 631, 'last_successfull_flash_op',                        rct_id.t_int16,   'last_successfull_flash_op'))
    id_tab.append(rct_id(0xB298395D, 632, 'dc_conv.dc_conv_struct[0].u_sg_lp',                rct_id.t_float,   'Solar generator A voltage [V]'))
    id_tab.append(rct_id(0xB2FB9A90, 633, 'bat_mng_struct.k_trust',                           rct_id.t_float,   'How fast the actual prediction can be trusted'))
    id_tab.append(rct_id(0xB399B5B3, 634, 'battery_placeholder[0].cells_stat[4].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[4].u_min.index'))
    id_tab.append(rct_id(0xB403A7E6, 635, 'battery_placeholder[0].soc_update_since',          rct_id.t_float,   'battery_placeholder[0].soc_update_since'))
    id_tab.append(rct_id(0xB408E40A, 636, 'acc_conv.i_acc_lp_slow',                           rct_id.t_float,   'acc_conv.i_acc_lp_slow'))
    id_tab.append(rct_id(0xB4222BDE, 637, 'wifi.state',                                       rct_id.t_uint8,   'wifi.state'))
    id_tab.append(rct_id(0xB45FE275, 638, 'p_rec_available[0]',                               rct_id.t_float,   'Available compensation power [W]'))
    id_tab.append(rct_id(0xB4E053D4, 639, 'battery.cells_stat[1].u_min.value',                rct_id.t_float,   'battery.cells_stat[1].u_min.value'))
    id_tab.append(rct_id(0xB5317B78, 640, 'dc_conv.dc_conv_struct[0].p_dc',                   rct_id.t_float,   'Solar generator A power [W]'))
    id_tab.append(rct_id(0xB55BA2CE, 641, 'g_sync.u_sg_avg[0]',                               rct_id.t_float,   'Solar generator A voltage [V]'))
    id_tab.append(rct_id(0xB57B59BD, 642, 'battery.ah_capacity',                              rct_id.t_float,   'Battery capacity [Ah]'))
    id_tab.append(rct_id(0xB5EDA8EC, 643, 'battery_placeholder[0].cells_stat[3].u_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[3].u_max.value'))
    id_tab.append(rct_id(0xB6623608, 644, 'power_mng.bat_next_calib_date',                    rct_id.t_uint32,  'Next battery calibration'))
    id_tab.append(rct_id(0xB69171C4, 645, 'db.power_board.Current_AC_RMS',                    rct_id.t_float,   'db.power_board.Current_AC_RMS'))
    id_tab.append(rct_id(0xB70D1703, 646, 'battery_placeholder[0].cells_stat[5].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[5].u_max.index'))
    id_tab.append(rct_id(0xB76E2B4C, 647, 'nsm.cos_phi_const',                                rct_id.t_float,   'Cos phi constant value (positive = overexcited)'))
    id_tab.append(rct_id(0xB7B2967F, 648, 'energy.e_dc_total_sum[0]',                         rct_id.t_float,   'energy.e_dc_total_sum[0]'))
    id_tab.append(rct_id(0xB7C85C51, 649, 'wifi.use_ethernet',                                rct_id.t_bool,    'wifi.use_ethernet'))
    id_tab.append(rct_id(0xB7FEA209, 650, 'wifi.connect_service_timestamp',                   rct_id.t_int32,   'Service auto disconnect time'))
    id_tab.append(rct_id(0xB81FB399, 651, 'battery.cells_stat[2].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[2].u_min.time'))
    id_tab.append(rct_id(0xB836B50C, 652, 'dc_conv.dc_conv_struct[1].rescan_correction',      rct_id.t_float,   'Last global rescan MPP correction on input B [V]'))
    id_tab.append(rct_id(0xB84A38AB, 653, 'battery.soc_target_high',                          rct_id.t_float,   'SOC target high'))
    id_tab.append(rct_id(0xB84FDCF9, 654, 'adc.u_acc',                                        rct_id.t_float,   'Battery voltage (inverter) [V]'))
    id_tab.append(rct_id(0xB851FA70, 655, 'io_board.rse_table[11]',                           rct_id.t_float,   'K4..K1: 1011'))
    id_tab.append(rct_id(0xB98C8194, 656, 'nsm.min_cos_phi',                                  rct_id.t_float,   'Minimum allowed cos(phi) [0..1]'))
    id_tab.append(rct_id(0xB9928C51, 657, 'g_sync.p_ac_lp[2]',                                rct_id.t_float,   'AC power phase 3 [W]'))
    id_tab.append(rct_id(0xB9A026F9, 658, 'energy.e_ext_day',                                 rct_id.t_float,   'External day energy [Wh]'))
    id_tab.append(rct_id(0xB9E09F78, 659, 'battery.cells_stat[5].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[5].u_min.index'))
    id_tab.append(rct_id(0xBA046C03, 660, 'battery_placeholder[0].cells_stat[5].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[5].t_max.value'))
    id_tab.append(rct_id(0xBA8B8515, 661, 'dc_conv.dc_conv_struct[0].mpp.mpp_step',           rct_id.t_float,   'MPP search step on input A [V]'))
    id_tab.append(rct_id(0xBB302278, 662, 'battery.cells_stat[1].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[1].t_min.time'))
    id_tab.append(rct_id(0xBB617E51, 663, 'nsm.u_q_u[1]',                                     rct_id.t_float,   'Low voltage max. point [V]'))
    id_tab.append(rct_id(0xBBE6B9DF, 664, 'io_board.p_rse_rise_grad',                         rct_id.t_float,   'Power rise gradient [P/Pn/s]'))
    id_tab.append(rct_id(0xBCA77559, 665, 'g_sync.q_ac[2]',                                   rct_id.t_float,   'Reactive power phase 3 [var]'))
    id_tab.append(rct_id(0xBCC6F92F, 666, 'io_board.home_relay_threshold',                    rct_id.t_float,   'Switching on threshold [W]'))
    id_tab.append(rct_id(0xBD008E29, 667, 'power_mng.battery_power_extern',                   rct_id.t_float,   'Battery target power [W] (positive = discharge)'))
    id_tab.append(rct_id(0xBD3A23C3, 668, 'power_mng.soc_charge',                             rct_id.t_float,   'SOC min maintenance charge'))
    id_tab.append(rct_id(0xBD4147B0, 669, 'can_bus.set_cell_resist',                          rct_id.t_uint32,  'can_bus.set_cell_resist'))
    id_tab.append(rct_id(0xBD55905F, 670, 'energy.e_ac_day',                                  rct_id.t_float,   'Day energy [Wh]'))
    id_tab.append(rct_id(0xBD55D796, 671, 'energy.e_dc_year[1]',                              rct_id.t_float,   'Solar generator B year energy [Wh]'))
    id_tab.append(rct_id(0xBD95C46C, 672, 'battery_placeholder[0].ah_capacity',               rct_id.t_float,   'Battery capacity [Ah]'))
    id_tab.append(rct_id(0xBDE3BF0A, 673, 'battery.cells_stat[6].t_max.index',                rct_id.t_uint8,   'battery.cells_stat[6].t_max.index'))
    id_tab.append(rct_id(0xBDFE5547, 674, 'io_board.rse_table[3]',                            rct_id.t_float,   'K4..K1: 0011'))
    id_tab.append(rct_id(0xBF9B6042, 675, 'svnversion_factory',                               rct_id.t_string,  'Control software factory version'))
    id_tab.append(rct_id(0xBFFF3CAD, 676, 'net.n_slaves',                                     rct_id.t_uint8,   'net.n_slaves'))
    id_tab.append(rct_id(0xC03462F6, 677, 'g_sync.p_ac[2]',                                   rct_id.t_float,   'AC3'))
    id_tab.append(rct_id(0xC04A5F3A, 678, 'battery_placeholder[0].bms_software_version',      rct_id.t_uint32,  'Software version BMS Master'))
    id_tab.append(rct_id(0xC0680302, 679, 'battery.cells_stat[2].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[2].t_min.time'))
    id_tab.append(rct_id(0xC07E02CE, 680, 'nsm.q_u_sel',                                      rct_id.t_enum,    'Voltage selection'))
    id_tab.append(rct_id(0xC0A7074F, 681, 'net.slave_data',                                   rct_id.t_string,  ''))
    id_tab.append(rct_id(0xC0B7C4D2, 682, 'db.power_board.afi_t30',                           rct_id.t_float,   'AFI 30 mA switching off time [s]'))
    id_tab.append(rct_id(0xC0CC81B6, 683, 'energy.e_ac_year',                                 rct_id.t_float,   'Year energy [Wh]'))
    id_tab.append(rct_id(0xC0DF2978, 684, 'battery.cycles',                                   rct_id.t_int32,   'Battery charge / discharge cycles'))
    id_tab.append(rct_id(0xC198B25B, 685, 'g_sync.u_zk_p_avg',                                rct_id.t_float,   'Positive buffer capacitor voltage [V]'))
    id_tab.append(rct_id(0xC1C82889, 686, 'hw_test.bt_power[1]',                              rct_id.t_float,   'hw_test.bt_power[1]'))
    id_tab.append(rct_id(0xC1D051EC, 687, 'display_struct.variate_contrast',                  rct_id.t_uint8,   'display_struct.variate_contrast'))
    id_tab.append(rct_id(0xC24E85D0, 688, 'db.core_temp',                                     rct_id.t_float,   'Core temperature [?C]'))
    id_tab.append(rct_id(0xC3352B17, 689, 'nsm.rpm',                                          rct_id.t_enum,    'nsm.rpm'))
    id_tab.append(rct_id(0xC36675D4, 690, 'i_ac_max_set',                                     rct_id.t_float,   'Maximum AC throttle current [A]'))
    id_tab.append(rct_id(0xC3A3F070, 691, 'i_ac_extern_connected',                            rct_id.t_bool,    'Current sensors detected'))
    id_tab.append(rct_id(0xC3C7325E, 692, 'hw_test.bt_time[4]',                               rct_id.t_float,   'hw_test.bt_time[4]'))
    id_tab.append(rct_id(0xC3DD7850, 693, 'partition[6].last_id',                             rct_id.t_int32,   'partition[6].last_id'))
    id_tab.append(rct_id(0xC40D5688, 694, 'prim_sm.state_source',                             rct_id.t_uint32,  'prim_sm.state_source'))
    id_tab.append(rct_id(0xC42F5807, 695, 'battery.cells_stat[1].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[1].u_max.index'))
    id_tab.append(rct_id(0xC46E9CA4, 696, 'nsm.u_lock_out',                                   rct_id.t_float,   'Cos phi(P) lock out voltage [V]'))
    id_tab.append(rct_id(0xC4D87E96, 697, 'prim_sm.island_retrials',                          rct_id.t_uint16,  'Island trials counter'))
    id_tab.append(rct_id(0xC4FA4E33, 698, 'frt.u_min[1]',                                     rct_id.t_float,   'Point 2 voltage [V]'))
    id_tab.append(rct_id(0xC55EF32E, 699, 'logger.year_egrid_load_log_ts',                    rct_id.t_int32,   'logger.year_egrid_load_log_ts'))
    id_tab.append(rct_id(0xC56A1346, 700, 'battery_placeholder[0].cells_stat[4].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[4].t_max.index'))
    id_tab.append(rct_id(0xC642B9D6, 701, 'acc_conv.i_discharge_max',                         rct_id.t_float,   'Max. battery converter discharge current [A]'))
    id_tab.append(rct_id(0xC66665E8, 702, 'battery_placeholder[0].temperature',               rct_id.t_float,   'Battery temperature [?C]'))
    id_tab.append(rct_id(0xC66A522B, 703, 'hw_test.bt_time[1]',                               rct_id.t_float,   'hw_test.bt_time[1]'))
    id_tab.append(rct_id(0xC6DA81A0, 704, 'battery.cells_stat[6].u_max.time',                 rct_id.t_uint32,  'battery.cells_stat[6].u_max.time'))
    id_tab.append(rct_id(0xC707102E, 705, 'hw_test.bt_power[3]',                              rct_id.t_float,   'hw_test.bt_power[3]'))
    id_tab.append(rct_id(0xC71155B5, 706, 'battery_placeholder[0].cells_stat[2].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[2].t_min.index'))
    id_tab.append(rct_id(0xC717D1FB, 707, 'iso_struct.Riso',                                  rct_id.t_float,   'Total insulation resistance [Ohm]'))
    id_tab.append(rct_id(0xC7459513, 708, 'power_mng.force_inv_class',                        rct_id.t_enum,    'Change inverter class'))
    id_tab.append(rct_id(0xC7605E16, 709, 'io_board.s0_sum',                                  rct_id.t_float,   'io_board.s0_sum'))
    id_tab.append(rct_id(0xC7D3B479, 710, 'energy.e_load_year',                               rct_id.t_float,   'Household year energy [Wh]'))
    id_tab.append(rct_id(0xC7E85F32, 711, 'battery_placeholder[0].cells_stat[4].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[4].t_max.time'))
    id_tab.append(rct_id(0xC8609C8E, 712, 'battery.cells[3]',                                 rct_id.t_string,  'battery.cells[3]'))
    id_tab.append(rct_id(0xC88EB032, 713, 'battery.cells_stat[0].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[0].u_min.time'))
    id_tab.append(rct_id(0xC8BA1729, 714, 'battery.stack_software_version[2]',                rct_id.t_uint32,  'Software version stack 2'))
    id_tab.append(rct_id(0xC8E56803, 715, 'battery_placeholder[0].maximum_charge_voltage',    rct_id.t_float,   'Max. charge voltage [V]'))
    id_tab.append(rct_id(0xC937D38D, 716, 'battery_placeholder[0].stack_cycles[0]',           rct_id.t_uint16,  'battery_placeholder[0].stack_cycles[0]'))
    id_tab.append(rct_id(0xC9900716, 717, 'power_mng.is_island_only',                         rct_id.t_bool,    'Island without power switch support'))
    id_tab.append(rct_id(0xC9D76279, 718, 'energy.e_dc_day_sum[0]',                           rct_id.t_float,   'energy.e_dc_day_sum[0]'))
    id_tab.append(rct_id(0xCA4E0C03, 719, 'battery_placeholder[0].cells_stat[5].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[5].u_max.time'))
    id_tab.append(rct_id(0xCA6D6472, 720, 'logger.day_eload_log_ts',                          rct_id.t_int32,   'logger.day_eload_log_ts'))
    id_tab.append(rct_id(0xCABC44CA, 721, 'g_sync.s_ac[0]',                                   rct_id.t_float,   'Apparent power phase 1 [VA]'))
    id_tab.append(rct_id(0xCB1B3B10, 722, 'io_board.io2_s0_min_duration',                     rct_id.t_float,   'Minimum S0 signal duration on I/O 2 [s]'))
    id_tab.append(rct_id(0xCB78F611, 723, 'frt.t_max[1]',                                     rct_id.t_float,   'Point 2 time [s]'))
    id_tab.append(rct_id(0xCB85C397, 724, 'battery_placeholder[0].cells_stat[3].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[3].u_min.value'))
    id_tab.append(rct_id(0xCB9E1E6C, 725, 'nsm.Q_const',                                      rct_id.t_float,   'Constant reactive power [var] (positive = overexcited)'))
    id_tab.append(rct_id(0xCBBEEB21, 726, 'battery_placeholder[0].cells_stat[2].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[2].u_max.time'))
    id_tab.append(rct_id(0xCBDAD315, 727, 'logger.minutes_ebat_log_ts',                       rct_id.t_int32,   'logger.minutes_ebat_log_ts'))
    id_tab.append(rct_id(0xCBEC8200, 728, 'hw_test.timer2',                                   rct_id.t_float,   'hw_test.timer2'))
    id_tab.append(rct_id(0xCCB51399, 729, 'nsm.q_u_max_u_low',                                rct_id.t_float,   'Qmax at lower voltage level [var] (positive = overexcited)'))
    id_tab.append(rct_id(0xCD8EDAD3, 730, 'battery_placeholder[0].cells_stat[3].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[3].t_min.value'))
    id_tab.append(rct_id(0xCE266F0F, 731, 'power_mng.soc_min',                                rct_id.t_float,   'Min SOC target'))
    id_tab.append(rct_id(0xCE49EB86, 732, 'battery_placeholder[0].cells_stat[2].t_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[2].t_max.index'))
    id_tab.append(rct_id(0xCF005C54, 733, 'prim_sm.phase_3_mode',                             rct_id.t_bool,    'prim_sm.phase_3_mode'))
    id_tab.append(rct_id(0xCF053085, 734, 'g_sync.u_l_rms[0]',                                rct_id.t_float,   ''))
    id_tab.append(rct_id(0xCF096A6B, 735, 'battery_placeholder[0].stack_software_version[4]', rct_id.t_uint32,  'Software version stack 4'))
    id_tab.append(rct_id(0xD0C47326, 736, 'battery.cells_stat[1].t_min.value',                rct_id.t_float,   'battery.cells_stat[1].t_min.value'))
    id_tab.append(rct_id(0xD143A391, 737, 'can_bus.set_cell_v_t',                             rct_id.t_uint32,  'can_bus.set_cell_v_t'))
    id_tab.append(rct_id(0xD166D94D, 738, 'flash_rtc.time_stamp',                             rct_id.t_uint32,  'Actual date/time'))
    id_tab.append(rct_id(0xD197CBE0, 739, 'power_mng.stop_charge_current',                    rct_id.t_float,   'Stop charge current [A]'))
    id_tab.append(rct_id(0xD1DFC969, 740, 'power_mng.soc_target_set',                         rct_id.t_float,   'Force SOC target'))
    id_tab.append(rct_id(0xD1F9D017, 741, 'battery_placeholder[0].cells_stat[4].u_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[4].u_min.time'))
    id_tab.append(rct_id(0xD2DEA4B1, 742, 'battery_placeholder[0].cells_stat[5].t_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[5].t_min.index'))
    id_tab.append(rct_id(0xD3085D80, 743, 'net.soc_av',                                       rct_id.t_float,   'net.soc_av'))
    id_tab.append(rct_id(0xD3E94E6B, 744, 'logger.minutes_temp_bat_log_ts',                   rct_id.t_int32,   'logger.minutes_temp_bat_log_ts'))
    id_tab.append(rct_id(0xD3F492EB, 745, 'battery_placeholder[0].cells_stat[0].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[0].t_max.time'))
    id_tab.append(rct_id(0xD451EF88, 746, 'cs_map[2]',                                        rct_id.t_uint8,   'Associate current sensor 2 with phase L'))
    id_tab.append(rct_id(0xD45913EC, 747, 'io_board.rse_table[13]',                           rct_id.t_float,   'K4..K1: 1101'))
    id_tab.append(rct_id(0xD4C4A941, 748, 'hw_test.bt_time[7]',                               rct_id.t_float,   'hw_test.bt_time[7]'))
    id_tab.append(rct_id(0xD5205A45, 749, 'net.slave_timeout',                                rct_id.t_float,   'net.slave_timeout'))
    id_tab.append(rct_id(0xD536E7E9, 750, 'frt.u_max[1]',                                     rct_id.t_float,   'Point 2 voltage [V]'))
    id_tab.append(rct_id(0xD5567470, 751, 'partition[4].last_id',                             rct_id.t_int32,   'partition[4].last_id'))
    id_tab.append(rct_id(0xD5790CE1, 752, 'wifi.use_wifi',                                    rct_id.t_bool,    'Enable Wi-Fi Access Point'))
    id_tab.append(rct_id(0xD580567B, 753, 'nsm.u_lock_in',                                    rct_id.t_float,   'Cos phi(P) lock in voltage [V]'))
    id_tab.append(rct_id(0xD60E7A2F, 754, 'battery.cells_stat[1].u_min.time',                 rct_id.t_uint32,  'battery.cells_stat[1].u_min.time'))
    id_tab.append(rct_id(0xD81471DF, 755, 'battery_placeholder[0].cells_stat[6].t_max.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[6].t_max.value'))
    id_tab.append(rct_id(0xD82F2D0B, 756, 'battery_placeholder[0].cells_stat[3].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[3].u_min.index'))
    id_tab.append(rct_id(0xD83DC6AC, 757, 'wifi.server_port',                                 rct_id.t_int32,   'wifi.server_port'))
    id_tab.append(rct_id(0xD876A4AC, 758, 'battery_placeholder[0].cells_stat[0].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[0].u_min.index'))
    id_tab.append(rct_id(0xD884AF95, 759, 'nsm.pf_desc_grad',                                 rct_id.t_float,   'Power decrease gradient for P(f) mode [P/(Pn*s)]'))
    id_tab.append(rct_id(0xD9D66B76, 760, 'energy.e_grid_load_year_sum',                      rct_id.t_float,   'energy.e_grid_load_year_sum'))
    id_tab.append(rct_id(0xD9E721A5, 761, 'grid_lt.timeframe',                                rct_id.t_float,   'Timeframe'))
    id_tab.append(rct_id(0xD9F9F35B, 762, 'acc_conv.state_slow',                              rct_id.t_uint8,   'acc_conv.state_slow'))
    id_tab.append(rct_id(0xDA207111, 763, 'energy.e_grid_load_month_sum',                     rct_id.t_float,   'energy.e_grid_load_month_sum'))
    id_tab.append(rct_id(0xDABD323E, 764, 'osci_struct.error',                                rct_id.t_int16,   'Communication error'))
    id_tab.append(rct_id(0xDAC7DD86, 765, 'io_board.p_rse_desc_grad',                         rct_id.t_float,   'Power descent gradient [P/Pn/s]'))
    id_tab.append(rct_id(0xDB11855B, 766, 'dc_conv.dc_conv_struct[0].p_dc_lp',                rct_id.t_float,   'Solar generator A power [W]'))
    id_tab.append(rct_id(0xDB2D69AE, 767, 'g_sync.p_ac_sum_lp',                               rct_id.t_float,   'AC power [W]'))
    id_tab.append(rct_id(0xDB45ABD0, 768, 'dc_conv.dc_conv_struct[0].rescan_correction',      rct_id.t_float,   'Last global rescan MPP correction on input A [V]'))
    id_tab.append(rct_id(0xDB62DCB7, 769, 'net.n_devices',                                    rct_id.t_uint8,   'net.n_devices'))
    id_tab.append(rct_id(0xDC667958, 770, 'power_mng.state',                                  rct_id.t_uint8,   'Battery state machine'))
    id_tab.append(rct_id(0xDCA1CF26, 771, 'g_sync.s_ac_sum_lp',                               rct_id.t_float,   'Apparent power [VA]'))
    id_tab.append(rct_id(0xDCAC0EA9, 772, 'g_sync.i_dr_lp[1]',                                rct_id.t_float,   'Current phase 2 (average) [A]'))
    id_tab.append(rct_id(0xDD5930A2, 773, 'battery.cells_stat[0].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[0].t_min.index'))
    id_tab.append(rct_id(0xDD90A328, 774, 'flash_rtc.time_stamp_update',                      rct_id.t_uint32,  'Last update date'))
    id_tab.append(rct_id(0xDDD1C2D0, 775, 'svnversion',                                       rct_id.t_string,  'Control software version'))
    id_tab.append(rct_id(0xDE17F021, 776, 'energy.e_grid_load_year',                          rct_id.t_float,   'Year energy grid load [Wh]'))
    id_tab.append(rct_id(0xDE68F62D, 777, 'bat_mng_struct.profile_pext',                      rct_id.t_string,  'bat_mng_struct.profile_pext'))
    id_tab.append(rct_id(0xDE9CBCB0, 778, 'battery.cells_stat[5].t_max.value',                rct_id.t_float,   'battery.cells_stat[5].t_max.value'))
    id_tab.append(rct_id(0xDEE1957F, 779, 'battery.cells_resist[4]',                          rct_id.t_string,  'battery.cells_resist[4]'))
    id_tab.append(rct_id(0xDF0A735C, 780, 'battery.maximum_discharge_current',                rct_id.t_float,   'Max. discharge current [A]'))
    id_tab.append(rct_id(0xDF6EA121, 781, 'bat_mng_struct.profile_pdc',                       rct_id.t_string,  'bat_mng_struct.profile_pdc'))
    id_tab.append(rct_id(0xDFB53AF3, 782, 'db.power_board.Current_Mean_Mean_AC',              rct_id.t_float,   'db.power_board.Current_Mean_Mean_AC'))
    id_tab.append(rct_id(0xDFF966E3, 783, 'battery.cells_stat[6].t_min.index',                rct_id.t_uint8,   'battery.cells_stat[6].t_min.index'))
    id_tab.append(rct_id(0xE04C3900, 784, 'logger.day_eac_log_ts',                            rct_id.t_int32,   'logger.day_eac_log_ts'))
    id_tab.append(rct_id(0xE0E16E63, 785, 'cs_map[0]',                                        rct_id.t_uint8,   'Associate current sensor 0 with phase L'))
    id_tab.append(rct_id(0xE14B8679, 786, 'i_dc_slow_max',                                    rct_id.t_float,   'Max. slow DC-component of Iac [A]'))
    id_tab.append(rct_id(0xE14F1CBA, 787, 'battery_placeholder[0].cells_stat[4]',             rct_id.t_string,  ''))
    id_tab.append(rct_id(0xE19C8B79, 788, 'battery_placeholder[0].cells_resist[1]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[1]'))
    id_tab.append(rct_id(0xE1F49459, 789, 'frt.t_min[2]',                                     rct_id.t_float,   'Point 3 time [s]'))
    id_tab.append(rct_id(0xE24B00BD, 790, 'power_mng.schedule[1]',                            rct_id.t_string,  'power_mng.schedule[1]'))
    id_tab.append(rct_id(0xE271C6D2, 791, 'nsm.u_q_u[2]',                                     rct_id.t_float,   'High voltage min. point [V]'))
    id_tab.append(rct_id(0xE29C24EB, 792, 'logger.minutes_eac3_log_ts',                       rct_id.t_int32,   'logger.minutes_eac3_log_ts'))
    id_tab.append(rct_id(0xE31F8B17, 793, 'prim_sm.Uzk_pump_grad[0]',                         rct_id.t_float,   'start power [W]'))
    id_tab.append(rct_id(0xE3F4D1DF, 794, 'acc_conv.i_max',                                   rct_id.t_float,   'Max. battery converter current [A]'))
    id_tab.append(rct_id(0xE49BE3ED, 795, 'nsm.pf_rise_grad',                                 rct_id.t_float,   'Power increase gradient after P(f) restriction [P/(Pn*s)]'))
    id_tab.append(rct_id(0xE4DC040A, 796, 'logger.month_eext_log_ts',                         rct_id.t_int32,   'logger.month_eext_log_ts'))
    id_tab.append(rct_id(0xE52B89FA, 798, 'io_board.home_relay_off_threshold',                rct_id.t_float,   'Switching off threshold [W]'))
    id_tab.append(rct_id(0xE5FBCC6F, 799, 'logger.year_eload_log_ts',                         rct_id.t_int32,   'logger.year_eload_log_ts'))
    id_tab.append(rct_id(0xE6248312, 800, 'hw_test.bt_power[8]',                              rct_id.t_float,   'hw_test.bt_power[8]'))
    id_tab.append(rct_id(0xE635A6C4, 801, 'battery_placeholder[0].module_sn[2]',              rct_id.t_string,  'Module 2 Serial Number'))
    id_tab.append(rct_id(0xE63A3529, 802, 'flash_result',                                     rct_id.t_uint16,  'Flash result'))
    id_tab.append(rct_id(0xE6F1CB83, 803, 'nsm.pu_ts',                                        rct_id.t_float,   'Time const for filter          [s]'))
    id_tab.append(rct_id(0xE7177DEE, 804, 'battery.cells_stat[2].u_max.value',                rct_id.t_float,   'battery.cells_stat[2].u_max.value'))
    id_tab.append(rct_id(0xE7B0E692, 805, 'battery.bat_impedance.impedance_fine',             rct_id.t_float,   'Battery circuit impedance'))
    id_tab.append(rct_id(0xE87B1F4B, 806, 'battery_placeholder[0].cells_stat[0].u_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[0].u_min.value'))
    id_tab.append(rct_id(0xE94C2EFC, 807, 'g_sync.q_ac[0]',                                   rct_id.t_float,   'Reactive power phase 1 [var]'))
    id_tab.append(rct_id(0xE952FF2D, 808, 'nsm.q_u_max_u_low_rel',                            rct_id.t_float,   'Qmax at lower voltage level relative to Smax (positive = overexcited)'))
    id_tab.append(rct_id(0xE96F1844, 809, 'io_board.s0_external_power',                       rct_id.t_float,   'io_board.s0_external_power'))
    id_tab.append(rct_id(0xE9BBF6E4, 810, 'power_mng.amp_hours_measured',                     rct_id.t_float,   'Measured battery capacity [Ah]'))
    id_tab.append(rct_id(0xEA399EA8, 811, 'battery_placeholder[0].min_cell_voltage',          rct_id.t_float,   'battery_placeholder[0].min_cell_voltage'))
    id_tab.append(rct_id(0xEA77252E, 812, 'battery.minimum_discharge_voltage_constant_u',     rct_id.t_float,   'Min. discharge voltage [V]'))
    id_tab.append(rct_id(0xEAEEB3CA, 813, 'energy.e_dc_month_sum[0]',                         rct_id.t_float,   'energy.e_dc_month_sum[0]'))
    id_tab.append(rct_id(0xEB4C2597, 814, 'battery.cells_resist[6]',                          rct_id.t_string,  'battery.cells_resist[6]'))
    id_tab.append(rct_id(0xEB7773BF, 815, 'nsm.p_u[1][1]',                                    rct_id.t_float,   'Point 2 voltage [V]'))
    id_tab.append(rct_id(0xEB7BCB93, 816, 'battery_placeholder[0].bms_sn',                    rct_id.t_string,  'BMS Serial Number'))
    id_tab.append(rct_id(0xEBC62737, 817, 'android_description',                              rct_id.t_string,  'Device name'))
    id_tab.append(rct_id(0xEBF7A4E8, 818, 'grid_mon[0].f_over.threshold',                     rct_id.t_float,   'Max. frequency level 1 [Hz]'))
    id_tab.append(rct_id(0xECABB6CF, 819, 'switch_on_cond.test_time',                         rct_id.t_float,   'Test time'))
    id_tab.append(rct_id(0xEE049B1F, 820, 'nsm.pf_hysteresis',                                rct_id.t_bool,    'Hysteresis mode'))
    id_tab.append(rct_id(0xEEA3F59B, 821, 'battery.stack_software_version[5]',                rct_id.t_uint32,  'Software version stack 5'))
    id_tab.append(rct_id(0xEEC44AA0, 822, 'battery_placeholder[0].cells_stat[2].u_min.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[2].u_min.index'))
    id_tab.append(rct_id(0xEECDFEFC, 823, 'battery.cells_stat[2].u_min.value',                rct_id.t_float,   'battery.cells_stat[2].u_min.value'))
    id_tab.append(rct_id(0xEF89568B, 824, 'grid_mon[0].u_under.time',                         rct_id.t_float,   'Min. voltage switch-off time level 1 [s]'))
    id_tab.append(rct_id(0xEFD3EC8A, 825, 'battery.cells_stat[5].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[5].t_min.time'))
    id_tab.append(rct_id(0xEFF4B537, 826, 'energy.e_load_total',                              rct_id.t_float,   'Household total energy [Wh]'))
    id_tab.append(rct_id(0xF03133E2, 827, 'partition[0].last_id',                             rct_id.t_int32,   'partition[0].last_id'))
    id_tab.append(rct_id(0xF044EDA0, 828, 'battery.cells_stat[3].t_max.value',                rct_id.t_float,   'battery.cells_stat[3].t_max.value'))
    id_tab.append(rct_id(0xF0527539, 829, 'db.power_board.adc_p3V3_meas',                     rct_id.t_float,   'db.power_board.adc_p3V3_meas'))
    id_tab.append(rct_id(0xF09CC4A2, 830, 'grid_mon[1].u_over.time',                          rct_id.t_float,   'Max. voltage switch-off time level 2 [s]'))
    id_tab.append(rct_id(0xF0A03A20, 831, 'bat_mng_struct.k',                                 rct_id.t_float,   'Forecast correction'))
    id_tab.append(rct_id(0xF0B436DD, 832, 'g_sync.p_ac_load[2]',                              rct_id.t_float,   'Load household phase 3 [W]'))
    id_tab.append(rct_id(0xF0BE6429, 833, 'energy.e_load_month',                              rct_id.t_float,   'Household month energy [Wh]'))
    id_tab.append(rct_id(0xF1342795, 834, 'power_mng.stop_discharge_current',                 rct_id.t_float,   'Stop discharge current [A]'))
    id_tab.append(rct_id(0xF168B748, 835, 'power_mng.soc_strategy',                           rct_id.t_enum,    'SOC target selection'))
    id_tab.append(rct_id(0xF1DE6E99, 836, 'battery_placeholder[0].cells_resist[3]',           rct_id.t_string,  'battery_placeholder[0].cells_resist[3]'))
    id_tab.append(rct_id(0xF1FA5BB9, 837, 'grid_mon[1].f_under.time',                         rct_id.t_float,   'Min. frequency switch-off time level 2 [s]'))
    id_tab.append(rct_id(0xF23D4595, 838, 'battery_placeholder[0].cells_stat[1].t_min.value', rct_id.t_float,   'battery_placeholder[0].cells_stat[1].t_min.value'))
    id_tab.append(rct_id(0xF2405AC6, 839, 'nsm.p_limit',                                      rct_id.t_float,   'Max. grid power [W]'))
    id_tab.append(rct_id(0xF247BB16, 840, 'display_struct.contrast',                          rct_id.t_uint8,   ''))
    id_tab.append(rct_id(0xF25591AA, 841, 'nsm.cos_phi_p[3][0]',                              rct_id.t_float,   'Point 4 [P/Pn]'))
    id_tab.append(rct_id(0xF257D342, 842, 'battery.cells_stat[1].t_max.value',                rct_id.t_float,   'battery.cells_stat[1].t_max.value'))
    id_tab.append(rct_id(0xF25C339B, 843, 'g_sync.u_ptp_rms[2]',                              rct_id.t_float,   'Phase to phase voltage 3 [V]'))
    id_tab.append(rct_id(0xF28341E2, 844, 'logger.month_eac_log_ts',                          rct_id.t_int32,   'logger.month_eac_log_ts'))
    id_tab.append(rct_id(0xF2BE0C9C, 845, 'p_buf_available',                                  rct_id.t_float,   'Available buffer power [W]'))
    id_tab.append(rct_id(0xF393B7B0, 846, 'power_mng.calib_charge_power',                     rct_id.t_float,   'Calibration charge power [W]'))
    id_tab.append(rct_id(0xF3FD6C4C, 847, 'nsm.pf_use_p_max',                                 rct_id.t_bool,    'By over-frequency in P(f) use Pmax instead of Pmom (instant P).'))
    id_tab.append(rct_id(0xF3FD8CE6, 848, 'battery.cells_resist[2]',                          rct_id.t_string,  'battery.cells_resist[2]'))
    id_tab.append(rct_id(0xF42D4DD0, 849, 'io_board.alarm_home_value',                        rct_id.t_enum,    'Evaluated value'))
    id_tab.append(rct_id(0xF451E935, 850, 'battery_placeholder[0].cells_stat[0].t_min.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[0].t_min.time'))
    id_tab.append(rct_id(0xF473BC5E, 851, 'buf_v_control.power_reduction_max_solar_grid',     rct_id.t_float,   'Max. allowed grid feed-in power [W]'))
    id_tab.append(rct_id(0xF49F58F2, 852, 'nsm.p_u[2][1]',                                    rct_id.t_float,   'Point 3 voltage [V]'))
    id_tab.append(rct_id(0xF52C0B50, 853, 'power_mng.schedule[7]',                            rct_id.t_string,  'power_mng.schedule[7]'))
    id_tab.append(rct_id(0xF54BC06D, 854, 'battery.cells_stat[4].u_max.value',                rct_id.t_float,   'battery.cells_stat[4].u_max.value'))
    id_tab.append(rct_id(0xF5584F90, 855, 'g_sync.p_ac_sc[1]',                                rct_id.t_float,   'Grid power phase 2 [W]'))
    id_tab.append(rct_id(0xF644DCA7, 856, 'bat_mng_struct.k_reserve',                         rct_id.t_float,   'Main reservation coefficient [0..2]'))
    id_tab.append(rct_id(0xF677D737, 857, 'battery_placeholder[0].cells_stat[6].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[6].u_max.time'))
    id_tab.append(rct_id(0xF68ECC1F, 858, 'battery_placeholder[0].cells_stat[1].u_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[1].u_max.time'))
    id_tab.append(rct_id(0xF6A85818, 859, 'nsm.f_entry',                                      rct_id.t_float,   'Entry frequency for P(f) over-frequency mode [Hz]'))
    id_tab.append(rct_id(0xF742C6BA, 860, 'battery_placeholder[0].cells_stat[1].u_max.index', rct_id.t_uint8,   'battery_placeholder[0].cells_stat[1].u_max.index'))
    id_tab.append(rct_id(0xF76DE445, 861, 'logger.minutes_temp_log_ts',                       rct_id.t_int32,   'logger.minutes_temp_log_ts'))
    id_tab.append(rct_id(0xF79D41D9, 862, 'db.temp1',                                         rct_id.t_float,   'Heat sink temperature [?C]'))
    id_tab.append(rct_id(0xF87A2A1E, 863, 'dc_conv.last_rescan',                              rct_id.t_uint32,  'Last global rescan'))
    id_tab.append(rct_id(0xF8C0D255, 864, 'battery.cells[0]',                                 rct_id.t_string,  'battery.cells[0]'))
    id_tab.append(rct_id(0xF8DECCE6, 865, 'wifi.connected_ap_ssid',                           rct_id.t_string,  'WiFi associated AP'))
    id_tab.append(rct_id(0xF99E8CC8, 866, 'battery.cells_stat[6]',                            rct_id.t_string,  'battery.cells_stat[6]'))
    id_tab.append(rct_id(0xF9FD0D61, 867, 'wifi.service_ip',                                  rct_id.t_string,  'wifi.service_ip'))
    id_tab.append(rct_id(0xFA3276DC, 868, 'battery.cells_stat[3].t_min.time',                 rct_id.t_uint32,  'battery.cells_stat[3].t_min.time'))
    id_tab.append(rct_id(0xFA7DB323, 869, 'io_board.check_s0_result',                         rct_id.t_uint16,  'io_board.check_s0_result'))
    id_tab.append(rct_id(0xFAA837C8, 870, 'nsm.f_low_rise_grad',                              rct_id.t_float,   'Power rise gradient for P(f) under-frequency mode without battery [1/Pn*Hz]'))
    id_tab.append(rct_id(0xFAE429C5, 871, 'rb485.f_grid[1]',                                  rct_id.t_float,   'Grid phase 2 frequency [Hz]'))
    id_tab.append(rct_id(0xFB57BA65, 872, 'bat_mng_struct.count',                             rct_id.t_string,  'bat_mng_struct.count'))
    id_tab.append(rct_id(0xFB5DE9C5, 873, 'prim_sm.minigrid_flag',                            rct_id.t_bool,    'Minigrid support'))
    id_tab.append(rct_id(0xFB796780, 874, 'battery.cells_stat[1]',                            rct_id.t_string,  'battery.cells_stat[1]'))
    id_tab.append(rct_id(0xFBD94C1F, 875, 'power_mng.amp_hours',                              rct_id.t_float,   'Battery energy [Ah]'))
    id_tab.append(rct_id(0xFBF3CE97, 876, 'energy.e_dc_day[1]',                               rct_id.t_float,   'Solar generator B day energy [Wh]'))
    id_tab.append(rct_id(0xFBF6D834, 877, 'battery.module_sn[0]',                             rct_id.t_string,  'Module 0 Serial Number'))
    id_tab.append(rct_id(0xFBF8D63C, 878, 'energy.e_grid_load_day_sum',                       rct_id.t_float,   'energy.e_grid_load_day_sum'))
    id_tab.append(rct_id(0xFC1C614E, 879, 'energy.e_ac_month_sum',                            rct_id.t_float,   'energy.e_ac_month_sum'))
    id_tab.append(rct_id(0xFC1F8C65, 880, 'battery_placeholder[0].cells_stat[6].t_max.time',  rct_id.t_uint32,  'battery_placeholder[0].cells_stat[6].t_max.time'))
    id_tab.append(rct_id(0xFC5AA529, 881, 'bat_mng_struct.bat_calib_soc_threshold',           rct_id.t_float,   'SOC threshold for battery calibration in advance'))
    id_tab.append(rct_id(0xFC724A9E, 882, 'energy.e_dc_total[0]',                             rct_id.t_float,   'Solar generator A total energy [Wh]'))
    id_tab.append(rct_id(0xFCA1CBB5, 883, 'battery_placeholder[0].voltage',                   rct_id.t_float,   'Battery voltage [V]'))
    id_tab.append(rct_id(0xFCC39293, 884, 'nsm.rpm_lock_in_power',                            rct_id.t_float,   'Reactive Power Mode lock-in power [P/Pn]'))
    id_tab.append(rct_id(0xFCF4E78D, 885, 'logger.day_ea_log_ts',                             rct_id.t_int32,   'logger.day_ea_log_ts'))
    id_tab.append(rct_id(0xFD4F17C4, 886, 'grid_mon[1].f_over.time',                          rct_id.t_float,   'Max. frequency switch-off time level 2 [s]'))
    id_tab.append(rct_id(0xFD72CC0D, 887, 'frt.enabled',                                      rct_id.t_bool,    'Enable FRT'))
    id_tab.append(rct_id(0xFDB81124, 888, 'energy.e_grid_feed_day_sum',                       rct_id.t_float,   'energy.e_grid_feed_day_sum'))
    id_tab.append(rct_id(0xFDBD9EE9, 889, 'battery.cells_stat[3].u_max.index',                rct_id.t_uint8,   'battery.cells_stat[3].u_max.index'))
    id_tab.append(rct_id(0xFE1AA500, 890, 'buf_v_control.power_reduction',                    rct_id.t_float,   'External power reduction based on solar plant peak power [0..1]'))
    id_tab.append(rct_id(0xFE38B227, 891, 'battery_placeholder[0].cells_stat[5]',             rct_id.t_string,  'battery_placeholder[0].cells_stat[5]'))
    id_tab.append(rct_id(0xFE44BA26, 892, 'battery.cells_stat[0].u_min.index',                rct_id.t_uint8,   'battery.cells_stat[0].u_min.index'))
    id_tab.append(rct_id(0xFED51BD2, 893, 'dc_conv.dc_conv_struct[1].enabled',                rct_id.t_bool,    'Solar generator B connected'))
    id_tab.append(rct_id(0xFF2A258B, 894, 'wifi.server_ip',                                   rct_id.t_string,  'wifi.server_ip'))
    id_tab.append(rct_id(0xFF5B8A54, 895, 'battery_placeholder[0].cells_stat[3]',             rct_id.t_string,  'battery_placeholder[0].cells_stat[3]'))
