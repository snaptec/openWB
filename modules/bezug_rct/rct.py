#!/usr/bin/python

#
# Functions, definitions and classes to access RCT POWER
# Implementation based on RCT Power Serial Communication Protocol (doc version 1.8)
#

import sys
import getopt
import socket
import select
import struct
import binascii

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

    # group id
    g_rb485 = 0
    g_energy = 1
    g_grid_mon = 2
    g_temperature = 3
    g_battery = 4
    g_cs_neg = 5
    g_hw_test = 6
    g_g_sync = 7
    g_logger = 8
    g_wifi = 9
    g_adc = 10
    g_net = 11
    g_acc_conv = 12
    g_dc_conv = 13
    g_nsm = 14
    g_io_board = 15
    g_flash_rtc = 16
    g_power_mng = 17
    g_buf_v_control = 18
    g_db = 19
    g_switch_on_board = 20 
    g_p_rec = 21
    g_modbus = 22
    g_bat_mng_struct = 23
    g_iso_struct = 24
    g_grid_lt = 25
    g_can_bus = 26
    g_display_struct = 27
    g_flash_param = 28
    g_fault = 29
    g_prim_sm = 30
    g_cs_map = 31
    g_line_mon = 32
    g_others = 33
    
    def __init__(self, group, msgid, idx, name, data_type, desc='', unit='', sim_data = None):
        self.group = group
        self.id = msgid
        self.idx = idx
        self.data_type = data_type
        self.name = name
        self.desc = desc
        self.unit = unit
        # sim_data is used by rct_sim to return an individual response
        if sim_data == None:
            if data_type == self.t_bool:
                self.sim_data = True
            elif data_type == self.t_string:
                self.sim_data = 'ABCDEFG'
            else:
                self.sim_data = 0
        else:
            self.sim_data = sim_data


# local variables
id_tab = []
bVerbose = False
host = 'localhost'
port = 8899
receive_timeout = 2.0
search_id = 0
search_name = None


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
            return str(data)
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
            buf = sock.recv(8)
            if len(buf) > 0:
                i = response.consume(buf)
                if response.FrameComplete and response.CRCOk == True:
                    if id > 0 and id != response.id:
                        errlog('response id', id, 'doesn\'t fit to the requested id')
                    else:
                        return response
        else:
            # timeout
            return None

# send a read request and wait for the response
def read(clientsocket, id, address = 0, timeout = receive_timeout):
    if clientsocket is not None:
        frame = send(clientsocket, cmd_read, id, address)
    
        response = receive(clientsocket, id, timeout)
        if response is None:
            return '[timeout]'
        else:
            return response.value
    
def close(clientsocket):
    clientsocket.close()
        
# setup the rct_id table with id and expected data type          
def init(argv):
    global bVerbose
    global host
    global port
    global search_id
    global search_name
    
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

    # add all known id's with name, data type, description and unit to the id table
    id_tab.append(rct_id(rct_id.g_rb485, 0x104EB6A, 0, 'rb485.f_grid[2]', rct_id.t_float, 'Grid phase 3 frequency', 'Hz'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x7367B64, 16, 'rb485.phase_marker', rct_id.t_int16, 'Next phase after phase 1 in Power Switch'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x173D81E4, 60, 'rb485.version_boot', rct_id.t_uint32, 'Power Switch bootloader version'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x21EE7CBB, 83, 'rb485.u_l_grid[2]', rct_id.t_float, 'Grid phase 3 voltage', 'V'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x27650FE2, 99, 'rb485.version_main', rct_id.t_uint32, 'Power Switch software version'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x3B5F6B9D, 151, 'rb485.f_wr[0]', rct_id.t_float, 'Power Storage phase 1 frequency', 'Hz'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x437B8122, 171, 'rb485.available', rct_id.t_bool))
    id_tab.append(rct_id(rct_id.g_rb485, 0x6FD36B32, 299, 'rb485.f_wr[1]', rct_id.t_float, 'Power Storage phase 2 frequency', 'Hz'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x7A9091EA, 334, 'rb485.u_l_grid[1]', rct_id.t_float, 'Grid phase 2 voltage', 'V'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x905F707B, 391, 'rb485.f_wr[2]', rct_id.t_float, 'Power Storage phase 3 frequency', 'Hz'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x93F976AB, 410, 'rb485.u_l_grid[0]', rct_id.t_float, 'Grid phase 1 voltage', 'V'))
    id_tab.append(rct_id(rct_id.g_rb485, 0x9558AD8A, 412, 'rb485.f_grid[0]', rct_id.t_float, 'Grid phase1 frequency', 'Hz'))
    id_tab.append(rct_id(rct_id.g_rb485, 0xFAE429C5, 656, 'rb485.f_grid[1]', rct_id.t_float, 'Grid phase 2 frequency', 'Hz'))

    id_tab.append(rct_id(rct_id.g_energy, 0x31A6110, 4, 'energy.e_ext_month', rct_id.t_float, 'External month energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xC588B75, 29, 'energy.e_ext_day_sum', rct_id.t_float, 'energy.e_ext_day_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0xF28E2E1, 41, 'energy.e_ext_total_sum', rct_id.t_float, 'energy.e_ext_total_sum')) 
    id_tab.append(rct_id(rct_id.g_energy, 0x10970E9D, 47, 'energy.e_ac_month', rct_id.t_float, 'Month energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x126ABC86, 50, 'energy.e_grid_load_month', rct_id.t_float, 'Month energy grid load', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x1BFA5A33, 70, 'energy.e_grid_load_total_sum', rct_id.t_float, 'energy.e_grid_load_total_sum')) 
    id_tab.append(rct_id(rct_id.g_energy, 0x21E1A802, 82, 'energy.e_dc_month_sum[1]', rct_id.t_float, 'energy.e_dc_month_sum[1]'))
    id_tab.append(rct_id(rct_id.g_energy, 0x241F1F98, 90, 'energy.e_dc_day_sum[1]', rct_id.t_float, 'energy.e_dc_day_sum[1]'))
    id_tab.append(rct_id(rct_id.g_energy, 0x26EFFC2F, 97, 'energy.e_grid_feed_year', rct_id.t_float, 'Year energy grid feed-in', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x27C828F4, 103, 'energy.e_grid_feed_total_sum', rct_id.t_float, 'energy.e_grid_feed_total_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x2AE703F2, 111, 'energy.e_dc_day[0]', rct_id.t_float, 'Solar generator A day energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x2F3C1D7D, 117, 'energy.e_load_day', rct_id.t_float, 'Household day energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x3A873343, 146, 'energy.e_ac_day_sum', rct_id.t_float, 'energy.e_ac_day_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x3A9D2680, 147, 'energy.e_ext_year_sum', rct_id.t_float, 'energy.e_ext_year_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x3C87C4F5, 155, 'energy.e_grid_feed_day', rct_id.t_float, 'Day energy grid feed-in', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x44D4C533, 178, 'energy.e_grid_feed_total', rct_id.t_float, 'Total energy grid feed-in', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x495BF0B6, 187, 'energy.e_dc_year_sum[0]', rct_id.t_float, 'energy.e_dc_year_sum[0]'))
    id_tab.append(rct_id(rct_id.g_energy, 0x4BE02BB7, 191, 'energy.e_load_day_sum', rct_id.t_float, 'energy.e_load_day_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x4EE8DB78, 206, 'energy.e_load_year_sum', rct_id.t_float, 'energy.e_load_year_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x62FBE7DC, 259, 'energy.e_grid_load_total', rct_id.t_float, 'Total energy grid load', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x65B624AB, 267, 'energy.e_grid_feed_month', rct_id.t_float, 'Month energy grid feed-in', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x6709A2F4, 271, 'energy.e_ac_year_sum', rct_id.t_float, 'energy.e_ac_year_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x68EEFD3D, 278, 'energy.e_dc_total[1]', rct_id.t_float, 'Solar generator B total energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x6CFCD774, 289, 'energy.e_dc_year_sum[1]', rct_id.t_float, 'energy.e_dc_year_sum[1]'))
    id_tab.append(rct_id(rct_id.g_energy, 0x6FF4BD55, 300, 'energy.e_ext_month_sum', rct_id.t_float, 'energy.e_ext_month_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x79C0A724, 331, 'energy.e_ac_total_sum', rct_id.t_float, 'energy.e_ac_total_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x7AB9B045, 335, 'energy.e_dc_month[1]', rct_id.t_float, 'Solar generator B month energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x7E096024, 342, 'energy.e_load_total_sum', rct_id.t_float, 'energy.e_load_total_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0x812E5ADD, 349, 'energy.e_dc_total_sum[1]', rct_id.t_float, 'energy.e_dc_total_sum[1]'))
    id_tab.append(rct_id(rct_id.g_energy, 0x81AE960B, 351, 'energy.e_dc_month[0]', rct_id.t_float, 'Solar generator A month energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x84ABE3D8, 358, 'energy.e_grid_feed_year_sum', rct_id.t_float, 'energy.e_grid_feed_year_sum')) 
    id_tab.append(rct_id(rct_id.g_energy, 0x867DEF7D, 361, 'energy.e_grid_load_day', rct_id.t_float, 'Day energy grid load', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0x917E3622, 398, 'energy.e_ext_year', rct_id.t_float, 'External year energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xA12BE39C, 436, 'energy.e_load_month_sum', rct_id.t_float, 'energy.e_load_month_sum')) 
    id_tab.append(rct_id(rct_id.g_energy, 0xA5341F4A, 443, 'energy.e_grid_feed_month_sum', rct_id.t_float, 'energy.e_grid_feed_month_sum')) 
    id_tab.append(rct_id(rct_id.g_energy, 0xA59C8428, 445, 'energy.e_ext_total', rct_id.t_float, 'External total energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xAF64D0FE, 467, 'energy.e_dc_year[0]', rct_id.t_float, 'Solar generator A year energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xB1EF67CE, 474, 'energy.e_ac_total', rct_id.t_float, 'Total energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xB7B2967F, 490, 'energy.e_dc_total_sum[0]', rct_id.t_float, 'energy.e_dc_total_sum[0]'))
    id_tab.append(rct_id(rct_id.g_energy, 0xB9A026F9, 499, 'energy.e_ext_day', rct_id.t_float, 'External day energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xBD55905F, 508, 'energy.e_ac_day', rct_id.t_float, 'Day energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xBD55D796, 509, 'energy.e_dc_year[1]', rct_id.t_float, 'Solar generator B year energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xC0CC81B6, 518, 'energy.e_ac_year', rct_id.t_float, 'Year energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xC7D3B479, 539, 'energy.e_load_year', rct_id.t_float, 'Household year energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xC9D76279, 543, 'energy.e_dc_day_sum[0]', rct_id.t_float, 'energy.e_dc_day_sum[0]'))
    id_tab.append(rct_id(rct_id.g_energy, 0xD9D66B76, 569, 'energy.e_grid_load_year_sum', rct_id.t_float, 'energy.e_grid_load_year_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0xDA207111, 572, 'energy.e_grid_load_month_sum', rct_id.t_float, 'energy.e_grid_load_month_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0xDE17F021, 584, 'energy.e_grid_load_year', rct_id.t_float, 'Year energy grid load', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xEAEEB3CA, 611, 'energy.e_dc_month_sum[0]', rct_id.t_float, 'energy.e_dc_month_sum[0]')) 
    id_tab.append(rct_id(rct_id.g_energy, 0xEFF4B537, 622, 'energy.e_load_total', rct_id.t_float, 'Household total energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xF0BE6429, 628, 'energy.e_load_month', rct_id.t_float, 'Household month energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xFBF3CE97, 661, 'energy.e_dc_day[1]', rct_id.t_float, 'Solar generator B day energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xFBF8D63C, 663, 'energy.e_grid_load_day_sum', rct_id.t_float, 'energy.e_grid_load_day_sum')) 
    id_tab.append(rct_id(rct_id.g_energy, 0xFC1C614E, 664, 'energy.e_ac_month_sum', rct_id.t_float, 'energy.e_ac_month_sum'))
    id_tab.append(rct_id(rct_id.g_energy, 0xFC724A9E, 665, 'energy.e_dc_total[0]', rct_id.t_float, 'Solar generator A total energy', 'Wh'))
    id_tab.append(rct_id(rct_id.g_energy, 0xFDB81124, 669, 'energy.e_grid_feed_day_sum', rct_id.t_float, 'energy.e_grid_feed_day_sum'))    

    id_tab.append(rct_id(rct_id.g_grid_mon, 0x16109E1, 1, 'grid_mon[0].u_over.time', rct_id.t_float, 'Max.voltage switch - off time level 1', 's')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x3044195F, 118, 'grid_mon[1].u_under.time', rct_id.t_float))
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x3CB1EF01, 157, 'grid_mon[0].u_under.threshold', rct_id.t_float, 'Min. voltage level 1', 'V')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x3E722B43, 160, 'grid_mon[1].f_under.threshold', rct_id.t_float, 'Min. frequency level 2', 'Hz'))
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x5438B68E, 218, 'grid_mon[1].u_over.threshold', rct_id.t_float, 'Max. voltage level 2', 'V')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x70E28322, 305, 'grid_mon[0].f_under.time', rct_id.t_float, 'Min. frequency switch-off time level 1', 's')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x82CD1525, 354, 'grid_mon[1].u_under.threshold', rct_id.t_float, 'Min. voltage level 2', 'V')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x915CD4A4, 396, 'grid_mon[1].f_over.threshold', rct_id.t_float, 'Max. frequency level 2', 'Hz')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0x933F9A24, 406, 'grid_mon[0].f_over.time', rct_id.t_float, 'Max. frequency switch-off time level 1', 's')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xA6271C2E, 448, 'grid_mon[0].u_over.threshold', rct_id.t_float, 'Max. voltage level 1', 'V')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xA95AD038, 458, 'grid_mon[0].f_under.threshold', rct_id.t_float, 'Min. frequency level 1', 'Hz')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xEBF7A4E8, 615, 'grid_mon[0].f_over.threshold', rct_id.t_float, 'Max. frequency level 1', 'Hz')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xEF89568B, 620, 'grid_mon[0].u_under.time', rct_id.t_float, 'Min. voltage switch-off time level 1', 's')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xF09CC4A2, 625, 'grid_mon[1].u_over.time', rct_id.t_float, 'Max. voltage switch-off time level 2', 's')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xF1FA5BB9, 631, 'grid_mon[1].f_under.time', rct_id.t_float, 'Min. frequency switch-off time level 2', 's')) 
    id_tab.append(rct_id(rct_id.g_grid_mon, 0xFD4F17C4, 668, 'grid_mon[1].f_over.time', rct_id.t_float, 'Max. frequency switch-off time level 2', 's')) 

    id_tab.append(rct_id(rct_id.g_temperature, 0x90B53336, 394, 'temperature.sink_temp_power_reduction', rct_id.t_float, 'Heat sink temperature target', 'Grad C')) 
    id_tab.append(rct_id(rct_id.g_temperature, 0xA7447FC4, 451, 'temperature.bat_temp_power_reduction', rct_id.t_float, 'Battery actuator temperature target', 'Grad C')) 

    id_tab.append(rct_id(rct_id.g_battery, 0x1676FA6, 2, 'battery.cells_stat[3]', rct_id.t_string, 'battery.cells_stat[3]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x3D9C51F, 7, 'battery.cells_stat[0].u_max.value', rct_id.t_float, 'battery.cells_stat[0].u_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x56162CA, 8, 'battery.cells_stat[4].u_min.time', rct_id.t_uint32, 'battery.cells_stat[4].u_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x56417DF, 9, 'battery.cells_stat[3].t_max.index', rct_id.t_uint8, 'battery.cells_stat[3].t_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x64A60FE, 12, 'battery.cells_stat[4].t_max.index', rct_id.t_uint8))
    id_tab.append(rct_id(rct_id.g_battery, 0x6A9FFA2, 14, 'battery.charged_amp_hours', rct_id.t_float, 'Total charge flow into battery', 'Ah'))
    id_tab.append(rct_id(rct_id.g_battery, 0x77692DE, 17, 'battery.cells_stat[4].u_max.index', rct_id.t_uint8, 'battery.cells_stat[4].u_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x86C75B0, 20, 'battery.stack_software_version[3]', rct_id.t_uint32, 'Software version stack 3'))
    id_tab.append(rct_id(rct_id.g_battery, 0x9923C1E, 23, 'battery.cells_stat[3].t_min.index', rct_id.t_uint8, 'battery.cells_stat[3].t_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xCFA8BC4, 33, 'battery.stack_cycles[1]', rct_id.t_uint16, 'battery.stack_cycles[1]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xDACF21B, 34, 'battery.cells_stat[4]', rct_id.t_string, 'battery.cells_stat[4]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xDE3D20D, 35, 'battery.status2', rct_id.t_int32, 'Battery extra status'))
    id_tab.append(rct_id(rct_id.g_battery, 0xEF60C7E, 40, 'battery.cells_stat[3].u_max.value', rct_id.t_float, 'battery.cells_stat[3].u_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x120EC3B4, 49, 'battery.cells_stat[4].u_min.index', rct_id.t_uint8, 'battery.cells_stat[4].u_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x1348AB07, 52, 'battery.cells[4]', rct_id.t_string, 'battery.cells[4]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x162491E8, 56, 'battery.module_sn[5]', rct_id.t_string, 'Module 5 Serial Number'))
    id_tab.append(rct_id(rct_id.g_battery, 0x16A1F844, 57, 'battery.bms_sn', rct_id.t_string, 'BMS Serial Number'))
    id_tab.append(rct_id(rct_id.g_battery, 0x18D1E9E0, 62, 'battery.cells_stat[5].u_max.index', rct_id.t_uint8, 'battery.cells_stat[5].u_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x18F98B6D, 63, 'battery.cells_stat[3].u_min.value', rct_id.t_float, 'battery.cells_stat[3].u_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x1B39A3A3, 68, 'battery.bms_power_version', rct_id.t_uint32, 'Software version BMS Power'))
    id_tab.append(rct_id(rct_id.g_battery, 0x1E5FCA70, 75, 'battery.maximum_charge_current', rct_id.t_float, 'Max. charge current', 'A')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x1F73B6A4, 76, 'battery.cells_stat[3].t_max.time', rct_id.t_uint32, 'battery.cells_stat[3].t_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x21961B58, 81, 'battery.current', rct_id.t_float, 'Battery current', 'A')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x23E55DA0, 87, 'battery.cells_stat[5]', rct_id.t_string, 'battery.cells_stat[5]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x257B5945, 92, 'battery.cells_stat[2].u_min.index', rct_id.t_uint8, 'battery.cells_stat[2].u_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x257B7612, 93, 'battery.module_sn[3]', rct_id.t_string, 'Module 3 Serial Number'))
    id_tab.append(rct_id(rct_id.g_battery, 0x26363AAE, 95, 'battery.cells_stat[1].t_max.index', rct_id.t_uint8, 'battery.cells_stat[1].t_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x265EACF6, 96, 'battery.cells_stat[2].t_max.time', rct_id.t_uint32, 'battery.cells_stat[2].t_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x27C39CEA, 102, 'battery.stack_cycles[6]', rct_id.t_uint16, 'battery.stack_cycles[6]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x2A30A97E, 108, 'battery.stack_cycles[5]', rct_id.t_uint16, 'battery.stack_cycles[5]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x2AACCAA7, 110, 'battery.max_cell_voltage', rct_id.t_float, 'battery.max_cell_voltage'))
    id_tab.append(rct_id(rct_id.g_battery, 0x2BC1E72B, 112, 'battery.discharged_amp_hours', rct_id.t_float, 'Total charge flow from battery', 'Ah')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x331D0689, 122, 'battery.cells_stat[2].t_max.value', rct_id.t_float, 'battery.cells_stat[2].t_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x336415EA, 123, 'battery.cells_stat[0].t_max.time', rct_id.t_uint32, 'battery.cells_stat[0].t_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x34A164E7, 126, 'battery.cells_stat[0]', rct_id.t_string, 'battery.cells_stat[0]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x34E33726, 127, 'battery.cells_stat[2].u_max.index', rct_id.t_uint8, 'battery.cells_stat[2].u_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x3503B92D, 130, 'battery.cells_stat[3].u_max.time', rct_id.t_uint32, 'battery.cells_stat[3].u_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x381B8BF9, 138, 'battery.soh', rct_id.t_float, 'SOH (State of Health)'))
    id_tab.append(rct_id(rct_id.g_battery, 0x3A7D5F53, 145, 'battery.cells_stat[1].u_max.value', rct_id.t_float, 'battery.cells_stat[1].u_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x3BA1B77B, 153, 'battery.cells_stat[3].t_min.value', rct_id.t_float, 'battery.cells_stat[3].t_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x3F98F58A, 163, 'battery.cells_stat[5].t_max.index', rct_id.t_uint8, 'battery.cells_stat[5].t_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x40FF01B7, 166, 'battery.cells[6]', rct_id.t_string, 'battery.cells[6]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x41B11ECF, 167, 'battery.cells_stat[3].u_min.index', rct_id.t_uint8, 'battery.cells_stat[3].u_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x428CCF46, 168, 'battery.cells_stat[5].u_min.value', rct_id.t_float, 'battery.cells_stat[5].u_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x442A3409, 176, 'battery.cells_stat[4].t_min.time', rct_id.t_uint32, 'battery.cells_stat[4].t_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x4443C661, 177, 'battery.cells_stat[0].t_max.index', rct_id.t_uint8, 'battery.cells_stat[0].t_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0x4B51A539, 189, 'battery.prog_sn', rct_id.t_string, 'battery.prog_sn'))
    id_tab.append(rct_id(rct_id.g_battery, 0x4CB7C0DC, 196, 'battery.min_cell_voltage', rct_id.t_float, 'battery.min_cell_voltage'))
    id_tab.append(rct_id(rct_id.g_battery, 0x4D985F33, 197, 'battery.cells_stat[5].u_max.value', rct_id.t_float, 'battery.cells_stat[5].u_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x4E699086, 203, 'battery.module_sn[4]', rct_id.t_string, 'Module 4 Serial Number'))
    id_tab.append(rct_id(rct_id.g_battery, 0x501A162D, 209, 'battery.cells_resist[5]', rct_id.t_string, 'battery.cells_resist[5]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x50514732, 210, 'battery.cells_stat[6].u_min.index', rct_id.t_uint8, 'battery.cells_stat[6].u_min.index')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x518C7BBE, 213, 'battery.cells_stat[5].u_min.time', rct_id.t_uint32, 'battery.cells_stat[5].u_min.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x537C719F, 215, 'battery.cells_stat[0].t_max.value', rct_id.t_float, 'battery.cells_stat[0].t_max.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x5570401B, 223, 'battery.stored_energy', rct_id.t_float, 'Total energy flow into battery', 'Wh'))
    id_tab.append(rct_id(rct_id.g_battery, 0x55DDF7BA, 225, 'battery.max_cell_temperature', rct_id.t_float, 'battery.max_cell_temperature')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x5939EC5D, 232, 'battery.module_sn[6]', rct_id.t_string, 'Module 6 Serial Number')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x5A120CE4, 234, 'battery.cells_stat[1].t_max.time', rct_id.t_uint32, 'battery.cells_stat[1].t_max.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x5A9EEFF0, 236, 'battery.stack_cycles[4]', rct_id.t_uint16, 'battery.stack_cycles[4]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x5AF50FD7, 237, 'battery.cells_stat[4].t_min.value', rct_id.t_float, 'battery.cells_stat[4].t_min.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x5BA122A5, 239, 'battery.stack_cycles[2]', rct_id.t_uint16, 'battery.stack_cycles[2]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x60749E5E, 251, 'battery.cells_stat[6].u_min.time', rct_id.t_uint32, 'battery.cells_stat[6].u_min.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x61EAC702, 254, 'battery.cells_stat[0].t_min.value', rct_id.t_float, 'battery.cells_stat[0].t_min.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x6213589B, 255, 'battery.cells_stat[6].u_min.value', rct_id.t_float, 'battery.cells_stat[6].u_min.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x62D645D9, 258, 'battery.cells[5]', rct_id.t_string, 'battery.cells[5]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x6388556C, 261, 'battery.stack_software_version[0]', rct_id.t_uint32, 'Software version stack 0')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x6445D856, 262, 'battery.cells_stat[1].u_min.index', rct_id.t_uint8, 'battery.cells_stat[1].u_min.index')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x649B10DA, 264, 'battery.cells_resist[0]', rct_id.t_string, 'battery.cells_resist[0]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x65EED11B, 268, 'battery.voltage', rct_id.t_float, 'Battery voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x6974798A, 279, 'battery.stack_software_version[6]', rct_id.t_uint32, 'Software version stack 6')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x69B8FF28, 281, 'battery.cells[2]', rct_id.t_string, 'battery.cells[2]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x6DB1FDDC, 292, 'battery.cells_stat[4].u_min.value', rct_id.t_float, 'battery.cells_stat[4].u_min.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x6E24632E, 295, 'battery.cells_stat[5].u_max.time', rct_id.t_uint32, 'battery.cells_stat[5].u_max.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x6E491B50, 296, 'battery.maximum_charge_voltage', rct_id.t_float, 'Max. charge voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x70349444, 302, 'battery.cells_stat[1].t_min.index', rct_id.t_uint8, 'battery.cells_stat[1].t_min.index')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x70A2AF4F, 303, 'battery.bat_status', rct_id.t_int32, 'battery.bat_status')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x71196579, 306, 'battery.cells_stat[5].t_min.index', rct_id.t_uint8, 'battery.cells_stat[5].t_min.index')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x71765BD8, 309, 'battery.status', rct_id.t_int32, 'Battery status')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x71CB0B57, 311, 'battery.cells_resist[1]', rct_id.t_string, 'battery.cells_resist[1]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x7268CE4D, 314, 'battery.inv_cmd', rct_id.t_uint32, 'battery.inv_cmd')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x73489528, 317, 'battery.module_sn[2]', rct_id.t_string, 'Module 2 Serial Number')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x74FD4609, 319, 'battery.cells_stat[2]', rct_id.t_string, 'battery.cells_stat[2]')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x770A6E7C, 324, 'battery.cells_stat[0].u_max.index', rct_id.t_uint8, 'battery.cells_stat[0].u_max.index')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x7E590128, 343, 'battery.cells_stat[0].u_max.time', rct_id.t_uint32, 'battery.cells_stat[0].u_max.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x7F42BB82, 344, 'battery.cells_stat[6].u_max.index', rct_id.t_uint8, 'battery.cells_stat[6].u_max.index')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x7FF6252C, 346, 'battery.cells_stat[5].t_max.time', rct_id.t_uint32, 'battery.cells_stat[5].t_max.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x804A3266, 347, 'battery.cells_stat[6].u_max.value', rct_id.t_float, 'battery.cells_stat[6].u_max.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x8160539D, 350, 'battery.cells_stat[4].t_max.value', rct_id.t_float, 'battery.cells_stat[4].t_max.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x885BB57E, 365, 'battery.cells_stat[6].t_min.value', rct_id.t_float, 'battery.cells_stat[6].t_min.value')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x889DC27F, 367, 'battery.cells_stat[0].u_min.value', rct_id.t_float, 'battery.cells_stat[0].u_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x88BBF8CB, 368, 'battery.cells_stat[5].t_min.value', rct_id.t_float, 'battery.cells_stat[5].t_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x89B25F4B, 372, 'battery.stack_cycles[3]', rct_id.t_uint16, 'battery.stack_cycles[3]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x8B9FF008, 375, 'battery.soc_target', rct_id.t_float, 'Target SOC'))
    id_tab.append(rct_id(rct_id.g_battery, 0x8BB08839, 376, 'battery.cells_stat[6].t_min.time', rct_id.t_uint32, 'battery.cells_stat[6].t_min.time')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x8DFFDD33, 380, 'battery.cells_stat[3].u_min.time', rct_id.t_uint32, 'battery.cells_stat[3].u_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x8EC23427, 383, 'battery.cells_stat[4].u_max.time', rct_id.t_uint32, 'battery.cells_stat[4].u_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x8EF6FBBD, 385, 'battery.cells[1]', rct_id.t_string, 'battery.cells[1]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x8EF9C9B8, 386, 'battery.cells_stat[6].t_max.time', rct_id.t_uint32, 'battery.cells_stat[6].t_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x902AFAFB, 389, 'battery.temperature', rct_id.t_float, 'Battery temperature', 'Grad C')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x90832471, 393, 'battery.cells_stat[1].u_max.time', rct_id.t_uint32, 'battery.cells_stat[1].u_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x91C325D9, 399, 'battery.cells_stat[0].t_min.time', rct_id.t_uint32, 'battery.cells_stat[0].t_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0x91FB68CD, 400, 'battery.cells_stat[6].t_max.value', rct_id.t_float, 'battery.cells_stat[6].t_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0x959930BF, 413, 'battery.soc', rct_id.t_float, 'SOC (State of charge)')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x99396810, 422, 'battery.module_sn[1]', rct_id.t_string, 'Module 1 Serial Number')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x993C06F6, 423, 'battery.cells_resist[3]', rct_id.t_string, 'battery.cells_resist[3]'))
    id_tab.append(rct_id(rct_id.g_battery, 0x9D785E8C, 429, 'battery.bms_software_version', rct_id.t_uint32, 'Software version BMS Master')) 
    id_tab.append(rct_id(rct_id.g_battery, 0x9E314430, 432, 'battery.cells_stat[2].u_max.time', rct_id.t_uint32, 'battery.cells_stat[2].u_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xA10D9A4B, 434, 'battery.min_cell_temperature', rct_id.t_float, 'battery.min_cell_temperature')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xA3E48B21, 440, 'battery.cells_stat[2].t_min.value', rct_id.t_float, 'battery.cells_stat[2].t_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xA40906BF, 441, 'battery.stack_software_version[4]', rct_id.t_uint32, 'Software version stack 4')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xA54C4685, 444, 'battery.stack_software_version[1]', rct_id.t_uint32, 'Software version stack 1')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xA616B022, 447, 'battery.soc_target_low', rct_id.t_float))
    id_tab.append(rct_id(rct_id.g_battery, 0xA6871A4D, 449, 'battery.cells_stat[4].t_min.index', rct_id.t_uint8, 'battery.cells_stat[4].t_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xA6C4FD4A, 450, 'battery.stack_cycles[0]', rct_id.t_uint16, 'battery.stack_cycles[0]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xA7DBD28C, 454, 'battery.cells_stat[2].t_max.index', rct_id.t_uint8, 'battery.cells_stat[2].t_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xA7FE5C0C, 456, 'battery.cells_stat[2].t_min.index', rct_id.t_uint8, 'battery.cells_stat[2].t_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xA9033880, 457, 'battery.used_energy', rct_id.t_float, 'Total energy flow from battery', 'Wh'))
    id_tab.append(rct_id(rct_id.g_battery, 0xAACAC898, 462, 'battery.cells_stat[4].t_max.time', rct_id.t_uint32, 'battery.cells_stat[4].t_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xACF7666B, 465, 'battery.efficiency', rct_id.t_float, 'Battery efficiency (used energy / stored energy)'))
    id_tab.append(rct_id(rct_id.g_battery, 0xB0EBE75A, 471, 'battery.minimum_discharge_voltage', rct_id.t_float, 'Min. discharge voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xB4E053D4, 483, 'battery.cells_stat[1].u_min.value', rct_id.t_float, 'battery.cells_stat[1].u_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xB57B59BD, 486, 'battery.ah_capacity', rct_id.t_float, 'Battery capacity', 'Ah')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xB81FB399, 492, 'battery.cells_stat[2].u_min.time', rct_id.t_uint32, 'battery.cells_stat[2].u_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xB84A38AB, 494, 'battery.soc_target_high', rct_id.t_float))
    id_tab.append(rct_id(rct_id.g_battery, 0xB9E09F78, 500, 'battery.cells_stat[5].u_min.index', rct_id.t_uint8, 'battery.cells_stat[5].u_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xBB302278, 501, 'battery.cells_stat[1].t_min.time', rct_id.t_uint32, 'battery.cells_stat[1].t_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xBDE3BF0A, 510, 'battery.cells_stat[6].t_max.index', rct_id.t_uint8, 'battery.cells_stat[6].t_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xC0680302, 515, 'battery.cells_stat[2].t_min.time', rct_id.t_uint32, 'battery.cells_stat[2].t_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xC0DF2978, 519, 'battery.cycles', rct_id.t_int32, 'Battery charge / discharge cycles')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xC42F5807, 529, 'battery.cells_stat[1].u_max.index', rct_id.t_uint8, 'battery.cells_stat[1].u_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xC6DA81A0, 534, 'battery.cells_stat[6].u_max.time', rct_id.t_uint32, 'battery.cells_stat[6].u_max.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xC8609C8E, 540, 'battery.cells[3]', rct_id.t_string, 'battery.cells[3]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xC88EB032, 541, 'battery.cells_stat[0].u_min.time', rct_id.t_uint32, 'battery.cells_stat[0].u_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xC8BA1729, 542, 'battery.stack_software_version[2]', rct_id.t_uint32, 'Software version stack 2')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xD0C47326, 554, 'battery.cells_stat[1].t_min.value', rct_id.t_float, 'battery.cells_stat[1].t_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xD60E7A2F, 567, 'battery.cells_stat[1].u_min.time', rct_id.t_uint32, 'battery.cells_stat[1].u_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xDD5930A2, 581, 'battery.cells_stat[0].t_min.index', rct_id.t_uint8, 'battery.cells_stat[0].t_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xDE9CBCB0, 586, 'battery.cells_stat[5].t_max.value', rct_id.t_float, 'battery.cells_stat[5].t_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xDEE1957F, 587, 'battery.cells_resist[4]', rct_id.t_string, 'battery.cells_resist[4]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xDF0A735C, 588, 'battery.maximum_discharge_current', rct_id.t_float, 'Max. discharge current', 'A')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xDFF966E3, 591, 'battery.cells_stat[6].t_min.index', rct_id.t_uint8, 'battery.cells_stat[6].t_min.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xE7177DEE, 607, 'battery.cells_stat[2].u_max.value', rct_id.t_float, 'battery.cells_stat[2].u_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xEB4C2597, 612, 'battery.cells_resist[6]', rct_id.t_string, 'battery.cells_resist[6]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xEEA3F59B, 618, 'battery.stack_software_version[5]', rct_id.t_uint32, 'Software version stack 5'))
    id_tab.append(rct_id(rct_id.g_battery, 0xEECDFEFC, 619, 'battery.cells_stat[2].u_min.value', rct_id.t_float, 'battery.cells_stat[2].u_min.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xEFD3EC8A, 621, 'battery.cells_stat[5].t_min.time', rct_id.t_uint32, 'battery.cells_stat[5].t_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xF044EDA0, 623, 'battery.cells_stat[3].t_max.value', rct_id.t_float))
    id_tab.append(rct_id(rct_id.g_battery, 0xF257D342, 635, 'battery.cells_stat[1].t_max.value', rct_id.t_float, 'battery.cells_stat[1].t_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xF3FD8CE6, 640, 'battery.cells_resist[2]', rct_id.t_string, 'battery.cells_resist[2]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xF54BC06D, 644, 'battery.cells_stat[4].u_max.value', rct_id.t_float, 'battery.cells_stat[4].u_max.value'))
    id_tab.append(rct_id(rct_id.g_battery, 0xF8C0D255, 651, 'battery.cells[0]', rct_id.t_string, 'battery.cells[0]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xF99E8CC8, 653, 'battery.cells_stat[6]', rct_id.t_string, 'battery.cells_stat[6]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xFA3276DC, 654, 'battery.cells_stat[3].t_min.time', rct_id.t_uint32, 'battery.cells_stat[3].t_min.time'))
    id_tab.append(rct_id(rct_id.g_battery, 0xFB796780, 659, 'battery.cells_stat[1]', rct_id.t_string, 'battery.cells_stat[1]'))
    id_tab.append(rct_id(rct_id.g_battery, 0xFBF6D834, 662, 'battery.module_sn[0]', rct_id.t_string, 'Module 0 Serial Number')) 
    id_tab.append(rct_id(rct_id.g_battery, 0xFDBD9EE9, 670, 'battery.cells_stat[3].u_max.index', rct_id.t_uint8, 'battery.cells_stat[3].u_max.index'))
    id_tab.append(rct_id(rct_id.g_battery, 0xFE44BA26, 672, 'battery.cells_stat[0].u_min.index', rct_id.t_uint8, 'battery.cells_stat[0].u_min.index'))

    id_tab.append(rct_id(rct_id.g_cs_neg, 0x19C0B60, 3, 'cs_neg[2]', rct_id.t_float, 'Miltiply value of the current sensor 2 by'))
    id_tab.append(rct_id(rct_id.g_cs_neg, 0x4C12C4C7, 192, 'cs_neg[1]', rct_id.t_float, 'Miltiply value of the current sensor 1 by')) 
    id_tab.append(rct_id(rct_id.g_cs_neg, 0x82258C01, 353, 'cs_neg[0]', rct_id.t_float, 'Miltiply value of the current sensor 0 by'))

    id_tab.append(rct_id(rct_id.g_hw_test, 0x39BDE11, 5, 'hw_test.state', rct_id.t_uint8, 'hw_test.state'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x58F1759, 10, 'hw_test.bt_power[6]', rct_id.t_float, 'hw_test.bt_power[6]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x875C906, 21, 'hw_test.bt_time[2]', rct_id.t_float, 'hw_test.bt_time[2]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x2082BFB6, 79, 'hw_test.bt_time[9]', rct_id.t_float, 'hw_test.bt_time[9]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x3CA8E8D0, 156, 'hw_test.bt_time[0]', rct_id.t_float, 'hw_test.bt_time[0]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x3D789979, 158, 'hw_test.bt_power[7]', rct_id.t_float, 'hw_test.bt_power[7]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x4E2B42A4, 200, 'hw_test.bt_power[0]', rct_id.t_float, 'hw_test.bt_power[0]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x4E77B2CE, 204, 'hw_test.bt_cycle', rct_id.t_uint8, 'hw_test.bt_cycle'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x58378BD0, 228, 'hw_test.bt_time[3]', rct_id.t_float, 'hw_test.bt_time[3]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x6BFF1AF4, 285, 'hw_test.bt_power[2]', rct_id.t_float, 'hw_test.bt_power[2]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x71B70DCE, 310, 'hw_test.bt_power[4]', rct_id.t_float, 'hw_test.bt_power[4]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x75AE19ED, 320, 'hw_test.hw_switch_time', rct_id.t_float, 'hw_test.hw_switch_time'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x77DD4364, 326, 'hw_test.bt_time[5]', rct_id.t_float, 'hw_test.bt_time[5]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x86782D58, 360, 'hw_test.bt_power[9]', rct_id.t_float, 'hw_test.bt_power[9]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x903FE89E, 390, 'hw_test.bt_time[8]', rct_id.t_float, 'hw_test.bt_time[8]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x9214A00C, 401, 'hw_test.booster_test_index', rct_id.t_uint8, 'hw_test.booster_test_index'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0x940569AC, 411, 'hw_test.bt_time[6]', rct_id.t_float, 'hw_test.bt_time[6]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xB082C4D7, 470, 'hw_test.bt_power[5]', rct_id.t_float, 'hw_test.bt_power[5]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xC1C82889, 521, 'hw_test.bt_power[1]', rct_id.t_float, 'hw_test.bt_power[1]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xC3C7325E, 527, 'hw_test.bt_time[4]', rct_id.t_float, 'hw_test.bt_time[4]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xC66A522B, 533, 'hw_test.bt_time[1]', rct_id.t_float, 'hw_test.bt_time[1]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xC707102E, 535, 'hw_test.bt_power[3]', rct_id.t_float, 'hw_test.bt_power[3]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xCBEC8200, 549, 'hw_test.timer2', rct_id.t_float, 'hw_test.timer2'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xD4C4A941, 563, 'hw_test.bt_time[7]', rct_id.t_float, 'hw_test.bt_time[7]'))
    id_tab.append(rct_id(rct_id.g_hw_test, 0xE6248312, 603, 'hw_test.bt_power[8]', rct_id.t_float, 'hw_test.bt_power[8]'))    

    id_tab.append(rct_id(rct_id.g_g_sync, 0x3A39CA2, 6, 'g_sync.p_ac_load[0]', rct_id.t_float, 'g_sync.p_ac_load[0]'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0xA04CA7F, 24, 'g_sync.u_zk_n_avg', rct_id.t_float, 'Negative buffer capacitor voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x147E8E26, 53, 'g_sync.p_ac[1]', rct_id.t_float, 'AC2')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x1AC87AA0, 67, 'g_sync.p_ac_load_sum_lp', rct_id.t_float, 'Load household - external Power', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x24150B85, 89, 'g_sync.u_zk_sum_mov_avg', rct_id.t_float, 'Actual DC link voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x2545E22D, 91, 'g_sync.u_l_rms[2]', rct_id.t_float, 'AC voltage phase 3', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x2788928C, 100, 'g_sync.p_ac_load[1]', rct_id.t_float, 'g_sync.p_ac_load[1]'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x27BE51D9, 101, 'g_sync.p_ac_sc[0]', rct_id.t_float, 'Grid power phase 1', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x3A444FC6, 144, 'g_sync.s_ac_lp[0]', rct_id.t_float, 'Apparent power phase 1', 'VA'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x400F015B, 164, 'g_sync.p_acc_lp', rct_id.t_float, 'Battery power', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x4077335D, 165, 'g_sync.s_ac_lp[1]', rct_id.t_float, 'Apparent power phase 2', 'VA'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x43257820, 170, 'g_sync.p_ac[0]', rct_id.t_float, 'AC1')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x485AD749, 183, 'g_sync.u_ptp_rms[1]', rct_id.t_float, 'Phase to phase voltage 2', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x48D73FA5, 185, 'g_sync.i_dr_lp[2]', rct_id.t_float, 'Current phase 3 (average)', 'A')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x4E49AEC5, 202, 'g_sync.p_ac_sum', rct_id.t_float, 'Real power', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x54B4684E, 220, 'g_sync.u_l_rms[1]', rct_id.t_float, 'AC voltage phase 2', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x55C22966, 224, 'g_sync.s_ac[2]', rct_id.t_float))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x6002891F, 250, 'g_sync.p_ac_sc_sum', rct_id.t_float, 'Grid power (ext. sensors)', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x612F7EAB, 253, 'g_sync.s_ac[1]', rct_id.t_float, 'Apparent power phase 2', 'VA'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x63476DBE, 260, 'g_sync.u_ptp_rms[0]', rct_id.t_float, 'Phase to phase voltage 1', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x650C1ED7, 265, 'g_sync.i_dr_eff[1]', rct_id.t_float, 'Current phase 2', 'A')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x6E1C5B78, 294, 'g_sync.p_ac_lp[1]', rct_id.t_float, 'AC power phase 2', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x71E10B51, 312, 'g_sync.p_ac_lp[0]', rct_id.t_float, 'AC power phase 1', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x7C78CBAC, 339, 'g_sync.q_ac_sum_lp', rct_id.t_float, 'Reactive power', 'var'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x82E3C121, 355, 'g_sync.q_ac[1]', rct_id.t_float, 'Reactive power phase 2', 'var'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x883DE9AB, 364, 'g_sync.s_ac_lp[2]', rct_id.t_float, 'Apparent power phase 3', 'VA'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0x887D43C4, 366, 'g_sync.i_dr_lp[0]', rct_id.t_float, 'Current phase 1 (average)', 'A')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x89EE3EB5, 373, 'g_sync.i_dr_eff[0]', rct_id.t_float, 'Current phase 1', 'A')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x8A18539B, 374, 'g_sync.u_zk_sum_avg', rct_id.t_float, 'DC link voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x91617C58, 397, 'g_sync.p_ac_grid_sum_lp', rct_id.t_float, 'Total grid power', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0x92BC682B, 405, 'g_sync.i_dr_eff[2]', rct_id.t_float, 'Current phase 3', 'A')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xB0041187, 468, 'g_sync.u_sg_avg[1]', rct_id.t_float, 'Solar generator B voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xB221BCFA, 476, 'g_sync.p_ac_sc[2]', rct_id.t_float, 'Grid power phase 3', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xB55BA2CE, 485, 'g_sync.u_sg_avg[0]', rct_id.t_float, 'Solar generator A voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xB9928C51, 498, 'g_sync.p_ac_lp[2]', rct_id.t_float, 'AC power phase 3', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xBCA77559, 503, 'g_sync.q_ac[2]', rct_id.t_float, 'Reactive power phase 3', 'var'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0xC03462F6, 514, 'g_sync.p_ac[2]', rct_id.t_float, 'AC3')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xC198B25B, 520, 'g_sync.u_zk_p_avg', rct_id.t_float, 'Positive buffer capacitor voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xCABC44CA, 545, 'g_sync.s_ac[0]', rct_id.t_float, 'Apparent power phase 1', 'VA'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0xCF053085, 553, 'g_sync.u_l_rms[0]', rct_id.t_float, 'AC voltage phase 1', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xDB2D69AE, 575, 'g_sync.p_ac_sum_lp', rct_id.t_float, 'AC power', 'W')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xDCA1CF26, 579, 'g_sync.s_ac_sum_lp', rct_id.t_float, 'Apparent power', 'VA'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0xDCAC0EA9, 580, 'g_sync.i_dr_lp[1]', rct_id.t_float, 'Current phase 2 (average)', 'A')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xE94C2EFC, 608, 'g_sync.q_ac[0]', rct_id.t_float, 'Reactive power phase 1', 'var'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0xF0B436DD, 627, 'g_sync.p_ac_load[2]', rct_id.t_float, 'g_sync.p_ac_load[2]'))
    id_tab.append(rct_id(rct_id.g_g_sync, 0xF25C339B, 636, 'g_sync.u_ptp_rms[2]', rct_id.t_float, 'Phase to phase voltage 3', 'V')) 
    id_tab.append(rct_id(rct_id.g_g_sync, 0xF5584F90, 645, 'g_sync.p_ac_sc[1]', rct_id.t_float, 'Grid power phase 2', 'W')) 

    id_tab.append(rct_id(rct_id.g_logger, 0x5C7CFB1, 11, 'logger.day_egrid_load_log_ts', rct_id.t_int32, 'logger.day_egrid_load_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x64E4340, 13, 'logger.minutes_ubat_log_ts', rct_id.t_int32, 'logger.minutes_ubat_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x95AFAA8, 22, 'logger.minutes_ul3_log_ts', rct_id.t_int32, 'logger.minutes_ul3_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xDF164DE, 36, 'logger.day_eb_log_ts', rct_id.t_int32, 'logger.day_eb_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xFA29566, 42, 'logger.minutes_ub_log_ts', rct_id.t_int32, 'logger.minutes_ub_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x132AA71E, 51, 'logger.minutes_temp2_log_ts', rct_id.t_int32, 'logger.minutes_temp2_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x19B814F2, 65, 'logger.year_egrid_feed_log_ts', rct_id.t_int32))
    id_tab.append(rct_id(rct_id.g_logger, 0x1D49380A, 74, 'logger.minutes_eb_log_ts', rct_id.t_int32, 'logger.minutes_eb_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x21879805, 80, 'logger.minutes_eac1_log_ts', rct_id.t_int32, 'logger.minutes_eac1_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x2A449E89, 109, 'logger.year_log_ts', rct_id.t_int32, 'logger.year_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x2F0A6B15, 116, 'logger.month_ea_log_ts', rct_id.t_int32, 'logger.month_ea_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x34ECA9CA, 128, 'logger.year_eb_log_ts', rct_id.t_int32, 'logger.year_eb_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x3906A1D0, 141, 'logger.minutes_eext_log_ts', rct_id.t_int32, 'logger.minutes_eext_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x431509D1, 169, 'logger.month_eload_log_ts', rct_id.t_int32, 'logger.month_eload_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x488052BA, 184, 'logger.minutes_ul2_log_ts', rct_id.t_int32, 'logger.minutes_ul2_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x4C14CC7C, 193, 'logger.year_ea_log_ts', rct_id.t_int32, 'logger.year_ea_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x4E9D95A6, 205, 'logger.year_eext_log_ts', rct_id.t_int32, 'logger.year_eext_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x50B441C1, 212, 'logger.minutes_ea_log_ts', rct_id.t_int32, 'logger.minutes_ea_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x5293B668, 214, 'logger.minutes_soc_log_ts', rct_id.t_int32, 'logger.minutes_soc_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x5411CE1B, 217, 'logger.minutes_ul1_log_ts', rct_id.t_int32, 'logger.minutes_ul1_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x554D8FEE, 222, 'logger.minutes_eac2_log_ts', rct_id.t_int32, 'logger.minutes_eac2_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x5D34D09D, 245, 'logger.month_egrid_load_log_ts', rct_id.t_int32, 'logger.month_egrid_load_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x60A9A532, 252, 'logger.day_eext_log_ts', rct_id.t_int32, 'logger.day_eext_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x669D02FE, 270, 'logger.minutes_eac_log_ts', rct_id.t_int32, 'logger.minutes_eac_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x6B5A56C2, 282, 'logger.month_eb_log_ts', rct_id.t_int32, 'logger.month_eb_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x6F3876BC, 297, 'logger.error_log_time_stamp', rct_id.t_int32, 'Time stamp for error log reading')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x70BD7C46, 304, 'logger.year_eac_log_ts', rct_id.t_int32, 'logger.year_eac_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x72ACC0BF, 315, 'logger.minutes_ua_log_ts', rct_id.t_int32, 'logger.minutes_ua_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x76C9A0BD, 322, 'logger.minutes_soc_targ_log_ts', rct_id.t_int32, 'logger.minutes_soc_targ_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x921997EE, 402, 'logger.month_egrid_feed_log_ts', rct_id.t_int32, 'logger.month_egrid_feed_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x9247DB99, 403, 'logger.minutes_egrid_load_log_ts', rct_id.t_int32, 'logger.minutes_egrid_load_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0x9A51A23B, 426, 'logger.log_rate', rct_id.t_uint16, 'Data log resolution', 's')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xA60082A9, 446, 'logger.minutes_egrid_feed_log_ts', rct_id.t_int32, 'logger.minutes_egrid_feed_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xA7C708EB, 453, 'logger.minutes_eload_log_ts', rct_id.t_int32, 'logger.minutes_eload_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xB20D1AD6, 475, 'logger.day_egrid_feed_log_ts', rct_id.t_int32, 'logger.day_egrid_feed_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xC55EF32E, 531, 'logger.year_egrid_load_log_ts', rct_id.t_int32, 'logger.year_egrid_load_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xCA6D6472, 544, 'logger.day_eload_log_ts', rct_id.t_int32, 'logger.day_eload_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xCBDAD315, 548, 'logger.minutes_ebat_log_ts', rct_id.t_int32, 'logger.minutes_ebat_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xD3E94E6B, 560, 'logger.minutes_temp_bat_log_ts', rct_id.t_int32, 'logger.minutes_temp_bat_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xE04C3900, 592, 'logger.day_eac_log_ts', rct_id.t_int32, 'logger.day_eac_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xE29C24EB, 596, 'logger.minutes_eac3_log_ts', rct_id.t_int32, 'logger.minutes_eac3_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xE4DC040A, 600, 'logger.month_eext_log_ts', rct_id.t_int32, 'logger.month_eext_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xE5FBCC6F, 602, 'logger.year_eload_log_ts', rct_id.t_int32, 'logger.year_eload_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xF28341E2, 637, 'logger.month_eac_log_ts', rct_id.t_int32, 'logger.month_eac_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xF76DE445, 648, 'logger.minutes_temp_log_ts', rct_id.t_int32, 'logger.minutes_temp_log_ts')) 
    id_tab.append(rct_id(rct_id.g_logger, 0xFCF4E78D, 667, 'logger.day_ea_log_ts', rct_id.t_int32, 'logger.day_ea_log_ts')) 

    id_tab.append(rct_id(rct_id.g_wifi, 0xBA16A10, 27, 'wifi.sockb_protocol', rct_id.t_enum, 'wifi.sockb_protocol')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x14C0E627, 54, 'wifi.password', rct_id.t_string, 'WiFi password')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x1D0623D6, 72, 'wifi.dns_address', rct_id.t_string, 'DNS address')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x5673D737, 226, 'wifi.connect_to_wifi', rct_id.t_bool, 'wifi.connect_to_wifi')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x57429627, 227, 'wifi.authentication_method', rct_id.t_string, 'WiFi authentication method')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x5952E5E6, 233, 'wifi.mask', rct_id.t_string, 'Netmask')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x5A316247, 235, 'wifi.mode', rct_id.t_string, 'WiFi mode')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x6D7C0BF4, 291, 'wifi.sockb_port', rct_id.t_int32))
    id_tab.append(rct_id(rct_id.g_wifi, 0x76CAA9BF, 323, 'wifi.encryption_algorithm', rct_id.t_string, 'wifi.encryption_algorithm'))
    id_tab.append(rct_id(rct_id.g_wifi, 0x7B1F7FBE, 337, 'wifi.gateway', rct_id.t_string, 'Gateway')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x7DDE352B, 341, 'wifi.sockb_ip', rct_id.t_string, 'wifi.sockb_ip')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0x8CA00014, 377, 'wifi.result', rct_id.t_int8, 'WiFi result')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0xB4222BDE, 481, 'wifi.state', rct_id.t_uint8, 'wifi.state')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0xB7C85C51, 491, 'wifi.use_ethernet', rct_id.t_bool, 'wifi.use_ethernet')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0xD5790CE1, 565, 'wifi.use_wifi', rct_id.t_bool, 'Enable Wi-Fi Access Point')) 
    id_tab.append(rct_id(rct_id.g_wifi, 0xF8DECCE6, 652, 'wifi.connected_ap_ssid', rct_id.t_string, 'WiFi associated AP')) 

    id_tab.append(rct_id(rct_id.g_adc, 0x7C61FAD, 18, 'adc.u_ref_1_5v[0]', rct_id.t_uint16, 'Reference voltage 1', 'V')) 
    id_tab.append(rct_id(rct_id.g_adc, 0x16B28CCA, 59, 'adc.u_ref_1_5v[1]', rct_id.t_uint16, 'Reference voltage 2', 'V')) 
    id_tab.append(rct_id(rct_id.g_adc, 0x508FCE78, 211, 'adc.u_ref_1_5v[3]', rct_id.t_uint16, 'Reference voltage 4', 'V')) 
    id_tab.append(rct_id(rct_id.g_adc, 0x715C84A1, 308, 'adc.u_ref_1_5v[2]', rct_id.t_uint16, 'Reference voltage 3', 'V')) 
    id_tab.append(rct_id(rct_id.g_adc, 0xB84FDCF9, 495, 'adc.u_acc', rct_id.t_float, 'Battery voltage (inverter)', 'V'))    

    id_tab.append(rct_id(rct_id.g_net, 0x8679611, 19, 'net.id', rct_id.t_uint32, 'net.id')) 
    id_tab.append(rct_id(rct_id.g_net, 0xC3815C2, 28, 'net.load_reduction', rct_id.t_float, 'net.load_reduction')) 
    id_tab.append(rct_id(rct_id.g_net, 0x23F525DE, 88, 'net.command', rct_id.t_uint16, 'net.command')) 
    id_tab.append(rct_id(rct_id.g_net, 0x2E06172D, 113, 'net.net_tunnel_id', rct_id.t_uint32, 'net.net_tunnel_id')) 
    id_tab.append(rct_id(rct_id.g_net, 0x3500F1E8, 129, 'net.index', rct_id.t_int8, 'net.index'))
    id_tab.append(rct_id(rct_id.g_net, 0x36214C57, 133, 'net.prev_k', rct_id.t_float, 'net.prev_k')) 
    id_tab.append(rct_id(rct_id.g_net, 0x3AA565FC, 148, 'net.package', rct_id.t_string, 'net.package'))
    id_tab.append(rct_id(rct_id.g_net, 0x46635546, 180, 'net.n_descendants', rct_id.t_int8, 'Number of descendant slaves')) 
    id_tab.append(rct_id(rct_id.g_net, 0x5D1B0835, 244, 'net.use_network_filter', rct_id.t_bool, 'net.use_network_filter')) 
    id_tab.append(rct_id(rct_id.g_net, 0x5E540FB2, 246, 'net.update_slaves', rct_id.t_bool, 'Activate aut. update slaves')) 
    id_tab.append(rct_id(rct_id.g_net, 0x67C0A2F5, 273, 'net.slave_p_total', rct_id.t_float, 'net.slave_p_total')) 
    id_tab.append(rct_id(rct_id.g_net, 0x6DCC4097, 293, 'net.master_timeout', rct_id.t_float, 'net.master_timeout')) 
    id_tab.append(rct_id(rct_id.g_net, 0xBFFF3CAD, 513, 'net.n_slaves', rct_id.t_uint8, 'net.n_slaves')) 
    id_tab.append(rct_id(rct_id.g_net, 0xC0A7074F, 516, 'net.slave_data', rct_id.t_string, 'net.slave_data')) 
    id_tab.append(rct_id(rct_id.g_net, 0xD3085D80, 559, 'net.soc_av', rct_id.t_float, 'net.soc_av')) 
    id_tab.append(rct_id(rct_id.g_net, 0xD5205A45, 564, 'net.slave_timeout', rct_id.t_float, 'net.slave_timeout')) 
    id_tab.append(rct_id(rct_id.g_net, 0xDB62DCB7, 577, 'net.n_devices', rct_id.t_uint8, 'net.n_devices')) 

    id_tab.append(rct_id(rct_id.g_acc_conv, 0xB0FA4D23, 472, 'acc_conv.i_charge_max', rct_id.t_float, 'Max. battery converter charge current', 'A')) 
    id_tab.append(rct_id(rct_id.g_acc_conv, 0xB408E40A, 480, 'acc_conv.i_acc_lp_slow', rct_id.t_float, 'acc_conv.i_acc_lp_slow')) 
    id_tab.append(rct_id(rct_id.g_acc_conv, 0xC642B9D6, 532, 'acc_conv.i_discharge_max', rct_id.t_float, 'Max. battery converter discharge current', 'A')) 
    id_tab.append(rct_id(rct_id.g_acc_conv, 0xD9F9F35B, 571, 'acc_conv.state_slow', rct_id.t_uint8, 'acc_conv.state_slow')) 
    id_tab.append(rct_id(rct_id.g_acc_conv, 0xE3F4D1DF, 598, 'acc_conv.i_max', rct_id.t_float, 'Max. battery converter current', 'A')) 

    id_tab.append(rct_id(rct_id.g_dc_conv, 0xCB5D21B, 30, 'dc_conv.dc_conv_struct[1].p_dc_lp', rct_id.t_float, 'Solar generator B power', 'W')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x5BB8075A, 240, 'dc_conv.dc_conv_struct[1].u_sg_lp', rct_id.t_float, 'Solar generator B voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x5E942C62, 247, 'dc_conv.dc_conv_struct[1].mpp.fixed_voltage', rct_id.t_float, 'Fixed voltage Solar generator B', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x62B8940B, 257, 'dc_conv.start_voltage', rct_id.t_float, 'Inverter DC-voltage start value', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x6476A836, 263, 'dc_conv.dc_conv_struct[0].mpp.enable_scan', rct_id.t_bool, 'Enable rescan for global MPP on solar generator A')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x701A0482, 301, 'dc_conv.dc_conv_struct[0].enabled', rct_id.t_bool, 'Solar generator A connected')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x8DD1C728, 379, 'dc_conv.dc_conv_struct[1].mpp.enable_scan', rct_id.t_bool, 'Enable rescan for global MPP on solar generator B')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0x9E1A88F5, 431, 'dc_conv.dc_conv_struct[0].mpp.fixed_voltage', rct_id.t_float, 'Fixed voltage Solar generator A', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xAA9AA253, 461, 'dc_conv.dc_conv_struct[1].p_dc', rct_id.t_float, 'Solar generator B power', 'W')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xB298395D, 478, 'dc_conv.dc_conv_struct[0].u_sg_lp', rct_id.t_float, 'Solar generator A voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xB5317B78, 484, 'dc_conv.dc_conv_struct[0].p_dc', rct_id.t_float, 'Solar generator A power', 'W')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xB836B50C, 493, 'dc_conv.dc_conv_struct[1].rescan_correction', rct_id.t_float, 'Last global rescan MPP correction on input B', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xDB11855B, 574, 'dc_conv.dc_conv_struct[0].p_dc_lp', rct_id.t_float, 'Solar generator A power', 'W')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xDB45ABD0, 576, 'dc_conv.dc_conv_struct[0].rescan_correction', rct_id.t_float, 'Last global rescan MPP correction on input A', 'V')) 
    id_tab.append(rct_id(rct_id.g_dc_conv, 0xFED51BD2, 673, 'dc_conv.dc_conv_struct[1].enabled', rct_id.t_bool, 'Solar generator B connected')) 

    id_tab.append(rct_id(rct_id.g_nsm, 0xCBA34B9, 31, 'nsm.u_q_u[3]', rct_id.t_float, 'High voltage max. point', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x10842019, 44, 'nsm.cos_phi_p[3][1]', rct_id.t_float, 'Point 4 [cos(rct_db)]'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x1089ACA9, 45, 'nsm.u_q_u[0]', rct_id.t_float, 'Low voltage min. point', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x14FCA232, 55, 'nsm.rpm_lock_out_power', rct_id.t_float, 'Reactive Power Mode lock-out power', ' P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x26260419, 94, 'nsm.cos_phi_p[1][0]', rct_id.t_float, 'Point 2', ' P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x32CD0DB3, 121, 'nsm.cos_phi_p[0][1]', rct_id.t_float, 'Point 1', 'cos(Phi)')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x33F76B78, 125, 'nsm.p_u[0][1]', rct_id.t_float, 'Point 1 voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x3515F4A0, 131, 'nsm.p_u[3][1]', rct_id.t_float, 'Point 4 voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x360BDE8A, 132, 'nsm.startup_grad', rct_id.t_float, 'Startup gradient', ' P/(Pn*s)'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x4397D078, 172, 'nsm.cos_phi_p[1][1]', rct_id.t_float, 'Point 2', 'cos(Phi)')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x43CD0B6F, 173, 'nsm.pf_delay', rct_id.t_float, 'Delay time after P(f)', 's')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x4A61BAEE, 188, 'nsm.p_u[3][0]', rct_id.t_float, 'Point 4 P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x4C2A7CDC, 194, 'nsm.cos_phi_p[2][1]', rct_id.t_float, 'Point 3', 'cos(Phi)')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x4C374958, 195, 'nsm.startup_grad_after_fault', rct_id.t_float, 'Startup gradient after fault', ' P/(Pn*s)'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x53EF7649, 216, 'nsm.p_u[0][0]', rct_id.t_float, 'Point 1 P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x71465EAF, 307, 'nsm.cos_phi_ts', rct_id.t_float, 'Time const for filter', 's')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x7232F7AF, 313, 'nsm.apm', rct_id.t_enum, 'Active power mode'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x7A5C91F8, 332, 'nsm.p_u[1][0]', rct_id.t_float, 'Point 2 P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x7AF779C1, 336, 'nsm.pu_mode', rct_id.t_bool, 'P(U) mode 0: Pn 1: Pload'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x81AF854E, 352, 'nsm.pu_use', rct_id.t_bool, 'P(U) active')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x83A5333A, 357, 'nsm.cos_phi_p[0][0]', rct_id.t_float, 'Point 1', ' P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x88DEBCFE, 370, 'nsm.q_u_max_u_high', rct_id.t_float, 'Qmax at upper voltage level', 'var'))
    id_tab.append(rct_id(rct_id.g_nsm, 0x93E6918D, 409, 'nsm.f_exit', rct_id.t_float, 'Exit frequency for P(f) mode', 'Hz')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0x9680077F, 415, 'nsm.cos_phi_p[2][0]', rct_id.t_float, 'Point 3', ' P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0xA33D0954, 439, 'nsm.q_u_hysteresis', rct_id.t_bool, 'Curve with hysteresis')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xA5044DCD, 442, 'nsm.p_u[2][0]', rct_id.t_float, 'Point 3 P/Pn')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xB76E2B4C, 489, 'nsm.cos_phi_const', rct_id.t_float, 'Cos phi constant value')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xB98C8194, 497, 'nsm.min_cos_phi', rct_id.t_float, 'Minimum allowed cos(phi) [0..1]')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xBB617E51, 502, 'nsm.u_q_u[1]', rct_id.t_float, 'Low voltage max. point', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xC3352B17, 524, 'nsm.rpm', rct_id.t_enum, 'Reactive power mode')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xC46E9CA4, 530, 'nsm.u_lock_out', rct_id.t_float, 'Cos phi(P) lock out voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xCB9E1E6C, 547, 'nsm.Q_const', rct_id.t_float, 'Q constant value', 'var'))
    id_tab.append(rct_id(rct_id.g_nsm, 0xCCB51399, 550, 'nsm.q_u_max_u_low', rct_id.t_float, 'Qmax at lower voltage level', 'var'))
    id_tab.append(rct_id(rct_id.g_nsm, 0xD580567B, 566, 'nsm.u_lock_in', rct_id.t_float, 'Cos phi(P) lock in voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xD884AF95, 568, 'nsm.pf_desc_grad', rct_id.t_float, 'Power decrease gradient for P(f) mode', ' P/(Pn*s)'))
    id_tab.append(rct_id(rct_id.g_nsm, 0xE271C6D2, 595, 'nsm.u_q_u[2]', rct_id.t_float, 'High voltage min. point', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xE49BE3ED, 599, 'nsm.pf_rise_grad', rct_id.t_float, 'Power increase gradient after P(f) restriction', ' P/(Pn*s)'))
    id_tab.append(rct_id(rct_id.g_nsm, 0xE6F1CB83, 606, 'nsm.pu_ts', rct_id.t_float, 'Time const for filter', 's')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xEB7773BF, 613, 'nsm.p_u[1][1]', rct_id.t_float, 'Point 2 voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xEE049B1F, 617, 'nsm.pf_hysteresis', rct_id.t_bool, 'Hysteresis mode')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xF2405AC6, 632, 'nsm.p_limit', rct_id.t_float, 'Max. grid power', 'W')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xF25591AA, 634, 'nsm.cos_phi_p[3][0]', rct_id.t_float, 'Point 4', ' P/Pn'))
    id_tab.append(rct_id(rct_id.g_nsm, 0xF49F58F2, 643, 'nsm.p_u[2][1]', rct_id.t_float, 'Point 3 voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xF6A85818, 647, 'nsm.f_entry', rct_id.t_float, 'Entry frequency for P(f) mode', 'Hz')) 
    id_tab.append(rct_id(rct_id.g_nsm, 0xFCC39293, 666, 'nsm.rpm_lock_in_power', rct_id.t_float, 'Reactive Power Mode lock-in power', ' P/Pn'))

    id_tab.append(rct_id(rct_id.g_io_board, 0xDF45696, 37, 'io_board.io1_polarity', rct_id.t_bool, 'Inverted signal on input I/O 1')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xE799A56, 39, 'io_board.rse_table[0]', rct_id.t_float, 'K4..K1: 0000')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xFB40090, 43, 'io_board.check_rs485_result', rct_id.t_uint8, 'io_board.check_rs485_result')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x1B5445C4, 69, 'io_board.check_rse_result', rct_id.t_uint16, 'io_board.check_rse_result')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x29CA60F8, 107, 'io_board.rse_table[10]', rct_id.t_float, 'K4..K1: 1010')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x2E0C6220, 114, 'io_board.home_relay_sw_off_delay', rct_id.t_float, 'Switching off delay', 's')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x3C705F61, 154, 'io_board.rse_table[8]', rct_id.t_float, 'K4..K1: 1000'))
    id_tab.append(rct_id(rct_id.g_io_board, 0x3DBCC6B4, 159, 'io_board.rse_table[6]', rct_id.t_float, 'K4..K1: 0110')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x4F330E08, 207, 'io_board.io2_usage', rct_id.t_enum, 'Digital I/O 2 usage')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x54DBC202, 221, 'io_board.rse_table[12]', rct_id.t_float, 'K4..K1: 1100')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x5867B3BE, 229, 'io_board.rse_table[2]', rct_id.t_float, 'K4..K1: 0010')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x58C1A946, 230, 'io_board.check_state', rct_id.t_uint8, 'io_board.check_state')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x5BD2DB45, 241, 'io_board.io1_s0_imp_per_kwh', rct_id.t_int16, 'Number of impulses per kWh for S0 signal on I/O 1v'))
    id_tab.append(rct_id(rct_id.g_io_board, 0x5EE03C45, 248, 'io_board.alarm_home_relay_mode', rct_id.t_enum, 'Multifunctional relay usage')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x664A1326, 269, 'io_board.rse_table[14]', rct_id.t_float, 'K4..K1: 1110')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x6830F6E4, 275, 'io_board.rse_table[9]', rct_id.t_float, 'K4..K1: 1001')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x68BA92E1, 276, 'io_board.io2_s0_imp_per_kwh', rct_id.t_int16, 'Number of impulses per kWh for S0 signal on I/O 2')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x6C2D00E4, 287, 'io_board.rse_table[1]', rct_id.t_float, 'K4..K1: 0001')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x7689BE6A, 321, 'io_board.home_relay_sw_on_delay', rct_id.t_float, 'Switching on delay', 's')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x792A7B79, 328, 'io_board.s0_direction', rct_id.t_enum, 'S0 inputs single or bidirectional')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x7C556C7A, 338, 'io_board.io2_polarity', rct_id.t_bool, 'Inverted signal on input I/O 2')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x8320B84C, 356, 'io_board.rse_data_delay', rct_id.t_float, 'Delay for new K4..K1 data', 's')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x872F380B, 362, 'io_board.load_set', rct_id.t_float, 'Dummy household load', 'W')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x88C9707B, 369, 'io_board.rse_table[15]', rct_id.t_float, 'K4..K1: 1111')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x88F36D45, 371, 'io_board.rse_data', rct_id.t_uint8, 'Actual K4..K1 data')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x90F123FA, 395, 'io_board.io1_usage', rct_id.t_enum, 'Digital I/O 1 usage')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x98ACC1B8, 421, 'io_board.rse_table[4]', rct_id.t_float, 'K4..K1: 0100')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0x9B92023F, 428, 'io_board.rse_table[7]', rct_id.t_float, 'K4..K1: 0111')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xA3393749, 438, 'io_board.check_start', rct_id.t_uint8, 'io_board.check_start')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xAACE057A, 463, 'io_board.io1_s0_min_duration', rct_id.t_float, 'Minimum S0 signal duration on I/O 1', 's')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xAC2E2A56, 464, 'io_board.rse_table[5]', rct_id.t_float, 'K4..K1: 0101')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xB851FA70, 496, 'io_board.rse_table[11]', rct_id.t_float, 'K4..K1: 1011')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xBCC6F92F, 504, 'io_board.home_relay_threshold', rct_id.t_float, 'Switching on threshold', 'W')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xBDFE5547, 511, 'io_board.rse_table[3]', rct_id.t_float, 'K4..K1: 0011')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xC7605E16, 538, 'io_board.s0_sum', rct_id.t_float, 'io_board.s0_sum')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xCB1B3B10, 546, 'io_board.io2_s0_min_duration', rct_id.t_float, 'Minimum S0 signal duration on I/O 2', 's')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xD45913EC, 562, 'io_board.rse_table[13]', rct_id.t_float, 'K4..K1: 1101')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xE52B89FA, 601, 'io_board.home_relay_off_threshold', rct_id.t_float, 'Switching off threshold', 'W')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xE96F1844, 609, 'io_board.s0_external_power', rct_id.t_float, 'io_board.s0_external_power')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xF42D4DD0, 641, 'io_board.alarm_home_value', rct_id.t_enum, 'Evaluated value')) 
    id_tab.append(rct_id(rct_id.g_io_board, 0xFA7DB323, 655, 'io_board.check_s0_result', rct_id.t_uint16, 'io_board.check_s0_result')) 

    id_tab.append(rct_id(rct_id.g_flash_rtc, 0xE0505B4, 38, 'flash_rtc.time_stamp_set', rct_id.t_uint32, 'Set date/time')) 
    id_tab.append(rct_id(rct_id.g_flash_rtc, 0x2266DCB8, 84, 'flash_rtc.rtc_mcc_quartz_max_diff', rct_id.t_float, 'Maximum allowed quartz frequency difference between RTC and Microcontroller', 'ppm'))
    id_tab.append(rct_id(rct_id.g_flash_rtc, 0x3903A5E9, 140, 'flash_rtc.flag_time_auto_switch', rct_id.t_bool, 'Automatically adjust clock for daylight saving time')) 
    id_tab.append(rct_id(rct_id.g_flash_rtc, 0x4E0C56F2, 199, 'flash_rtc.rtc_mcc_quartz_ppm_difference', rct_id.t_float, 'Quartz frequency difference between RTC and Microcontroller', 'ppm'))
    id_tab.append(rct_id(rct_id.g_flash_rtc, 0x7301A5A7, 316, 'flash_rtc.time_stamp_factory', rct_id.t_uint32, 'Production date')) 
    id_tab.append(rct_id(rct_id.g_flash_rtc, 0xD166D94D, 556, 'flash_rtc.time_stamp', rct_id.t_uint32, 'Actual date/time')) 
    id_tab.append(rct_id(rct_id.g_flash_rtc, 0xDD90A328, 582, 'flash_rtc.time_stamp_update', rct_id.t_uint32, 'Last update date')) 

    id_tab.append(rct_id(rct_id.g_power_mng, 0x1156DFD0, 48, 'power_mng.battery_power', rct_id.t_float, 'Battery discharge power', 'W')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x1D2994EA, 73, 'power_mng.soc_charge_power', rct_id.t_float, 'Maintenance charge power', 'W')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x315D1490, 119, 'power_mng.bat_empty_full', rct_id.t_uint8, 'Bit 0 - battery was empty, bit 1 - battery was full')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x36A9E9A6, 136, 'power_mng.use_grid_power_enable', rct_id.t_bool, 'Utilize external Inverter energy')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x59358EB2, 231, 'power_mng.maximum_charge_voltage', rct_id.t_float, 'Max. battery charge voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x5B10CE81, 238, 'power_mng.is_heiphoss', rct_id.t_uint8, 'HeiPhoss mode')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x682CDDA1, 274, 'power_mng.battery_type', rct_id.t_enum, 'Battery type')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x8EBF9574, 382, 'power_mng.soc_min_island', rct_id.t_float, 'Min SOC target (island)'))
    id_tab.append(rct_id(rct_id.g_power_mng, 0x93C0C2E2, 408, 'power_mng.bat_calib_reqularity', rct_id.t_uint32, 'Battery calibration interval', 'days')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x972B3029, 417, 'power_mng.stop_discharge_voltage_buffer', rct_id.t_float, 'Stop discharge voltage buffer', 'V')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x97997C93, 418, 'power_mng.soc_max', rct_id.t_float, 'Max SOC target')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x97E203F9, 419, 'power_mng.is_grid', rct_id.t_bool, 'power_mng.is_grid')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x97E3A6F2, 420, 'power_mng.u_acc_lp', rct_id.t_float, 'Battery voltage (inverter)', 'V')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x99EE89CB, 425, 'power_mng.power_lim_src_index', rct_id.t_enum, 'Power limit source')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0x9F52F968, 433, 'power_mng.feed_asymmetrical', rct_id.t_bool, 'Allow asymmetrical feed')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xA7FA5C5D, 455, 'power_mng.u_acc_mix_lp', rct_id.t_float, 'Battery voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xA95EE214, 459, 'power_mng.model.bat_power_change', rct_id.t_float, 'power_mng.model.bat_power_change')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xAEF76FA1, 466, 'power_mng.minimum_discharge_voltage', rct_id.t_float, 'Min. battery discharge voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xB6623608, 487, 'power_mng.bat_next_calib_date', rct_id.t_uint32, 'Next battery calibration')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xBD008E29, 505, 'power_mng.battery_power_extern', rct_id.t_float, 'power_mng.battery_power_extern')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xBD3A23C3, 506, 'power_mng.soc_charge', rct_id.t_float, 'SOC min maintenance charge')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xC7459513, 537, 'power_mng.force_inv_class', rct_id.t_enum, 'Change inverter class')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xCE266F0F, 551, 'power_mng.soc_min', rct_id.t_float, 'Min SOC target')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xD197CBE0, 557, 'power_mng.stop_charge_current', rct_id.t_float, 'Stop charge current', 'A')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xD1DFC969, 558, 'power_mng.soc_target_set', rct_id.t_float, 'Force SOC target')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xDC667958, 578, 'power_mng.state', rct_id.t_uint8, 'Battery state machine')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xE9BBF6E4, 610, 'power_mng.amp_hours_measured', rct_id.t_float, 'Measured battery capacity')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xF1342795, 629, 'power_mng.stop_discharge_current', rct_id.t_float, 'Stop discharge current', 'A')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xF168B748, 630, 'power_mng.soc_strategy', rct_id.t_enum, 'SOC target selection')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xF393B7B0, 639, 'power_mng.calib_charge_power', rct_id.t_float, 'Calibration charge power', 'W')) 
    id_tab.append(rct_id(rct_id.g_power_mng, 0xFBD94C1F, 660, 'power_mng.amp_hours', rct_id.t_float, 'Battery energy', 'Ah')) 

    id_tab.append(rct_id(rct_id.g_buf_v_control, 0x4BC0F974, 190, 'buf_v_control.power_reduction_max_solar', rct_id.t_float, 'Solar plant peak power', 'Wp'))
    id_tab.append(rct_id(rct_id.g_buf_v_control, 0xF473BC5E, 642, 'buf_v_control.power_reduction_max_solar_grid', rct_id.t_float, 'Max. allowed grid feed-in power', 'W')) 
    id_tab.append(rct_id(rct_id.g_buf_v_control, 0xFE1AA500, 671, 'buf_v_control.power_reduction', rct_id.t_float, 'External power reduction based on solar plant peak power [0;1]'))

    id_tab.append(rct_id(rct_id.g_db, 0x16AF2A92, 58, 'db.power_board.Current_Mean', rct_id.t_float, 'db.power_board.Current_Mean'))
    id_tab.append(rct_id(rct_id.g_db, 0x17E3AF97, 61, 'db.power_board.adc_p9V_meas', rct_id.t_float, 'db.power_board.adc_p9V_meas'))
    id_tab.append(rct_id(rct_id.g_db, 0x1F9CBBF2, 77, 'db.power_board.Calibr_Value_Mean', rct_id.t_float, 'db.power_board.Calibr_Value_Mean'))
    id_tab.append(rct_id(rct_id.g_db, 0x2ED89924, 115, 'db.power_board.afi_t300', rct_id.t_float, 'AFI 300 mA switching off time', 's')) 
    id_tab.append(rct_id(rct_id.g_db, 0x383A3614, 139, 'db.power_board.afi_i60', rct_id.t_float, 'AFI 60 mA threshold', 'A')) 
    id_tab.append(rct_id(rct_id.g_db, 0x3EFEB931, 162, 'db.power_board.relays_state', rct_id.t_uint16, 'db.power_board.relays_state'))
    id_tab.append(rct_id(rct_id.g_db, 0x43FF47C3, 175, 'db.power_board.afi_t60', rct_id.t_float, 'AFI 60 mA switching off time', 's')) 
    id_tab.append(rct_id(rct_id.g_db, 0x4F735D10, 208, 'db.temp2', rct_id.t_float, 'Heat sink (battery actuator) temperature', 'Grad C')) 
    id_tab.append(rct_id(rct_id.g_db, 0x5CD75669, 242, 'db.power_board.afi_t150', rct_id.t_float, 'AFI 150 mA switching off time', 's')) 
    id_tab.append(rct_id(rct_id.g_db, 0x6279F2A3, 256, 'db.power_board.version_boot', rct_id.t_uint32, 'PIC bootloader software version')) 
    id_tab.append(rct_id(rct_id.g_db, 0x6BA10831, 283, 'db.power_board.afi_i30', rct_id.t_float, 'AFI 30 mA threshold', 'A')) 
    id_tab.append(rct_id(rct_id.g_db, 0x6FB2E2BF, 298, 'db.power_board.afi_i150', rct_id.t_float, 'AFI 150 mA threshold', 'A')) 
    id_tab.append(rct_id(rct_id.g_db, 0x742966A6, 318, 'db.power_board.afi_i300', rct_id.t_float, 'AFI 300 mA threshold', 'A')) 
    id_tab.append(rct_id(rct_id.g_db, 0x7DA7D8B6, 340, 'db.power_board.version_main', rct_id.t_uint32, 'PIC software version')) 
    id_tab.append(rct_id(rct_id.g_db, 0x80835476, 348, 'db.power_board.adc_p5V_W_meas', rct_id.t_float, 'db.power_board.adc_p5V_W_meas')) 
    id_tab.append(rct_id(rct_id.g_db, 0x9981F1AC, 424, 'db.power_board.adc_m9V_meas', rct_id.t_float, 'db.power_board.adc_m9V_meas')) 
    id_tab.append(rct_id(rct_id.g_db, 0xB0307591, 469, 'db.power_board.status', rct_id.t_uint16, 'Power board status')) 
    id_tab.append(rct_id(rct_id.g_db, 0xB69171C4, 488, 'db.power_board.Current_AC_RMS', rct_id.t_float, 'db.power_board.Current_AC_RMS')) 
    id_tab.append(rct_id(rct_id.g_db, 0xC0B7C4D2, 517, 'db.power_board.afi_t30', rct_id.t_float, 'AFI 30 mA switching off time', 's')) 
    id_tab.append(rct_id(rct_id.g_db, 0xC24E85D0, 523, 'db.core_temp', rct_id.t_float, 'Core temperature', 'Grad C')) 
    id_tab.append(rct_id(rct_id.g_db, 0xDFB53AF3, 590, 'db.power_board.Current_Mean_Mean_AC', rct_id.t_float, 'db.power_board.Current_Mean_Mean_AC')) 
    id_tab.append(rct_id(rct_id.g_db, 0xF0527539, 624, 'db.power_board.adc_p3V3_meas', rct_id.t_float, 'db.power_board.adc_p3V3_meas')) 
    id_tab.append(rct_id(rct_id.g_db, 0xF79D41D9, 649, 'db.temp1', rct_id.t_float, 'Heat sink temperature', 'Grad C')) 

    id_tab.append(rct_id(rct_id.g_switch_on_board, 0x1FEB2F67, 78, 'switch_on_cond.u_min', rct_id.t_float, 'Min. voltage'))
    id_tab.append(rct_id(rct_id.g_switch_on_board, 0x234DD4DF, 86, 'switch_on_cond.f_min', rct_id.t_float, 'Min. frequency'))
    id_tab.append(rct_id(rct_id.g_switch_on_board, 0x3390CC2F, 124, 'switch_on_cond.test_time_fault', rct_id.t_float, 'Switching on time after any grid fault', 's'))
    id_tab.append(rct_id(rct_id.g_switch_on_board, 0x4DB1B91E, 198, 'switch_on_cond.f_max', rct_id.t_float, 'Max. frequency'))
    id_tab.append(rct_id(rct_id.g_switch_on_board, 0x934E64E9, 407, 'switch_on_cond.u_max', rct_id.t_float, 'Max. voltage'))
    id_tab.append(rct_id(rct_id.g_switch_on_board, 0xECABB6CF, 616, 'switch_on_cond.test_time', rct_id.t_float, 'Test time'))

    id_tab.append(rct_id(rct_id.g_p_rec, 0xAA372CE, 25, 'p_rec_req[1]', rct_id.t_float, 'Required battery to grid power', 'W')) 
    id_tab.append(rct_id(rct_id.g_p_rec, 0x1ABA3EE8, 66, 'p_rec_req[0]', rct_id.t_float, 'Required compensation power', 'W')) 
    id_tab.append(rct_id(rct_id.g_p_rec, 0x365D12DA, 135, 'p_rec_req[2]', rct_id.t_float, 'Required Pac', 'W'))
    id_tab.append(rct_id(rct_id.g_p_rec, 0x54829753, 219, 'p_rec_lim[1]', rct_id.t_float, 'Max. battery to grid power', 'W')) 
    id_tab.append(rct_id(rct_id.g_p_rec, 0x5D0CDCF0, 243, 'p_rec_available[2]', rct_id.t_float, 'Available Pac', 'W'))
    id_tab.append(rct_id(rct_id.g_p_rec, 0x85886E2E, 359, 'p_rec_lim[0]', rct_id.t_float, 'Max. compensation power', 'W')) 
    id_tab.append(rct_id(rct_id.g_p_rec, 0x8F0FF9F3, 387, 'p_rec_available[1]', rct_id.t_float, 'Available battery to grid power', 'W'))
    id_tab.append(rct_id(rct_id.g_p_rec, 0x9A67600D, 427, 'p_rec_lim[2]', rct_id.t_float, 'Pac max.', 'W'))
    id_tab.append(rct_id(rct_id.g_p_rec, 0xB45FE275, 482, 'p_rec_available[0]', rct_id.t_float, 'Available compensation power', 'W'))

    id_tab.append(rct_id(rct_id.g_modbus, 0x31ED1B75, 120, 'modbus.mode', rct_id.t_enum, 'RS485 working mode'))
    id_tab.append(rct_id(rct_id.g_modbus, 0x6C243F71, 286, 'modbus.address', rct_id.t_uint8, 'RS485 address'))                                         

    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0x3B0C6A53, 150, 'bat_mng_struct.profile_pdc_max', rct_id.t_string, 'bat_mng_struct.profile_pdc_max'))
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0x9DC927AA, 430, 'bat_mng_struct.profile_load', rct_id.t_string, 'bat_mng_struct.profile_load'))
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0xB2FB9A90, 479, 'bat_mng_struct.k_trust', rct_id.t_float, 'How fast the actual prediction can be trusted [0..10]'))
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0xDE68F62D, 585, 'bat_mng_struct.profile_pext', rct_id.t_string, 'bat_mng_struct.profile_pext'))
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0xDF6EA121, 589, 'bat_mng_struct.profile_pdc', rct_id.t_string, 'bat_mng_struct.profile_pdc'))
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0xF0A03A20, 626, 'bat_mng_struct.k', rct_id.t_float, 'Forecast correction'))
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0xF644DCA7, 646, 'bat_mng_struct.k_reserve', rct_id.t_float, 'Main reservation coefficient [0..2]')) 
    id_tab.append(rct_id(rct_id.g_bat_mng_struct, 0xFB57BA65, 657, 'bat_mng_struct.count', rct_id.t_string, 'bat_mng_struct.count'))

    id_tab.append(rct_id(rct_id.g_iso_struct, 0x474F80D5, 182, 'iso_struct.Rn', rct_id.t_float, 'Insulation resistance on negative DC input', 'Ohm'))
    id_tab.append(rct_id(rct_id.g_iso_struct, 0x777DC0EB, 325, 'iso_struct.r_min', rct_id.t_float, 'Minimum allowed insulation resistance', 'Ohm')) 
    id_tab.append(rct_id(rct_id.g_iso_struct, 0x8E41FC47, 381, 'iso_struct.Rp', rct_id.t_float, 'Insulation resistance on positive DC input', 'Ohm')) 
    id_tab.append(rct_id(rct_id.g_iso_struct, 0xC717D1FB, 536, 'iso_struct.Riso', rct_id.t_float, 'Total insulation resistance', 'Ohm'))     

    id_tab.append(rct_id(rct_id.g_grid_lt, 0x3A3050E6, 143, 'grid_lt.threshold', rct_id.t_float, 'Max. voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_grid_lt, 0x9061EA7B, 392, 'grid_lt.granularity', rct_id.t_float, 'Resolution'))
    id_tab.append(rct_id(rct_id.g_grid_lt, 0xD9E721A5, 570, 'grid_lt.timeframe', rct_id.t_float, 'Timeframe'))

    id_tab.append(rct_id(rct_id.g_can_bus, 0x4539A6D4, 179, 'can_bus.bms_update_response[0]', rct_id.t_uint32, 'can_bus.bms_update_response[0]'))
    id_tab.append(rct_id(rct_id.g_can_bus, 0x69AA598A, 280, 'can_bus.requested_id', rct_id.t_int32, 'can_bus.requested_id'))
    id_tab.append(rct_id(rct_id.g_can_bus, 0x7A67E33B, 333, 'can_bus.bms_update_response[1]', rct_id.t_uint32, 'can_bus.bms_update_response[1]'))
    id_tab.append(rct_id(rct_id.g_can_bus, 0x96629BB9, 414, 'can_bus.bms_update_state', rct_id.t_uint8, 'can_bus.bms_update_state'))
    id_tab.append(rct_id(rct_id.g_can_bus, 0xBD4147B0, 507, 'can_bus.set_cell_resist', rct_id.t_uint32, 'can_bus.set_cell_resist'))
    id_tab.append(rct_id(rct_id.g_can_bus, 0xD143A391, 555, 'can_bus.set_cell_v_t', rct_id.t_uint32, 'can_bus.set_cell_v_t'))

    id_tab.append(rct_id(rct_id.g_display_struct, 0x67BF3003, 272, 'display_struct.display_dir', rct_id.t_bool, 'Rotate display'))
    id_tab.append(rct_id(rct_id.g_display_struct, 0x8EC4116E, 384, 'display_struct.blink', rct_id.t_bool, 'Display blinking enable'))
    id_tab.append(rct_id(rct_id.g_display_struct, 0xC1D051EC, 522, 'display_struct.variate_contrast', rct_id.t_uint8, 'display_struct.variate_contrast'))
    id_tab.append(rct_id(rct_id.g_display_struct, 0xF247BB16, 633, 'display_struct.contrast', rct_id.t_uint8, 'Display contrast'))

    id_tab.append(rct_id(rct_id.g_flash_param, 0x43F16F7E, 174, 'flash_state', rct_id.t_uint16, 'Flash state'))
    id_tab.append(rct_id(rct_id.g_flash_param, 0x65A44A98, 266, 'flash_mem', rct_id.t_string, 'flash_mem'))
    id_tab.append(rct_id(rct_id.g_flash_param, 0x46892579, 181, 'flash_param.write_cycles', rct_id.t_uint32, 'Write cycles of flash parameters'))
    id_tab.append(rct_id(rct_id.g_flash_param, 0x96E32D11, 416, 'flash_param.erase_cycles', rct_id.t_uint32, 'Erase cycles of flash parameter'))
    id_tab.append(rct_id(rct_id.g_flash_param, 0xB238942F, 477, 'last_successfull_flash_op', rct_id.t_int16, 'last_successfull_flash_op'))
    id_tab.append(rct_id(rct_id.g_flash_param, 0xE63A3529, 604, 'flash_result', rct_id.t_uint16, 'Flash result'))

    id_tab.append(rct_id(rct_id.g_fault, 0x234B4736, 85, 'fault[1].flt', rct_id.t_uint32, 'Error bit field 2'))
    id_tab.append(rct_id(rct_id.g_fault, 0x37F9D5CA, 137, 'fault[0].flt', rct_id.t_uint32, 'Error bit field 1'))
    id_tab.append(rct_id(rct_id.g_fault, 0x3B7FCD47, 152, 'fault[2].flt', rct_id.t_uint32, 'Error bit field 3'))
    id_tab.append(rct_id(rct_id.g_fault, 0x7F813D73, 345, 'fault[3].flt', rct_id.t_uint32, 'Error bit field 4'))

    id_tab.append(rct_id(rct_id.g_prim_sm, 0x3623D82A, 134, 'prim_sm.island_flag', rct_id.t_uint16, 'Grid-separated'))
    id_tab.append(rct_id(rct_id.g_prim_sm, 0x3AFEF139, 149, 'prim_sm.is_thin_layer', rct_id.t_bool, 'Thin-film solar module'))
    id_tab.append(rct_id(rct_id.g_prim_sm, 0x5F33284E, 249, 'prim_sm.state', rct_id.t_uint8, 'Inverter status'))
    id_tab.append(rct_id(rct_id.g_prim_sm, 0xC40D5688, 528, 'prim_sm.state_source', rct_id.t_uint32, 'prim_sm.state_source'))
    id_tab.append(rct_id(rct_id.g_prim_sm, 0xCF005C54, 552, 'prim_sm.phase_3_mode', rct_id.t_bool, 'prim_sm.phase_3_mode'))
    id_tab.append(rct_id(rct_id.g_prim_sm, 0xFB5DE9C5, 658, 'prim_sm.minigrid_flag', rct_id.t_bool, 'Minigrid support'))

    id_tab.append(rct_id(rct_id.g_cs_map, 0x6D5318C8, 290, 'cs_map[1]', rct_id.t_uint8, 'Associate current sensor 1 with phase L'))
    id_tab.append(rct_id(rct_id.g_cs_map, 0xD451EF88, 561, 'cs_map[2]', rct_id.t_uint8, 'Associate current sensor 2 with phase L'))
    id_tab.append(rct_id(rct_id.g_cs_map, 0xE0E16E63, 593, 'cs_map[0]', rct_id.t_uint8, 'Associate current sensor 0 with phase L'))

    id_tab.append(rct_id(rct_id.g_line_mon, 0x6BBDC7C8, 284, 'line_mon.u_max', rct_id.t_float, 'Max line voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_line_mon, 0x8D8E19F7, 378, 'line_mon.u_min', rct_id.t_float, 'Min line voltage', 'V')) 
    id_tab.append(rct_id(rct_id.g_line_mon, 0xA1266D6B, 435, 'line_mon.time_lim', rct_id.t_float, 'Switch off time line voltage', 's')) 

    id_tab.append(rct_id(rct_id.g_others, 0xCC4BDAA, 32, 'detect_phase_shift_enable', rct_id.t_bool, 'Enable active island detection'))
    id_tab.append(rct_id(rct_id.g_others, 0x108FC93D, 46, 'max_phase_shift', rct_id.t_float, 'Max. phase shift from 120 position', 'degrees'))
    id_tab.append(rct_id(rct_id.g_others, 0x19608C98, 64, 'partition[3].last_id', rct_id.t_int32, 'partition[3].last_id'))
    id_tab.append(rct_id(rct_id.g_others, 0x1C4A665F, 71, 'grid_pll[0].f', rct_id.t_float, 'Grid frequency', 'Hz'))
    id_tab.append(rct_id(rct_id.g_others, 0x2703A771, 98, 'cs_struct.is_tuned', rct_id.t_bool, 'Current sensors are tuned'))
    id_tab.append(rct_id(rct_id.g_others, 0x27EC8487, 104, 'performance_free[0]', rct_id.t_uint32, 'performance_free[0]'))
    id_tab.append(rct_id(rct_id.g_others, 0x2848A1EE, 105, 'grid_offset', rct_id.t_float, 'grid_offset'))
    id_tab.append(rct_id(rct_id.g_others, 0x3A0EA5BE, 142, 'power_spring_up', rct_id.t_float, 'power_spring_up'))
    id_tab.append(rct_id(rct_id.g_others, 0x3E728842, 161, 'power_spring_bat', rct_id.t_float, 'power_spring_bat'))
    id_tab.append(rct_id(rct_id.g_others, 0x494FE156, 186, 'power_spring_offset', rct_id.t_float, 'power_spring_offset'))
    id_tab.append(rct_id(rct_id.g_others, 0x4E3CB7F8, 201, 'phase_3_mode', rct_id.t_bool, '3-phase feed in'))
    id_tab.append(rct_id(rct_id.g_others, 0x68BC034D, 277, 'parameter_file', rct_id.t_string))
    id_tab.append(rct_id(rct_id.g_others, 0x6C44F721, 288, 'i_dc_max', rct_id.t_float, 'Max. DC-component of Iac', 'A'))
    id_tab.append(rct_id(rct_id.g_others, 0x7924ABD9, 327, 'inverter_sn', rct_id.t_string, 'Serial number'))
    id_tab.append(rct_id(rct_id.g_others, 0x7940547B, 329, 'inv_struct.force_dh', rct_id.t_bool, 'inv_struct.force_dh'))
    id_tab.append(rct_id(rct_id.g_others, 0x7946D888, 330, 'i_dc_slow_time', rct_id.t_float, 'Time for slow DC-component of Iac', 's'))
    id_tab.append(rct_id(rct_id.g_others, 0x87E4387A, 363, 'current_sensor_max', rct_id.t_float, 'Power Sensor current range', 'A'))
    id_tab.append(rct_id(rct_id.g_others, 0x8FC89B10, 388, 'com_service', rct_id.t_enum, 'COM service'))
    id_tab.append(rct_id(rct_id.g_others, 0x929394B7, 404, 'svnversion_last_known', rct_id.t_string, 'svnversion_last_known'))
    id_tab.append(rct_id(rct_id.g_others, 0xA12E9B43, 437, 'phase_marker', rct_id.t_int16, 'Next phase after phase 1'))
    id_tab.append(rct_id(rct_id.g_others, 0xA76AE9CA, 452, 'relays.bits_real', rct_id.t_uint16, 'relays.bits_real'))
    id_tab.append(rct_id(rct_id.g_others, 0xA9CF517D, 460, 'power_spring_down', rct_id.t_float, 'power_spring_down'))
    id_tab.append(rct_id(rct_id.g_others, 0xB1D1BE71, 473, 'osci_struct.cmd_response_time', rct_id.t_float, 'osci_struct.cmd_response_time'))
    id_tab.append(rct_id(rct_id.g_others, 0xBF9B6042, 512, 'svnversion_factory', rct_id.t_string, 'Control software factory version'))
    id_tab.append(rct_id(rct_id.g_others, 0xC36675D4, 525, 'i_ac_max_set', rct_id.t_float, 'Maximum AC throttle current', 'A'))
    id_tab.append(rct_id(rct_id.g_others, 0xC3A3F070, 526, 'i_ac_extern_connected', rct_id.t_bool, 'Current sensors detected'))
    id_tab.append(rct_id(rct_id.g_others, 0xDABD323E, 573, 'osci_struct.error', rct_id.t_int16, 'Communication error'))
    id_tab.append(rct_id(rct_id.g_others, 0xDDD1C2D0, 583, 'svnversion', rct_id.t_string, 'Control software version'))
    id_tab.append(rct_id(rct_id.g_others, 0xE14B8679, 594, 'i_dc_slow_max', rct_id.t_float, 'Max. slow DC-component of Iac', 'A'))
    id_tab.append(rct_id(rct_id.g_others, 0xE6AC95E5, 605, 'phase_shift_threshold', rct_id.t_uint32, 'Detection threshold'))
    id_tab.append(rct_id(rct_id.g_others, 0xEBC62737, 614, 'android_description', rct_id.t_string, 'Device name', '', 'RCT'))
    id_tab.append(rct_id(rct_id.g_others, 0xF2BE0C9C, 638, 'p_buf_available', rct_id.t_float, 'Available buffer power', 'W'))