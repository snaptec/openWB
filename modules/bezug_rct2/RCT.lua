-- Wireshark dissector to visualize the RCT Power Protocol
-- Developed by Peter Oberhofer based on RCT Power Protocol specification v.1.13
-- 
-- Note: script can't properly decode packets which are fragmented over consecutive TCP/IP frames
--  
RCT_protocol = Proto("RCT",  "RCT Protocol")

start_token = 0x2B
escape_token = 0x2D

-- commands
cmd_read = 0x01
cmd_write = 0x02
cmd_long_write = 0x03
cmd_response = 0x05
cmd_long_response = 0x06
cmd_reserved = 0x7
cmd_read_periodically = 0x8
cmd_no_len = 0x2D    -- not in spec but seen in wireshark trace
cmd_extension = 0x3C

t_bool = 0
t_uint8 = 1
t_int8 = 2
t_uint16 = 3
t_int16 = 4
t_uint32 = 5
t_int32 = 6
t_string = 7
t_enum = 8
t_float = 9
t_float = 10
t_log_ts = 11

HEADER_WITH_LENGTH = 1 + 1 + 2      -- frame length for header, command and 2 byte length
FRAME_TYPE_STANDARD = 4             -- standard frame with id
FRAME_TYPE_PLANT = 8                -- plant frame with id and address
FRAME_CRC16_LENGTH = 2              -- nr of bytes for CRC16 field

command_id     = ProtoField.string("RCT.command_id",    "command",       base.ASCII)
message_length = ProtoField.int32("RCT.message_length", "messageLength", base.DEC)
message_name   = ProtoField.string("RCT.name",          "name",          base.ASCII)
data_field     = ProtoField.string("RCT.data",          "data",          base.ASCII)
local subtree

RCT_protocol.fields = { message_length, request_id, response_to, cmd }

function RCT_protocol.dissector(buffer, pinfo, tree)
    local length = buffer:len()
    if length == 0 then 
        return 
    end

    consume(tree, pinfo, data, buffer)
end

function consume(tree, pinfo, data, buffer)
    local bEscapeMode = false
    local msg = ""
    local msg_len = 0
    local line = buffer:bytes():tohex()
    local previous_byte, Missing, payload, entry, crc, crc_expected
    local by, cval, skip, dropped, cmd, idx, PayloadLength, FrameLength, id

    subtree = tree:add(RCT_protocol, buffer(), "RCT Power Protocol Data")
    dropped = ""
    for offset=0, buffer:len()-1, 1 do
        by = string.sub(line, offset*2+1, offset*2+2)
        cval = tonumber(by,16)
        skip = false

        if msg_len == 0 then 
            if cval == start_token then
                msg = msg .. by
                msg_len = msg_len + 1
                by = ""
                if dropped:len() == 2 and previous_byte == "00" then
                    dropped = ""
                else
                    if dropped:len() > 0 then
                        subtree:add(data_field, dropped)
                        subtree:add(data_field, "!!!!! Data dropped (might be the fragment from the previous IP packet)")
                        dropped = ""
                    end
                end
            else
                previous_byte = by
            end
            skip = true
        end

        if skip == false then
            if bEscapeMode == true then
                bEscapeMode = false
            else
                if cval == escape_token then
                    bEscapeMode = true
                    skip = true
                    by = ""
                end
            end
        end

        if skip == false then
            -- add byte to message
            msg = msg .. by
            msg_len = msg_len + 1
            by = ""

            -- when minimum frame size is received, decode the length and check completness of frame
            if msg_len >= HEADER_WITH_LENGTH then
                if msg_len == HEADER_WITH_LENGTH then
                    idx = 3
                    cmd = tonumber(string.sub(msg, idx, idx+1), 16)                    
                    idx = idx + 2
                    if cmd == cmd_no_len then
                        PayloadLength = 8
                        FrameLength = PayloadLength + 1
                    elseif cmd == cmd_long_response or cmd == cmd_long_write then
                        PayloadLength = tonumber(string.sub(msg, idx, idx+3), 16)
                        idx = idx + 4
                        FrameLength = PayloadLength + 2
                    else
                        PayloadLength = tonumber(string.sub(msg, idx, idx+1), 16)
                        idx = idx + 2
                        FrameLength = PayloadLength + 1
                    end
                else
                    Missing = 2 + FrameLength + FRAME_CRC16_LENGTH - msg_len
                    if Missing == 0 then
                        id = tonumber(string.sub(msg, idx, idx+7), 16)
                        idx = idx + 8
                        if(PayloadLength > 4) then
                            payload = string.sub(msg, idx, -5)
                        else
                            payload = ""
                        end
                        pinfo.cols.protocol = "RCT Power"
                        entry = rct_find_entry(id)
                        crc_expected = string.sub(msg, msg:len()-3, msg:len())
                        crc = CRC16(string.sub(msg, 3, msg:len()-4))
                        subtree:add(data_field, msg)
                        if crc == crc_expected then
                            parse_payload(cmd, entry, payload)
                        else
                            subtree:add(data_field, string.format("!!!!! CRC error: %s != %s", crc, crc_expected))
                        end
                        msg_len = 0
                        msg = "" 
                    end
                end
            end
        else
            if by:len() > 0 then
                dropped = dropped .. by
            end
        end
    end

    if msg_len > 0 then
        subtree:add(data_field, msg)
        subtree:add(data_field, "!!!!! incomplete message. Next packet will show dropped data")
    end

    if dropped:len() > 0 then
        subtree:add(data_field, dropped)
        subtree:add(data_field, "!!!!! Data dropped (might be the fragment from the previous IP packet)")
end
end

function parse_payload(cmd, entry, payload)
    local cmd_name, name, value, txt

    if entry == nil then
        return
    end
    cmd_name = get_cmd_name(cmd)
    name = rct_entry_name(entry)
    if cmd == cmd_response or cmd == cmd_long_response then
        value = get_value(entry, payload)
        txt = string.format("> %-21s #%08X:%-50s %s", cmd_name, entry.msgid, name, value)
    else
        txt = string.format("> %-21s #%08X:%-50s %s", cmd_name, entry.msgid, name, entry.Desc)
    end
    subtree:add(data_field, txt)
end

function get_cmd_name(cmd)
    if cmd == cmd_read then return "read"
    elseif cmd == cmd_write then return  "write"
    elseif cmd == cmd_long_write then return  "write (long)"
    elseif cmd == cmd_response then return "response"
    elseif cmd == cmd_long_response then return "response (long)"
    elseif cmd == cmd_reserved then return "reserved"
    elseif cmd == cmd_read_periodically then return "read (periodically)"
    elseif cmd == cmd_extension then return "OP_GET_MORE"
    elseif cmd == cmd_no_len then return "response (no length)"
    else return "unknown"
    end
end

function CRC16(data)
    local crcsum = 0xFFFF
    local polynom = 0x1021  -- CCITT Polynom
    local by, cval

    -- align buffer: append a 0 if needed
    if bit.band(data:len()/2, 1) > 0 then
        data = data .. "00"
    end

    for offset=1, data:len(), 2 do
        by = string.sub(data, offset, offset+1)
        cval = tonumber(by,16)

        crcsum = bit.bxor(crcsum, bit.lshift(cval, 8))
        for j=1,8 do
            crcsum = bit.lshift(crcsum, 1)
            if bit.band(crcsum, 0x7FFF0000) > 0 then
                -- overflow in bit 16
                crcsum = bit.bxor(bit.band(crcsum,0x0000FFFF), polynom)
            end
        end
    end

    return string.format("%04X", crcsum)
end

function get_value(entry, payload)
    local n, s, v, value, len

    --print(payload, type(payload), entry.DataType)
    if payload:len() == 0 then
        value = ""
    elseif entry.DataType == t_bool then
        n = tonumber(string.sub(payload, 1, 2), 16)
        if n == 0 then value = "false" else velue = "true" end
    elseif entry.DataType == t_uint8 then
        value = tonumber(string.sub(payload, 1, 2), 16)
    elseif entry.DataType == t_int8 then
        value = tonumber(string.sub(payload, 1, 2), 16)
    elseif entry.DataType == t_uint16 then
        value = tonumber(string.sub(payload, 1, 4), 16)
    elseif entry.DataType == t_int16 then
        value = tonumber(string.sub(payload, 1, 4), 16)
    elseif entry.DataType == t_uint32 then
        value = tonumber(string.sub(payload, 1, 8), 16)
    elseif entry.DataType == t_int32 then
        value = tonumber(string.sub(payload, 1, 8), 16)
    elseif entry.DataType == t_enum then
        value = tonumber(string.sub(payload, 1, 2), 16)
    elseif entry.DataType == t_float then
        if(payload:len()>=8) then 
            n = tonumber(payload:sub(0,8), 16)
            s = Struct.pack("I4", n)
            v = Struct.unpack("f",s)
            value = string.format("%.3f", v)
        end
    elseif entry.DataType == t_string then
        value = payload:gsub('%x%x',function(c)return c.char(tonumber(c,16))end)
    elseif entry.DataType == t_time then
        n = tonumber(payload, 16)
        value = string.format("%08X: %s", n, os.date("%c", n))
    elseif entry.DataType == t_log_ts then
        if(payload:len()>=8) then 
            n = tonumber(payload:sub(0,8), 16)
            value = string.format("%s", os.date("%d.%m.%Y %H:%M:%S", n))
        end
    else
        value = payload
    end

    --print(value)
    return value
end

local tcp_port = DissectorTable.get("tcp.port")
tcp_port:add(8899, RCT_protocol)

local rct_id = 
{
    {msgid = 0x0104EB6A, idx =   0, Name = "rb485.f_grid[2]",                                  DataType = t_float,   Desc = "Grid phase 3 frequency [Hz]"},
    {msgid = 0x011F41DB, idx =   1, Name = "power_mng.schedule[0]",                            DataType = t_string,  Desc = "power_mng.schedule[0]"},
    {msgid = 0x016109E1, idx =   2, Name = "grid_mon[0].u_over.time",                          DataType = t_float,   Desc = "Max. voltage switch-off time level 1 [s]"},
    {msgid = 0x01676FA6, idx =   3, Name = "battery.cells_stat[3]",                            DataType = t_string,  Desc = "battery.cells_stat[3]"},
    {msgid = 0x019C0B60, idx =   4, Name = "cs_neg[2]",                                        DataType = t_float,   Desc = "Miltiply value of the current sensor 2 by"},
    {msgid = 0x02247588, idx =   5, Name = "battery_placeholder[0].cells_stat[2].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[2].u_min.value"},
    {msgid = 0x031A6110, idx =   6, Name = "energy.e_ext_month",                               DataType = t_float,   Desc = "External month energy [Wh]"},
    {msgid = 0x035E64EA, idx =   7, Name = "battery_placeholder[0].module_sn[5]",              DataType = t_string,  Desc = "Module 5 Serial Number"},
    {msgid = 0x039BDE11, idx =   8, Name = "hw_test.state",                                    DataType = t_uint8,   Desc = "hw_test.state"},
    {msgid = 0x03A39CA2, idx =   9, Name = "g_sync.p_ac_load[0]",                              DataType = t_float,   Desc = "Load household phase 1 [W]"},
    {msgid = 0x03D9C51F, idx =  10, Name = "battery.cells_stat[0].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[0].u_max.value"},
    {msgid = 0x040385DB, idx =  11, Name = "common_control_bits",                              DataType = t_uint32,  Desc = "Bit coded functions"},
    {msgid = 0x048C9D69, idx =  12, Name = "battery_placeholder[0].cells_stat[1].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[1].u_min.value"},
    {msgid = 0x04EAAA98, idx =  13, Name = "nsm.f_low_entry",                                  DataType = t_float,   Desc = "Entry frequency for P(f) under-frequency mode [Hz]"},
    {msgid = 0x0528D1D8, idx =  14, Name = "frt.u_min[2]",                                     DataType = t_float,   Desc = "Point 3 voltage [V]"},
    {msgid = 0x056162CA, idx =  15, Name = "battery.cells_stat[4].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[4].u_min.time"},
    {msgid = 0x056417DF, idx =  16, Name = "battery.cells_stat[3].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[3].t_max.index"},
    {msgid = 0x058F1759, idx =  17, Name = "hw_test.bt_power[6]",                              DataType = t_float,   Desc = "hw_test.bt_power[6]"},
    {msgid = 0x05C7CFB1, idx =  18, Name = "logger.day_egrid_load_log_ts",                     DataType = t_log_ts,  Desc = "logger.day_egrid_load_log_ts"},
    {msgid = 0x064A60FE, idx =  19, Name = "battery.cells_stat[4].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[4].t_max.index"},
    {msgid = 0x064E4340, idx =  20, Name = "logger.minutes_ubat_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_ubat_log_ts"},
    {msgid = 0x06A9FFA2, idx =  21, Name = "battery.charged_amp_hours",                        DataType = t_float,   Desc = "Total charge flow into battery [Ah]"},
    {msgid = 0x06E03755, idx =  22, Name = "wifi.ip",                                          DataType = t_string,  Desc = "IP Address"},
    {msgid = 0x071B5514, idx =  23, Name = "battery_placeholder[0].cells_stat[3].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[3].t_max.index"},
    {msgid = 0x07367B64, idx =  24, Name = "rb485.phase_marker",                               DataType = t_int16,   Desc = "Next phase after phase 1 in Power Switch"},
    {msgid = 0x073C7E5D, idx =  25, Name = "battery_placeholder[0].max_cell_temperature",      DataType = t_float,   Desc = "battery_placeholder[0].max_cell_temperature"},
    {msgid = 0x074B1EF5, idx =  26, Name = "battery_placeholder[0].cells_stat[3].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[3].u_max.index"},
    {msgid = 0x077692DE, idx =  27, Name = "battery.cells_stat[4].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[4].u_max.index"},
    {msgid = 0x07C61FAD, idx =  28, Name = "adc.u_ref_1_5v[0]",                                DataType = t_uint16,  Desc = "Reference voltage 1 [V]"},
    {msgid = 0x08679611, idx =  29, Name = "net.id",                                           DataType = t_uint32,  Desc = "net.id"},
    {msgid = 0x086C75B0, idx =  30, Name = "battery.stack_software_version[3]",                DataType = t_uint32,  Desc = "Software version stack 3"},
    {msgid = 0x0875C906, idx =  31, Name = "hw_test.bt_time[2]",                               DataType = t_float,   Desc = "hw_test.bt_time[2]"},
    {msgid = 0x08E81725, idx =  32, Name = "battery_placeholder[0].cells_stat[0].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[0].t_max.value"},
    {msgid = 0x095AFAA8, idx =  33, Name = "logger.minutes_ul3_log_ts",                        DataType = t_log_ts,  Desc = "logger.minutes_ul3_log_ts"},
    {msgid = 0x09923C1E, idx =  35, Name = "battery.cells_stat[3].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[3].t_min.index"},
    {msgid = 0x0A04CA7F, idx =  36, Name = "g_sync.u_zk_n_avg",                                DataType = t_float,   Desc = "Negative buffer capacitor voltage [V]"},
    {msgid = 0x0AA372CE, idx =  37, Name = "p_rec_req[1]",                                     DataType = t_float,   Desc = "Required battery to grid power [W]"},
    {msgid = 0x0AFDD6CF, idx =  38, Name = "acc_conv.i_acc_lp_fast",                           DataType = t_float,   Desc = "Battery current [A]"},
    {msgid = 0x0B94A673, idx =  39, Name = "battery_placeholder[0].cells_stat[6].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[6].t_min.time"},
    {msgid = 0x0BA16A10, idx =  40, Name = "wifi.sockb_protocol",                              DataType = t_enum,    Desc = "Network mode"},
    {msgid = 0x0C2A7286, idx =  41, Name = "battery_placeholder[0].cells_resist[0]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[0]"},
    {msgid = 0x0C3815C2, idx =  42, Name = "net.load_reduction",                               DataType = t_float,   Desc = "net.load_reduction"},
    {msgid = 0x0C588B75, idx =  43, Name = "energy.e_ext_day_sum",                             DataType = t_float,   Desc = "energy.e_ext_day_sum"},
    {msgid = 0x0CB5D21B, idx =  44, Name = "dc_conv.dc_conv_struct[1].p_dc_lp",                DataType = t_float,   Desc = "Solar generator B power [W]"},
    {msgid = 0x0CBA34B9, idx =  45, Name = "nsm.u_q_u[3]",                                     DataType = t_float,   Desc = "High voltage max. point [V]"},
    {msgid = 0x0CC4BDAA, idx =  46, Name = "detect_phase_shift_enable",                        DataType = t_bool,    Desc = "Enable active island detection"},
    {msgid = 0x0CFA8BC4, idx =  47, Name = "battery.stack_cycles[1]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[1]"},
    {msgid = 0x0D658831, idx =  48, Name = "i_bottom_max",                                     DataType = t_float,   Desc = "i_bottom_max"},
    {msgid = 0x0DACF21B, idx =  49, Name = "battery.cells_stat[4]",                            DataType = t_string,  Desc = "battery.cells_stat[4]"},
    {msgid = 0x0DBD5E77, idx =  50, Name = "battery_placeholder[0].cells_stat[6].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[6].u_min.index"},
    {msgid = 0x0DE3D20D, idx =  51, Name = "battery.status2",                                  DataType = t_int32,   Desc = "Battery extra status"},
    {msgid = 0x0DF164DE, idx =  52, Name = "logger.day_eb_log_ts",                             DataType = t_log_ts,  Desc = "logger.day_eb_log_ts"},
    {msgid = 0x0DF45696, idx =  53, Name = "io_board.io1_polarity",                            DataType = t_bool,    Desc = "Inverted signal on input I/O 1"},
    {msgid = 0x0E0505B4, idx =  54, Name = "flash_rtc.time_stamp_set",                         DataType = t_uint32,  Desc = "Set date/time"},
    {msgid = 0x0E4AA301, idx =  55, Name = "battery_placeholder[0].cells_stat[6].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[6].u_max.index"},
    {msgid = 0x0E799A56, idx =  56, Name = "io_board.rse_table[0]",                            DataType = t_float,   Desc = "K4..K1: 0000"},
    {msgid = 0x0EC64BA7, idx =  57, Name = "battery_placeholder[0].stack_software_version[3]", DataType = t_uint32,  Desc = "Software version stack 3"},
    {msgid = 0x0EF60C7E, idx =  58, Name = "battery.cells_stat[3].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[3].u_max.value"},
    {msgid = 0x0F28E2E1, idx =  59, Name = "energy.e_ext_total_sum",                           DataType = t_float,   Desc = "energy.e_ext_total_sum"},
    {msgid = 0x0FA29566, idx =  60, Name = "logger.minutes_ub_log_ts",                         DataType = t_log_ts,  Desc = "logger.minutes_ub_log_ts"},
    {msgid = 0x0FB40090, idx =  61, Name = "io_board.check_rs485_result",                      DataType = t_uint8,   Desc = "io_board.check_rs485_result"},
    {msgid = 0x1025B491, idx =  62, Name = "battery_placeholder[0].maximum_discharge_current", DataType = t_float,   Desc = "Max. discharge current [A]"},
    {msgid = 0x10842019, idx =  63, Name = "nsm.cos_phi_p[3][1]",                              DataType = t_float,   Desc = "Point 4 [cos(􀳦 )] (positive = overexcited)"},
    {msgid = 0x1089ACA9, idx =  64, Name = "nsm.u_q_u[0]",                                     DataType = t_float,   Desc = "Low voltage min. point [V]"},
    {msgid = 0x108FC93D, idx =  65, Name = "max_phase_shift",                                  DataType = t_float,   Desc = "Max. phase shift from 120° position [degrees]"},
    {msgid = 0x10970E9D, idx =  66, Name = "energy.e_ac_month",                                DataType = t_float,   Desc = "Month energy [Wh]"},
    {msgid = 0x1156DFD0, idx =  67, Name = "power_mng.battery_power",                          DataType = t_float,   Desc = "Battery discharge power [W]"},
    {msgid = 0x120EC3B4, idx =  68, Name = "battery.cells_stat[4].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[4].u_min.index"},
    {msgid = 0x126ABC86, idx =  69, Name = "energy.e_grid_load_month",                         DataType = t_float,   Desc = "Month energy grid load [Wh]"},
    {msgid = 0x132AA71E, idx =  70, Name = "logger.minutes_temp2_log_ts",                      DataType = t_log_ts,  Desc = "logger.minutes_temp2_log_ts"},
    {msgid = 0x1348AB07, idx =  71, Name = "battery.cells[4]",                                 DataType = t_string,  Desc = "battery.cells[4]"},
    {msgid = 0x147E8E26, idx =  72, Name = "g_sync.p_ac[1]",                                   DataType = t_float,   Desc = "AC2"},
    {msgid = 0x14C0E627, idx =  73, Name = "wifi.password",                                    DataType = t_string,  Desc = "WiFi password"},
    {msgid = 0x14FCA232, idx =  74, Name = "nsm.rpm_lock_out_power",                           DataType = t_float,   Desc = "Reactive Power Mode lock-out power [P/Pn]"},
    {msgid = 0x15AB1A61, idx =  75, Name = "power_mng.schedule[2]",                            DataType = t_string,  Desc = "power_mng.schedule[2]"},
    {msgid = 0x162491E8, idx =  76, Name = "battery.module_sn[5]",                             DataType = t_string,  Desc = "Module 5 Serial Number"},
    {msgid = 0x1639B2D8, idx =  77, Name = "battery_placeholder[0].cells_stat[4].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[4].u_max.index"},
    {msgid = 0x16A1F844, idx =  78, Name = "battery.bms_sn",                                   DataType = t_string,  Desc = "BMS Serial Number"},
    {msgid = 0x16AF2A92, idx =  79, Name = "db.power_board.Current_Mean",                      DataType = t_float,   Desc = "db.power_board.Current_Mean"},
    {msgid = 0x16B28CCA, idx =  80, Name = "adc.u_ref_1_5v[1]",                                DataType = t_uint16,  Desc = "Reference voltage 2 [V]"},
    {msgid = 0x16ED8F8F, idx =  81, Name = "partition[1].last_id",                             DataType = t_int32,   Desc = "partition[1].last_id"},
    {msgid = 0x173D81E4, idx =  82, Name = "rb485.version_boot",                               DataType = t_uint32,  Desc = "Power Switch bootloader version"},
    {msgid = 0x1781CD31, idx =  83, Name = "battery_placeholder[0].soh",                       DataType = t_float,   Desc = "SOH (State of Health)"},
    {msgid = 0x17E3AF97, idx =  84, Name = "db.power_board.adc_p9V_meas",                      DataType = t_float,   Desc = "db.power_board.adc_p9V_meas"},
    {msgid = 0x18469762, idx =  85, Name = "battery_placeholder[0].cells_stat[0].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[0].u_max.value"},
    {msgid = 0x18BD807D, idx =  86, Name = "battery_placeholder[0].cells_stat[4].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[4].t_min.index"},
    {msgid = 0x18D1E9E0, idx =  87, Name = "battery.cells_stat[5].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[5].u_max.index"},
    {msgid = 0x18F98B6D, idx =  88, Name = "battery.cells_stat[3].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[3].u_min.value"},
    {msgid = 0x19608C98, idx =  89, Name = "partition[3].last_id",                             DataType = t_int32,   Desc = "partition[3].last_id"},
    {msgid = 0x19B814F2, idx =  90, Name = "logger.year_egrid_feed_log_ts",                    DataType = t_log_ts,  Desc = "logger.year_egrid_feed_log_ts"},
    {msgid = 0x1ABA3EE8, idx =  91, Name = "p_rec_req[0]",                                     DataType = t_float,   Desc = "Required compensation power [W]"},
    {msgid = 0x1AC87AA0, idx =  92, Name = "g_sync.p_ac_load_sum_lp",                          DataType = t_float,   Desc = "Load household - external Power[W]"},
    {msgid = 0x1B39A3A3, idx =  93, Name = "battery.bms_power_version",                        DataType = t_uint32,  Desc = "Software version BMS Power"},
    {msgid = 0x1B5445C4, idx =  94, Name = "io_board.check_rse_result",                        DataType = t_uint16,  Desc = "io_board.check_rse_result"},
    {msgid = 0x1BFA5A33, idx =  95, Name = "energy.e_grid_load_total_sum",                     DataType = t_float,   Desc = "energy.e_grid_load_total_sum"},
    {msgid = 0x1C4A665F, idx =  96, Name = "grid_pll[0].f",                                    DataType = t_float,   Desc = "Grid frequency [Hz]"},
    {msgid = 0x1D0623D6, idx =  97, Name = "wifi.dns_address",                                 DataType = t_string,  Desc = "DNS address"},
    {msgid = 0x1D2994EA, idx =  98, Name = "power_mng.soc_charge_power",                       DataType = t_float,   Desc = "Maintenance charge power [W]"},
    {msgid = 0x1D49380A, idx =  99, Name = "logger.minutes_eb_log_ts",                         DataType = t_log_ts,  Desc = "logger.minutes_eb_log_ts"},
    {msgid = 0x1D83D2A5, idx = 100, Name = "battery_placeholder[0].cells[4]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[4]"},
    {msgid = 0x1E0EB397, idx = 101, Name = "battery_placeholder[0].cells_stat[6].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[6].u_max.value"},
    {msgid = 0x1E5FCA70, idx = 102, Name = "battery.maximum_charge_current",                   DataType = t_float,   Desc = "Max. charge current [A]"},
    {msgid = 0x1F44C23A, idx = 103, Name = "battery_placeholder[0].cells_stat[1].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[1].t_min.index"},
    {msgid = 0x1F73B6A4, idx = 104, Name = "battery.cells_stat[3].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[3].t_max.time"},
    {msgid = 0x1F9CBBF2, idx = 105, Name = "db.power_board.Calibr_Value_Mean",                 DataType = t_float,   Desc = "db.power_board.Calibr_Value_Mean"},
    {msgid = 0x1FA192E3, idx = 106, Name = "battery_placeholder[0].cells_resist[4]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[4]"},
    {msgid = 0x1FB3A602, idx = 107, Name = "battery_placeholder[0].cells_stat[2].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[2].t_max.value"},
    {msgid = 0x1FEB2F67, idx = 108, Name = "switch_on_cond.u_min",                             DataType = t_float,   Desc = "Min. voltage"},
    {msgid = 0x2082BFB6, idx = 109, Name = "hw_test.bt_time[9]",                               DataType = t_float,   Desc = "hw_test.bt_time[9]"},
    {msgid = 0x20A3A91F, idx = 110, Name = "battery_placeholder[0].module_sn[4]",              DataType = t_string,  Desc = "Module 4 Serial Number"},
    {msgid = 0x20FD4419, idx = 111, Name = "prim_sm.island_next_repeat_timeout",               DataType = t_float,   Desc = "Next island trial timeout [s]"},
    {msgid = 0x21879805, idx = 112, Name = "logger.minutes_eac1_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_eac1_log_ts"},
    {msgid = 0x21961B58, idx = 113, Name = "battery.current",                                  DataType = t_float,   Desc = "Battery current [A]"},
    {msgid = 0x21E1A802, idx = 114, Name = "energy.e_dc_month_sum[1]",                         DataType = t_float,   Desc = "energy.e_dc_month_sum[1]"},
    {msgid = 0x21EE7CBB, idx = 115, Name = "rb485.u_l_grid[2]",                                DataType = t_float,   Desc = "Grid phase 3 voltage [V]"},
    {msgid = 0x2266DCB8, idx = 116, Name = "flash_rtc.rtc_mcc_quartz_max_diff",                DataType = t_float,   Desc = "Maximum allowed quartz frequency difference between RTC and Microcontroller [ppm]"},
    {msgid = 0x226A23A4, idx = 117, Name = "dc_conv.dc_conv_struct[0].u_target",               DataType = t_float,   Desc = "MPP on input A [V]"},
    {msgid = 0x2295401F, idx = 118, Name = "battery_placeholder[0].cells_stat[3].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[3].u_max.time"},
    {msgid = 0x22CC80C6, idx = 119, Name = "frt.u_min_end",                                    DataType = t_float,   Desc = "FRT end undervoltage threshold [V]"},
    {msgid = 0x234B4736, idx = 120, Name = "fault[1].flt",                                     DataType = t_uint32,  Desc = "Error bit field 2"},
    {msgid = 0x234DD4DF, idx = 121, Name = "switch_on_cond.f_min",                             DataType = t_float,   Desc = "Min. frequency"},
    {msgid = 0x235E0DF5, idx = 122, Name = "battery_placeholder[0].stack_software_version[1]", DataType = t_uint32,  Desc = "Software version stack 1"},
    {msgid = 0x236D2178, idx = 123, Name = "frt.t_min[1]",                                     DataType = t_float,   Desc = "Point 2 time [s]"},
    {msgid = 0x23D4A386, idx = 124, Name = "battery_placeholder[0].cells_stat[0]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[0]"},
    {msgid = 0x23E55DA0, idx = 125, Name = "battery.cells_stat[5]",                            DataType = t_string,  Desc = "battery.cells_stat[5]"},
    {msgid = 0x23F525DE, idx = 126, Name = "net.command",                                      DataType = t_uint16,  Desc = "net.command"},
    {msgid = 0x24150B85, idx = 127, Name = "g_sync.u_zk_sum_mov_avg",                          DataType = t_float,   Desc = "Actual DC link voltage [V]"},
    {msgid = 0x241CFA0A, idx = 128, Name = "battery_placeholder[0].min_cell_temperature",      DataType = t_float,   Desc = "battery_placeholder[0].min_cell_temperature"},
    {msgid = 0x241F1F98, idx = 129, Name = "energy.e_dc_day_sum[1]",                           DataType = t_float,   Desc = "energy.e_dc_day_sum[1]"},
    {msgid = 0x24AC4CBB, idx = 130, Name = "battery_placeholder[0].cells_resist[6]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[6]"},
    {msgid = 0x2545E22D, idx = 131, Name = "g_sync.u_l_rms[2]",                                DataType = t_float,   Desc = "AC voltage phase 3 [V]"},
    {msgid = 0x257B5945, idx = 132, Name = "battery.cells_stat[2].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[2].u_min.index"},
    {msgid = 0x257B7612, idx = 133, Name = "battery.module_sn[3]",                             DataType = t_string,  Desc = "Module 3 Serial Number"},
    {msgid = 0x26260419, idx = 134, Name = "nsm.cos_phi_p[1][0]",                              DataType = t_float,   Desc = "Point 2 [P/Pn]"},
    {msgid = 0x26363AAE, idx = 135, Name = "battery.cells_stat[1].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[1].t_max.index"},
    {msgid = 0x265EACF6, idx = 136, Name = "battery.cells_stat[2].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[2].t_max.time"},
    {msgid = 0x26EFFC2F, idx = 137, Name = "energy.e_grid_feed_year",                          DataType = t_float,   Desc = "Year energy grid feed-in [Wh]"},
    {msgid = 0x2703A771, idx = 138, Name = "cs_struct.is_tuned",                               DataType = t_bool,    Desc = "Current sensors are tuned"},
    {msgid = 0x27116260, idx = 139, Name = "battery_placeholder[0].cells_stat[5].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[5].u_min.value"},
    {msgid = 0x27650FE2, idx = 140, Name = "rb485.version_main",                               DataType = t_uint32,  Desc = "Power Switch software version"},
    {msgid = 0x2788928C, idx = 141, Name = "g_sync.p_ac_load[1]",                              DataType = t_float,   Desc = "Load household phase 2 [W]"},
    {msgid = 0x27BE51D9, idx = 142, Name = "g_sync.p_ac_sc[0]",                                DataType = t_float,   Desc = "Grid power phase 1 [W]"},
    {msgid = 0x27C39CEA, idx = 143, Name = "battery.stack_cycles[6]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[6]"},
    {msgid = 0x27C828F4, idx = 144, Name = "energy.e_grid_feed_total_sum",                     DataType = t_float,   Desc = "energy.e_grid_feed_total_sum"},
    {msgid = 0x27EC8487, idx = 145, Name = "performance_free[0]",                              DataType = t_uint32,  Desc = "performance_free[0]"},
    {msgid = 0x2848A1EE, idx = 146, Name = "grid_offset",                                      DataType = t_float,   Desc = "grid_offset"},
    {msgid = 0x29BDA75F, idx = 147, Name = "display_struct.brightness",                        DataType = t_uint8,   Desc = "Display brightness"},
    {msgid = 0x29CA60F8, idx = 148, Name = "io_board.rse_table[10]",                           DataType = t_float,   Desc = "K4..K1: 1010"},
    {msgid = 0x2A30A97E, idx = 149, Name = "battery.stack_cycles[5]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[5]"},
    {msgid = 0x2A449E89, idx = 150, Name = "logger.year_log_ts",                               DataType = t_log_ts,  Desc = "logger.year_log_ts"},
    {msgid = 0x2AACCAA7, idx = 151, Name = "battery.max_cell_voltage",                         DataType = t_float,   Desc = "battery.max_cell_voltage"},
    {msgid = 0x2AE703F2, idx = 152, Name = "energy.e_dc_day[0]",                               DataType = t_float,   Desc = "Solar generator A day energy [Wh]"},
    {msgid = 0x2BC1E72B, idx = 153, Name = "battery.discharged_amp_hours",                     DataType = t_float,   Desc = "Total charge flow from battery [Ah]"},
    {msgid = 0x2E06172D, idx = 154, Name = "net.net_tunnel_id",                                DataType = t_uint32,  Desc = "net.net_tunnel_id"},
    {msgid = 0x2E0C6220, idx = 155, Name = "io_board.home_relay_sw_off_delay",                 DataType = t_float,   Desc = "Switching off delay [s]"},
    {msgid = 0x2E9F3C50, idx = 156, Name = "battery_placeholder[0].cells_stat[0].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[0].t_max.index"},
    {msgid = 0x2ED89924, idx = 157, Name = "db.power_board.afi_t300",                          DataType = t_float,   Desc = "AFI 300 mA switching off time [s]"},
    {msgid = 0x2ED8A639, idx = 158, Name = "battery_placeholder[0].cells_stat[2].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[2].u_min.time"},
    {msgid = 0x2F0A6B15, idx = 159, Name = "logger.month_ea_log_ts",                           DataType = t_log_ts,  Desc = "logger.month_ea_log_ts"},
    {msgid = 0x2F3C1D7D, idx = 160, Name = "energy.e_load_day",                                DataType = t_float,   Desc = "Household day energy [Wh]"},
    {msgid = 0x2F84A0A9, idx = 161, Name = "battery_placeholder[0].cells[2]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[2]"},
    {msgid = 0x3044195F, idx = 162, Name = "grid_mon[1].u_under.time",                         DataType = t_float,   Desc = "Min. voltage switch-off time level 2 [s]"},
    {msgid = 0x31413485, idx = 163, Name = "battery_placeholder[0].cells_stat[5].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[5].u_min.index"},
    {msgid = 0x314C13EB, idx = 164, Name = "battery_placeholder[0].cells_stat[5].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[5].u_max.value"},
    {msgid = 0x315D1490, idx = 165, Name = "power_mng.bat_empty_full",                         DataType = t_uint8,   Desc = "Bit 0 - battery was empty, bit 1 - battery was full"},
    {msgid = 0x31ED1B75, idx = 166, Name = "modbus.mode",                                      DataType = t_enum,    Desc = "RS485 working mode"},
    {msgid = 0x32CD0DB3, idx = 167, Name = "nsm.cos_phi_p[0][1]",                              DataType = t_float,   Desc = "Point 1 [cos(􀳦 )] (positive = overexcited)"},
    {msgid = 0x32DCA605, idx = 168, Name = "frt.u_max[0]",                                     DataType = t_float,   Desc = "Point 1 voltage [V]"},
    {msgid = 0x331D0689, idx = 169, Name = "battery.cells_stat[2].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[2].t_max.value"},
    {msgid = 0x336415EA, idx = 170, Name = "battery.cells_stat[0].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[0].t_max.time"},
    {msgid = 0x3390CC2F, idx = 171, Name = "switch_on_cond.test_time_fault",                   DataType = t_float,   Desc = "Switching on time after any grid fault [s]"},
    {msgid = 0x33F76B78, idx = 172, Name = "nsm.p_u[0][1]",                                    DataType = t_float,   Desc = "Point 1 voltage [V]"},
    {msgid = 0x34A164E7, idx = 173, Name = "battery.cells_stat[0]",                            DataType = t_string,  Desc = "battery.cells_stat[0]"},
    {msgid = 0x34E33726, idx = 174, Name = "battery.cells_stat[2].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[2].u_max.index"},
    {msgid = 0x34ECA9CA, idx = 175, Name = "logger.year_eb_log_ts",                            DataType = t_log_ts,  Desc = "logger.year_eb_log_ts"},
    {msgid = 0x3500F1E8, idx = 176, Name = "net.index",                                        DataType = t_int8,    Desc = "net.index"},
    {msgid = 0x3503B92D, idx = 177, Name = "battery.cells_stat[3].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[3].u_max.time"},
    {msgid = 0x3515F4A0, idx = 178, Name = "nsm.p_u[3][1]",                                    DataType = t_float,   Desc = "Point 4 voltage [V]"},
    {msgid = 0x360BDE8A, idx = 179, Name = "nsm.startup_grad",                                 DataType = t_float,   Desc = "Startup gradient [P/(Pn*s)]"},
    {msgid = 0x36214C57, idx = 180, Name = "net.prev_k",                                       DataType = t_float,   Desc = "net.prev_k"},
    {msgid = 0x362346D4, idx = 181, Name = "switch_on_cond.max_rnd_test_time_fault",           DataType = t_float,   Desc = "Max additional random switching on time after any grid fault [s]"},
    {msgid = 0x3623D82A, idx = 182, Name = "prim_sm.island_flag",                              DataType = t_uint16,  Desc = "Grid-separated"},
    {msgid = 0x365D12DA, idx = 183, Name = "p_rec_req[2]",                                     DataType = t_float,   Desc = "Required Pac [W]"},
    {msgid = 0x36A9E9A6, idx = 184, Name = "power_mng.use_grid_power_enable",                  DataType = t_bool,    Desc = "Utilize external Inverter energy"},
    {msgid = 0x374B5DD6, idx = 185, Name = "battery_placeholder[0].cells_stat[6].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[6].u_min.time"},
    {msgid = 0x37F9D5CA, idx = 186, Name = "fault[0].flt",                                     DataType = t_uint32,  Desc = "Error bit field 1"},
    {msgid = 0x381B8BF9, idx = 187, Name = "battery.soh",                                      DataType = t_float,   Desc = "SOH (State of Health)"},
    {msgid = 0x383A3614, idx = 188, Name = "db.power_board.afi_i60",                           DataType = t_float,   Desc = "AFI 60 mA threshold [A]"},
    {msgid = 0x38789061, idx = 189, Name = "nsm.f_low_rise_grad_storage",                      DataType = t_float,   Desc = "Power rise gradient for P(f) under-frequency mode with battery [1/Pn*Hz]"},
    {msgid = 0x3903A5E9, idx = 190, Name = "flash_rtc.flag_time_auto_switch",                  DataType = t_bool,    Desc = "Automatically adjust clock for daylight saving time"},
    {msgid = 0x3906A1D0, idx = 191, Name = "logger.minutes_eext_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_eext_log_ts"},
    {msgid = 0x392D1BEE, idx = 192, Name = "wifi.connect_to_server",                           DataType = t_uint8,   Desc = "wifi.connect_to_server"},
    {msgid = 0x39AD4639, idx = 193, Name = "battery_placeholder[0].cells_stat[5].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[5].u_min.time"},
    {msgid = 0x3A0EA5BE, idx = 194, Name = "power_spring_up",                                  DataType = t_float,   Desc = "power_spring_up"},
    {msgid = 0x3A3050E6, idx = 195, Name = "grid_lt.threshold",                                DataType = t_float,   Desc = "Max. voltage [V]"},
    {msgid = 0x3A35D491, idx = 196, Name = "battery_placeholder[0].cells_stat[2].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[2].u_max.value"},
    {msgid = 0x3A444FC6, idx = 197, Name = "g_sync.s_ac_lp[0]",                                DataType = t_float,   Desc = "Apparent power phase 1 [VA]"},
    {msgid = 0x3A7D5F53, idx = 198, Name = "battery.cells_stat[1].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[1].u_max.value"},
    {msgid = 0x3A873343, idx = 199, Name = "energy.e_ac_day_sum",                              DataType = t_float,   Desc = "energy.e_ac_day_sum"},
    {msgid = 0x3A9D2680, idx = 200, Name = "energy.e_ext_year_sum",                            DataType = t_float,   Desc = "energy.e_ext_year_sum"},
    {msgid = 0x3AA565FC, idx = 201, Name = "net.package",                                      DataType = t_string,  Desc = "net.package"},
    {msgid = 0x3AFEF139, idx = 202, Name = "prim_sm.is_thin_layer",                            DataType = t_bool,    Desc = "Thin-film solar module"},
    {msgid = 0x3B0C6A53, idx = 203, Name = "bat_mng_struct.profile_pdc_max",                   DataType = t_string,  Desc = "bat_mng_struct.profile_pdc_max"},
    {msgid = 0x3B5F6B9D, idx = 204, Name = "rb485.f_wr[0]",                                    DataType = t_float,   Desc = "Power Storage phase 1 frequency [Hz]"},
    {msgid = 0x3B7FCD47, idx = 205, Name = "fault[2].flt",                                     DataType = t_uint32,  Desc = "Error bit field 3"},
    {msgid = 0x3BA1B77B, idx = 206, Name = "battery.cells_stat[3].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[3].t_min.value"},
    {msgid = 0x3C24F3E8, idx = 207, Name = "inv_struct.cosinus_phi",                           DataType = t_float,   Desc = "cos 􀳦"},
    {msgid = 0x3C705F61, idx = 208, Name = "io_board.rse_table[8]",                            DataType = t_float,   Desc = "K4..K1: 1000"},
    {msgid = 0x3C87C4F5, idx = 209, Name = "energy.e_grid_feed_day",                           DataType = t_float,   Desc = "Day energy grid feed-in [Wh]"},
    {msgid = 0x3CA8E8D0, idx = 210, Name = "hw_test.bt_time[0]",                               DataType = t_float,   Desc = "hw_test.bt_time[0]"},
    {msgid = 0x3CB1EF01, idx = 211, Name = "grid_mon[0].u_under.threshold",                    DataType = t_float,   Desc = "Min. voltage level 1 [V]"},
    {msgid = 0x3D789979, idx = 212, Name = "hw_test.bt_power[7]",                              DataType = t_float,   Desc = "hw_test.bt_power[7]"},
    {msgid = 0x3DBCC6B4, idx = 213, Name = "io_board.rse_table[6]",                            DataType = t_float,   Desc = "K4..K1: 0110"},
    {msgid = 0x3E25C391, idx = 214, Name = "bat_mng_struct.bat_calib_soc_thresh",              DataType = t_float,   Desc = "Part of max historical SOC for battery calibration in advance"},
    {msgid = 0x3E722B43, idx = 215, Name = "grid_mon[1].f_under.threshold",                    DataType = t_float,   Desc = "Min. frequency level 2 [Hz]"},
    {msgid = 0x3E728842, idx = 216, Name = "power_spring_bat",                                 DataType = t_float,   Desc = "power_spring_bat"},
    {msgid = 0x3EFEB931, idx = 217, Name = "db.power_board.relays_state",                      DataType = t_uint16,  Desc = "db.power_board.relays_state"},
    {msgid = 0x3F98F58A, idx = 218, Name = "battery.cells_stat[5].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[5].t_max.index"},
    {msgid = 0x400F015B, idx = 219, Name = "g_sync.p_acc_lp",                                  DataType = t_float,   Desc = "Battery power [W]"},
    {msgid = 0x4077335D, idx = 220, Name = "g_sync.s_ac_lp[1]",                                DataType = t_float,   Desc = "Apparent power phase 2 [VA]"},
    {msgid = 0x40B07CA4, idx = 221, Name = "power_mng.schedule[6]",                            DataType = t_string,  Desc = "power_mng.schedule[6]"},
    {msgid = 0x40FF01B7, idx = 222, Name = "battery.cells[6]",                                 DataType = t_string,  Desc = "battery.cells[6]"},
    {msgid = 0x41744E11, idx = 223, Name = "frt.u_min[0]",                                     DataType = t_float,   Desc = "Point 1 voltage [V]"},
    {msgid = 0x41B11ECF, idx = 224, Name = "battery.cells_stat[3].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[3].u_min.index"},
    {msgid = 0x428CCF46, idx = 225, Name = "battery.cells_stat[5].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[5].u_min.value"},
    {msgid = 0x431509D1, idx = 226, Name = "logger.month_eload_log_ts",                        DataType = t_log_ts,  Desc = "logger.month_eload_log_ts"},
    {msgid = 0x43257820, idx = 227, Name = "g_sync.p_ac[0]",                                   DataType = t_float,   Desc = "AC1"},
    {msgid = 0x437B8122, idx = 228, Name = "rb485.available",                                  DataType = t_bool,    Desc = "Power Switch is available"},
    {msgid = 0x4397D078, idx = 229, Name = "nsm.cos_phi_p[1][1]",                              DataType = t_float,   Desc = "Point 2 [cos(􀳦 )] (positive = overexcited)"},
    {msgid = 0x43CD0B6F, idx = 230, Name = "nsm.pf_delay",                                     DataType = t_float,   Desc = "Delay time after P(f) [s]"},
    {msgid = 0x43F16F7E, idx = 231, Name = "flash_state",                                      DataType = t_uint16,  Desc = "Flash state"},
    {msgid = 0x43FF47C3, idx = 232, Name = "db.power_board.afi_t60",                           DataType = t_float,   Desc = "AFI 60 mA switching off time [s]"},
    {msgid = 0x442A3409, idx = 233, Name = "battery.cells_stat[4].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[4].t_min.time"},
    {msgid = 0x4443C661, idx = 234, Name = "battery.cells_stat[0].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[0].t_max.index"},
    {msgid = 0x44D4C533, idx = 235, Name = "energy.e_grid_feed_total",                         DataType = t_float,   Desc = "Total energy grid feed-in [Wh]"},
    {msgid = 0x4539A6D4, idx = 236, Name = "can_bus.bms_update_response[0]",                   DataType = t_uint32,  Desc = "can_bus.bms_update_response[0]"},
    {msgid = 0x465DDB50, idx = 237, Name = "battery_placeholder[0].cells_stat[2].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[2].t_min.value"},
    {msgid = 0x46635546, idx = 238, Name = "net.n_descendants",                                DataType = t_int8,    Desc = "Number of descendant slaves"},
    {msgid = 0x4686E044, idx = 239, Name = "battery_placeholder[0].cells_stat[1].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[1].u_min.index"},
    {msgid = 0x46892579, idx = 240, Name = "flash_param.write_cycles",                         DataType = t_uint32,  Desc = "Write cycles of flash parameters"},
    {msgid = 0x46C3625D, idx = 241, Name = "battery_placeholder[0].cells_stat[2]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[2]"},
    {msgid = 0x474F80D5, idx = 242, Name = "iso_struct.Rn",                                    DataType = t_float,   Desc = "Insulation resistance on negative DC input [Ohm]"},
    {msgid = 0x4764F9EE, idx = 243, Name = "battery_placeholder[0].cells_stat[3].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[3].t_max.value"},
    {msgid = 0x47A1DACA, idx = 244, Name = "power_mng.schedule[8]",                            DataType = t_string,  Desc = "power_mng.schedule[8]"},
    {msgid = 0x485AD749, idx = 245, Name = "g_sync.u_ptp_rms[1]",                              DataType = t_float,   Desc = "Phase to phase voltage 2 [V]"},
    {msgid = 0x488052BA, idx = 246, Name = "logger.minutes_ul2_log_ts",                        DataType = t_log_ts,  Desc = "logger.minutes_ul2_log_ts"},
    {msgid = 0x48D73FA5, idx = 247, Name = "g_sync.i_dr_lp[2]",                                DataType = t_float,   Desc = "Current phase 3 (average) [A]"},
    {msgid = 0x494FE156, idx = 248, Name = "power_spring_offset",                              DataType = t_float,   Desc = "power_spring_offset"},
    {msgid = 0x495BF0B6, idx = 249, Name = "energy.e_dc_year_sum[0]",                          DataType = t_float,   Desc = "energy.e_dc_year_sum[0]"},
    {msgid = 0x4992E65A, idx = 250, Name = "update_is_allowed_id",                             DataType = t_uint8,   Desc = "update_is_allowed_id"},
    {msgid = 0x4A61BAEE, idx = 251, Name = "nsm.p_u[3][0]",                                    DataType = t_float,   Desc = "Point 4 P/Pn"},
    {msgid = 0x4AAEB0D2, idx = 252, Name = "battery_placeholder[0].cells_stat[1]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[1]"},
    {msgid = 0x4AE96C12, idx = 253, Name = "dc_conv.dc_conv_struct[1].mpp.mpp_step",           DataType = t_float,   Desc = "MPP search step on input B [V]"},
    {msgid = 0x4B51A539, idx = 254, Name = "battery.prog_sn",                                  DataType = t_string,  Desc = "battery.prog_sn"},
    {msgid = 0x4BC0F974, idx = 255, Name = "buf_v_control.power_reduction_max_solar",          DataType = t_float,   Desc = "Solar plant peak power [Wp]"},
    {msgid = 0x4BE02BB7, idx = 256, Name = "energy.e_load_day_sum",                            DataType = t_float,   Desc = "energy.e_load_day_sum"},
    {msgid = 0x4C12C4C7, idx = 257, Name = "cs_neg[1]",                                        DataType = t_float,   Desc = "Miltiply value of the current sensor 1 by"},
    {msgid = 0x4C14CC7C, idx = 258, Name = "logger.year_ea_log_ts",                            DataType = t_log_ts,  Desc = "logger.year_ea_log_ts"},
    {msgid = 0x4C2A7CDC, idx = 259, Name = "nsm.cos_phi_p[2][1]",                              DataType = t_float,   Desc = "Point 3 [cos(􀳦 )] (positive = overexcited)"},
    {msgid = 0x4C374958, idx = 260, Name = "nsm.startup_grad_after_fault",                     DataType = t_float,   Desc = "Startup gradient after fault [P/(Pn*s)]"},
    {msgid = 0x4CB7C0DC, idx = 261, Name = "battery.min_cell_voltage",                         DataType = t_float,   Desc = "battery.min_cell_voltage"},
    {msgid = 0x4D684EF2, idx = 262, Name = "battery_placeholder[0].cells[0]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[0]"},
    {msgid = 0x4D985F33, idx = 263, Name = "battery.cells_stat[5].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[5].u_max.value"},
    {msgid = 0x4DB1B91E, idx = 264, Name = "switch_on_cond.f_max",                             DataType = t_float,   Desc = "Max. frequency"},
    {msgid = 0x4DC372A0, idx = 265, Name = "battery_placeholder[0].cells_stat[4].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[4].u_max.value"},
    {msgid = 0x4E04DD55, idx = 266, Name = "battery.soc_update_since",                         DataType = t_float,   Desc = "battery.soc_update_since"},
    {msgid = 0x4E0C56F2, idx = 267, Name = "flash_rtc.rtc_mcc_quartz_ppm_difference",          DataType = t_float,   Desc = "Quartz frequency difference between RTC and Microcontroller [ppm]"},
    {msgid = 0x4E2B42A4, idx = 268, Name = "hw_test.bt_power[0]",                              DataType = t_float,   Desc = "hw_test.bt_power[0]"},
    {msgid = 0x4E3CB7F8, idx = 269, Name = "phase_3_mode",                                     DataType = t_bool,    Desc = "3-phase feed in"},
    {msgid = 0x4E49AEC5, idx = 270, Name = "g_sync.p_ac_sum",                                  DataType = t_float,   Desc = "Real power [W]"},
    {msgid = 0x4E699086, idx = 271, Name = "battery.module_sn[4]",                             DataType = t_string,  Desc = "Module 4 Serial Number"},
    {msgid = 0x4E77B2CE, idx = 272, Name = "hw_test.bt_cycle",                                 DataType = t_uint8,   Desc = "hw_test.bt_cycle"},
    {msgid = 0x4E9D95A6, idx = 273, Name = "logger.year_eext_log_ts",                          DataType = t_log_ts,  Desc = "logger.year_eext_log_ts"},
    {msgid = 0x4EE8DB78, idx = 274, Name = "energy.e_load_year_sum",                           DataType = t_float,   Desc = "energy.e_load_year_sum"},
    {msgid = 0x4F330E08, idx = 275, Name = "io_board.io2_usage",                               DataType = t_enum,    Desc = "Digital I/O 2 usage"},
    {msgid = 0x4F735D10, idx = 276, Name = "db.temp2",                                         DataType = t_float,   Desc = "Heat sink (battery actuator) temperature [°C]"},
    {msgid = 0x4FC53F19, idx = 277, Name = "battery_placeholder[0].module_sn[3]",              DataType = t_string,  Desc = "Module 3 Serial Number"},
    {msgid = 0x4FEDC1BE, idx = 278, Name = "battery_placeholder[0].cells_stat[5].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[5].t_min.value"},
    {msgid = 0x4FF8CCE2, idx = 279, Name = "battery_placeholder[0].stack_software_version[5]", DataType = t_uint32,  Desc = "Software version stack 5"},
    {msgid = 0x501A162D, idx = 280, Name = "battery.cells_resist[5]",                          DataType = t_string,  Desc = "battery.cells_resist[5]"},
    {msgid = 0x50514732, idx = 281, Name = "battery.cells_stat[6].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[6].u_min.index"},
    {msgid = 0x508FCE78, idx = 282, Name = "adc.u_ref_1_5v[3]",                                DataType = t_uint16,  Desc = "Reference voltage 4 [V]"},
    {msgid = 0x50B441C1, idx = 283, Name = "logger.minutes_ea_log_ts",                         DataType = t_log_ts,  Desc = "logger.minutes_ea_log_ts"},
    {msgid = 0x5151D84C, idx = 284, Name = "prim_sm.island_reset_retrials_counter_time",       DataType = t_float,   Desc = "Reset island trials counter in [min] (by 0 not used)"},
    {msgid = 0x518C7BBE, idx = 285, Name = "battery.cells_stat[5].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[5].u_min.time"},
    {msgid = 0x51E5377D, idx = 286, Name = "battery_placeholder[0].stack_cycles[1]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[1]"},
    {msgid = 0x5293B668, idx = 287, Name = "logger.minutes_soc_log_ts",                        DataType = t_log_ts,  Desc = "logger.minutes_soc_log_ts"},
    {msgid = 0x53656F42, idx = 288, Name = "battery_placeholder[0].cells_stat[2].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[2].u_max.index"},
    {msgid = 0x537C719F, idx = 289, Name = "battery.cells_stat[0].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[0].t_max.value"},
    {msgid = 0x53886C09, idx = 290, Name = "wifi.connect_to_service",                          DataType = t_uint8,   Desc = "wifi.connect_to_service"},
    {msgid = 0x53EF7649, idx = 291, Name = "nsm.p_u[0][0]",                                    DataType = t_float,   Desc = "Point 1 P/Pn"},
    {msgid = 0x5411CE1B, idx = 292, Name = "logger.minutes_ul1_log_ts",                        DataType = t_log_ts,  Desc = "logger.minutes_ul1_log_ts"},
    {msgid = 0x5438B68E, idx = 293, Name = "grid_mon[1].u_over.threshold",                     DataType = t_float,   Desc = "Max. voltage level 2 [V]"},
    {msgid = 0x54829753, idx = 294, Name = "p_rec_lim[1]",                                     DataType = t_float,   Desc = "Max. battery to grid power [W]"},
    {msgid = 0x54B4684E, idx = 295, Name = "g_sync.u_l_rms[1]",                                DataType = t_float,   Desc = "AC voltage phase 2 [V]"},
    {msgid = 0x54DBC202, idx = 296, Name = "io_board.rse_table[12]",                           DataType = t_float,   Desc = "K4..K1: 1100"},
    {msgid = 0x554D8FEE, idx = 297, Name = "logger.minutes_eac2_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_eac2_log_ts"},
    {msgid = 0x5570401B, idx = 298, Name = "battery.stored_energy",                            DataType = t_float,   Desc = "Total energy flow into battery [Wh]"},
    {msgid = 0x55C22966, idx = 299, Name = "g_sync.s_ac[2]",                                   DataType = t_float,   Desc = "Apparent power phase 3 [VA]"},
    {msgid = 0x55DDF7BA, idx = 300, Name = "battery.max_cell_temperature",                     DataType = t_float,   Desc = "battery.max_cell_temperature"},
    {msgid = 0x5673D737, idx = 301, Name = "wifi.connect_to_wifi",                             DataType = t_bool,    Desc = "wifi.connect_to_wifi"},
    {msgid = 0x57429627, idx = 302, Name = "wifi.authentication_method",                       DataType = t_string,  Desc = "WiFi authentication method"},
    {msgid = 0x576D2A08, idx = 303, Name = "battery_placeholder[0].cells_stat[3].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[3].t_min.time"},
    {msgid = 0x57945EE4, idx = 304, Name = "battery_placeholder[0].maximum_charge_current",    DataType = t_float,   Desc = "Max. charge current [A]"},
    {msgid = 0x58378BD0, idx = 305, Name = "hw_test.bt_time[3]",                               DataType = t_float,   Desc = "hw_test.bt_time[3]"},
    {msgid = 0x5847E59E, idx = 306, Name = "battery.maximum_charge_voltage_constant_u",        DataType = t_float,   Desc = "Max. charge voltage [V]"},
    {msgid = 0x5867B3BE, idx = 307, Name = "io_board.rse_table[2]",                            DataType = t_float,   Desc = "K4..K1: 0010"},
    {msgid = 0x58C1A946, idx = 308, Name = "io_board.check_state",                             DataType = t_uint8,   Desc = "io_board.check_state"},
    {msgid = 0x592B13DF, idx = 309, Name = "power_mng.schedule[4]",                            DataType = t_string,  Desc = "power_mng.schedule[4]"},
    {msgid = 0x59358EB2, idx = 310, Name = "power_mng.maximum_charge_voltage",                 DataType = t_float,   Desc = "Max. battery charge voltage [V]"},
    {msgid = 0x5939EC5D, idx = 311, Name = "battery.module_sn[6]",                             DataType = t_string,  Desc = "Module 6 Serial Number"},
    {msgid = 0x5952E5E6, idx = 312, Name = "wifi.mask",                                        DataType = t_string,  Desc = "Netmask"},
    {msgid = 0x5A120CE4, idx = 313, Name = "battery.cells_stat[1].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[1].t_max.time"},
    {msgid = 0x5A316247, idx = 314, Name = "wifi.mode",                                        DataType = t_string,  Desc = "WiFi mode"},
    {msgid = 0x5A9EEFF0, idx = 315, Name = "battery.stack_cycles[4]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[4]"},
    {msgid = 0x5AF50FD7, idx = 316, Name = "battery.cells_stat[4].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[4].t_min.value"},
    {msgid = 0x5B10CE81, idx = 317, Name = "power_mng.is_heiphoss",                            DataType = t_uint8,   Desc = "HeiPhoss mode"},
    {msgid = 0x5BA122A5, idx = 318, Name = "battery.stack_cycles[2]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[2]"},
    {msgid = 0x5BB8075A, idx = 319, Name = "dc_conv.dc_conv_struct[1].u_sg_lp",                DataType = t_float,   Desc = "Solar generator B voltage [V]"},
    {msgid = 0x5BD2DB45, idx = 320, Name = "io_board.io1_s0_imp_per_kwh",                      DataType = t_int16,   Desc = "Number of impulses per kWh for S0 signal on I/O 1"},
    {msgid = 0x5C93093B, idx = 321, Name = "battery_placeholder[0].status2",                   DataType = t_int32,   Desc = "Battery extra status"},
    {msgid = 0x5CD75669, idx = 322, Name = "db.power_board.afi_t150",                          DataType = t_float,   Desc = "AFI 150 mA switching off time [s]"},
    {msgid = 0x5D0CDCF0, idx = 323, Name = "p_rec_available[2]",                               DataType = t_float,   Desc = "Available Pac [W]"},
    {msgid = 0x5D1B0835, idx = 324, Name = "net.use_network_filter",                           DataType = t_bool,    Desc = "net.use_network_filter"},
    {msgid = 0x5D34D09D, idx = 325, Name = "logger.month_egrid_load_log_ts",                   DataType = t_log_ts,  Desc = "logger.month_egrid_load_log_ts"},
    {msgid = 0x5E540FB2, idx = 326, Name = "net.update_slaves",                                DataType = t_bool,    Desc = "Activate aut. update slaves"},
    {msgid = 0x5E942C62, idx = 327, Name = "dc_conv.dc_conv_struct[1].mpp.fixed_voltage",      DataType = t_float,   Desc = "Fixed voltage Solar generator B [V]"},
    {msgid = 0x5EE03C45, idx = 328, Name = "io_board.alarm_home_relay_mode",                   DataType = t_enum,    Desc = "Multifunctional relay usage"},
    {msgid = 0x5EF54372, idx = 329, Name = "battery_placeholder[0].cells_stat[0].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[0].u_max.index"},
    {msgid = 0x5F33284E, idx = 330, Name = "prim_sm.state",                                    DataType = t_uint8,   Desc = "Inverter status"},
    {msgid = 0x6002891F, idx = 331, Name = "g_sync.p_ac_sc_sum",                               DataType = t_float,   Desc = "Grid power (ext. sensors) [W]"},
    {msgid = 0x60435F1C, idx = 332, Name = "battery_placeholder[0].cells[6]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[6]"},
    {msgid = 0x60749E5E, idx = 333, Name = "battery.cells_stat[6].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[6].u_min.time"},
    {msgid = 0x60A9A532, idx = 334, Name = "logger.day_eext_log_ts",                           DataType = t_log_ts,  Desc = "logger.day_eext_log_ts"},
    {msgid = 0x612F7EAB, idx = 335, Name = "g_sync.s_ac[1]",                                   DataType = t_float,   Desc = "Apparent power phase 2 [VA]"},
    {msgid = 0x61EAC702, idx = 336, Name = "battery.cells_stat[0].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[0].t_min.value"},
    {msgid = 0x6213589B, idx = 337, Name = "battery.cells_stat[6].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[6].u_min.value"},
    {msgid = 0x6279F2A3, idx = 338, Name = "db.power_board.version_boot",                      DataType = t_uint32,  Desc = "PIC bootloader software version"},
    {msgid = 0x62B8940B, idx = 339, Name = "dc_conv.start_voltage",                            DataType = t_float,   Desc = "Inverter DC-voltage start value [V]"},
    {msgid = 0x62D645D9, idx = 340, Name = "battery.cells[5]",                                 DataType = t_string,  Desc = "battery.cells[5]"},
    {msgid = 0x62FBE7DC, idx = 341, Name = "energy.e_grid_load_total",                         DataType = t_float,   Desc = "Total energy grid load [Wh]"},
    {msgid = 0x63476DBE, idx = 342, Name = "g_sync.u_ptp_rms[0]",                              DataType = t_float,   Desc = "Phase to phase voltage 1 [V]"},
    {msgid = 0x6383DEA9, idx = 343, Name = "battery_placeholder[0].cells_stat[1].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[1].t_max.value"},
    {msgid = 0x6388556C, idx = 344, Name = "battery.stack_software_version[0]",                DataType = t_uint32,  Desc = "Software version stack 0"},
    {msgid = 0x6445D856, idx = 345, Name = "battery.cells_stat[1].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[1].u_min.index"},
    {msgid = 0x6476A836, idx = 346, Name = "dc_conv.dc_conv_struct[0].mpp.enable_scan",        DataType = t_bool,    Desc = "Enable rescan for global MPP on solar generator A"},
    {msgid = 0x649B10DA, idx = 347, Name = "battery.cells_resist[0]",                          DataType = t_string,  Desc = "battery.cells_resist[0]"},
    {msgid = 0x650C1ED7, idx = 348, Name = "g_sync.i_dr_eff[1]",                               DataType = t_float,   Desc = "Current phase 2 [A]"},
    {msgid = 0x652B7536, idx = 349, Name = "battery_placeholder[0].cells_stat[3].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[3].t_min.index"},
    {msgid = 0x6599E3D3, idx = 350, Name = "power_mng.schedule[3]",                            DataType = t_string,  Desc = "power_mng.schedule[3]"},
    {msgid = 0x65A44A98, idx = 351, Name = "flash_mem",                                        DataType = t_string,  Desc = "flash_mem"},
    {msgid = 0x65B624AB, idx = 352, Name = "energy.e_grid_feed_month",                         DataType = t_float,   Desc = "Month energy grid feed-in [Wh]"},
    {msgid = 0x65EED11B, idx = 353, Name = "battery.voltage",                                  DataType = t_float,   Desc = "Battery voltage [V]"},
    {msgid = 0x663F1452, idx = 354, Name = "power_mng.n_batteries",                            DataType = t_uint8,   Desc = "power_mng.n_batteries"},
    {msgid = 0x664A1326, idx = 355, Name = "io_board.rse_table[14]",                           DataType = t_float,   Desc = "K4..K1: 1110"},
    {msgid = 0x669D02FE, idx = 356, Name = "logger.minutes_eac_log_ts",                        DataType = t_log_ts,  Desc = "logger.minutes_eac_log_ts"},
    {msgid = 0x6709A2F4, idx = 357, Name = "energy.e_ac_year_sum",                             DataType = t_float,   Desc = "energy.e_ac_year_sum"},
    {msgid = 0x672552DC, idx = 358, Name = "power_mng.bat_calib_days_in_advance",              DataType = t_uint8,   Desc = "Battery calibration days in advance"},
    {msgid = 0x6743CCCE, idx = 359, Name = "battery_placeholder[0].cells_stat[6].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[6].t_max.index"},
    {msgid = 0x675776B1, idx = 360, Name = "dc_conv.dc_conv_struct[1].u_target",               DataType = t_float,   Desc = "MPP on input B [V]"},
    {msgid = 0x67BF3003, idx = 361, Name = "display_struct.display_dir",                       DataType = t_bool,    Desc = "Rotate display"},
    {msgid = 0x67C0A2F5, idx = 362, Name = "net.slave_p_total",                                DataType = t_float,   Desc = "net.slave_p_total"},
    {msgid = 0x682CDDA1, idx = 363, Name = "power_mng.battery_type",                           DataType = t_enum,    Desc = "Battery type"},
    {msgid = 0x6830F6E4, idx = 364, Name = "io_board.rse_table[9]",                            DataType = t_float,   Desc = "K4..K1: 1001"},
    {msgid = 0x68BA92E1, idx = 365, Name = "io_board.io2_s0_imp_per_kwh",                      DataType = t_int16,   Desc = "Number of impulses per kWh for S0 signal on I/O 2"},
    {msgid = 0x68BC034D, idx = 366, Name = "parameter_file",                                   DataType = t_string,  Desc = "Norm"},
    {msgid = 0x68EEFD3D, idx = 367, Name = "energy.e_dc_total[1]",                             DataType = t_float,   Desc = "Solar generator B total energy [Wh]"},
    {msgid = 0x690C32D2, idx = 368, Name = "battery_placeholder[0].module_sn[0]",              DataType = t_string,  Desc = "Module 0 Serial Number"},
    {msgid = 0x6974798A, idx = 369, Name = "battery.stack_software_version[6]",                DataType = t_uint32,  Desc = "Software version stack 6"},
    {msgid = 0x69AA598A, idx = 370, Name = "can_bus.requested_id",                             DataType = t_int32,   Desc = "can_bus.requested_id"},
    {msgid = 0x69B8FF28, idx = 371, Name = "battery.cells[2]",                                 DataType = t_string,  Desc = "battery.cells[2]"},
    {msgid = 0x6B5A56C2, idx = 372, Name = "logger.month_eb_log_ts",                           DataType = t_log_ts,  Desc = "logger.month_eb_log_ts"},
    {msgid = 0x6BA10831, idx = 373, Name = "db.power_board.afi_i30",                           DataType = t_float,   Desc = "AFI 30 mA threshold [A]"},
    {msgid = 0x6BBDC7C8, idx = 374, Name = "line_mon.u_max",                                   DataType = t_float,   Desc = "Max line voltage [V]"},
    {msgid = 0x6BFF1AF4, idx = 375, Name = "hw_test.bt_power[2]",                              DataType = t_float,   Desc = "hw_test.bt_power[2]"},
    {msgid = 0x6C03F5ED, idx = 376, Name = "battery_placeholder[0].bms_power_version",         DataType = t_uint32,  Desc = "Software version BMS Power"},
    {msgid = 0x6C10E96A, idx = 377, Name = "battery_placeholder[0].cells_stat[0].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[0].u_min.time"},
    {msgid = 0x6C243F71, idx = 378, Name = "modbus.address",                                   DataType = t_uint8,   Desc = "RS485 address"},
    {msgid = 0x6C2D00E4, idx = 379, Name = "io_board.rse_table[1]",                            DataType = t_float,   Desc = "K4..K1: 0001"},
    {msgid = 0x6C44F721, idx = 380, Name = "i_dc_max",                                         DataType = t_float,   Desc = "Max. DC-component of Iac [A]"},
    {msgid = 0x6CFCD774, idx = 381, Name = "energy.e_dc_year_sum[1]",                          DataType = t_float,   Desc = "energy.e_dc_year_sum[1]"},
    {msgid = 0x6D5318C8, idx = 382, Name = "cs_map[1]",                                        DataType = t_uint8,   Desc = "Associate current sensor 1 with phase L"},
    {msgid = 0x6D639C25, idx = 383, Name = "battery_placeholder[0].cells_stat[0].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[0].t_min.value"},
    {msgid = 0x6D7C0BF4, idx = 384, Name = "wifi.sockb_port",                                  DataType = t_int32,   Desc = "Port"},
    {msgid = 0x6DB1FDDC, idx = 385, Name = "battery.cells_stat[4].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[4].u_min.value"},
    {msgid = 0x6DCC4097, idx = 386, Name = "net.master_timeout",                               DataType = t_float,   Desc = "net.master_timeout"},
    {msgid = 0x6E1C5B78, idx = 387, Name = "g_sync.p_ac_lp[1]",                                DataType = t_float,   Desc = "AC power phase 2 [W]"},
    {msgid = 0x6E24632E, idx = 388, Name = "battery.cells_stat[5].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[5].u_max.time"},
    {msgid = 0x6E3336A8, idx = 389, Name = "battery_placeholder[0].cells_stat[5].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[5].t_max.index"},
    {msgid = 0x6E491B50, idx = 390, Name = "battery.maximum_charge_voltage",                   DataType = t_float,   Desc = "Max. charge voltage [V]"},
    {msgid = 0x6F3876BC, idx = 391, Name = "logger.error_log_time_stamp",                      DataType = t_int32,   Desc = "Time stamp for error log reading"},
    {msgid = 0x6FB2E2BF, idx = 392, Name = "db.power_board.afi_i150",                          DataType = t_float,   Desc = "AFI 150 mA threshold [A]"},
    {msgid = 0x6FD36B32, idx = 393, Name = "rb485.f_wr[1]",                                    DataType = t_float,   Desc = "Power Storage phase 2 frequency [Hz]"},
    {msgid = 0x6FF4BD55, idx = 394, Name = "energy.e_ext_month_sum",                           DataType = t_float,   Desc = "energy.e_ext_month_sum"},
    {msgid = 0x701A0482, idx = 395, Name = "dc_conv.dc_conv_struct[0].enabled",                DataType = t_bool,    Desc = "Solar generator A connected"},
    {msgid = 0x70349444, idx = 396, Name = "battery.cells_stat[1].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[1].t_min.index"},
    {msgid = 0x70A2AF4F, idx = 397, Name = "battery.bat_status",                               DataType = t_int32,   Desc = "battery.bat_status"},
    {msgid = 0x70BD7C46, idx = 398, Name = "logger.year_eac_log_ts",                           DataType = t_log_ts,  Desc = "logger.year_eac_log_ts"},
    {msgid = 0x70E28322, idx = 399, Name = "grid_mon[0].f_under.time",                         DataType = t_float,   Desc = "Min. frequency switch-off time level 1 [s]"},
    {msgid = 0x71196579, idx = 400, Name = "battery.cells_stat[5].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[5].t_min.index"},
    {msgid = 0x71277E71, idx = 401, Name = "frt.u_min_begin",                                  DataType = t_float,   Desc = "FRT begin undervoltage threshold [V]"},
    {msgid = 0x71465EAF, idx = 402, Name = "nsm.cos_phi_ts",                                   DataType = t_float,   Desc = "Time const for filter [s]"},
    {msgid = 0x715C84A1, idx = 403, Name = "adc.u_ref_1_5v[2]",                                DataType = t_uint16,  Desc = "Reference voltage 3 [V]"},
    {msgid = 0x71765BD8, idx = 404, Name = "battery.status",                                   DataType = t_int32,   Desc = "Battery status"},
    {msgid = 0x71B70DCE, idx = 405, Name = "hw_test.bt_power[4]",                              DataType = t_float,   Desc = "hw_test.bt_power[4]"},
    {msgid = 0x71CB0B57, idx = 406, Name = "battery.cells_resist[1]",                          DataType = t_string,  Desc = "battery.cells_resist[1]"},
    {msgid = 0x71E10B51, idx = 407, Name = "g_sync.p_ac_lp[0]",                                DataType = t_float,   Desc = "AC power phase 1 [W]"},
    {msgid = 0x7232F7AF, idx = 408, Name = "nsm.apm",                                          DataType = t_enum,    Desc = "nsm.apm"},
    {msgid = 0x7268CE4D, idx = 409, Name = "battery.inv_cmd",                                  DataType = t_uint32,  Desc = "battery.inv_cmd"},
    {msgid = 0x72ACC0BF, idx = 410, Name = "logger.minutes_ua_log_ts",                         DataType = t_log_ts,  Desc = "logger.minutes_ua_log_ts"},
    {msgid = 0x7301A5A7, idx = 411, Name = "flash_rtc.time_stamp_factory",                     DataType = t_uint32,  Desc = "Production date"},
    {msgid = 0x73489528, idx = 412, Name = "battery.module_sn[2]",                             DataType = t_string,  Desc = "Module 2 Serial Number"},
    {msgid = 0x73E3ED49, idx = 413, Name = "prim_sm.island_max_trials",                        DataType = t_uint16,  Desc = "Max island trials"},
    {msgid = 0x742966A6, idx = 414, Name = "db.power_board.afi_i300",                          DataType = t_float,   Desc = "AFI 300 mA threshold [A]"},
    {msgid = 0x74FD4609, idx = 415, Name = "battery.cells_stat[2]",                            DataType = t_string,  Desc = "battery.cells_stat[2]"},
    {msgid = 0x751E80CA, idx = 416, Name = "prim_sm.island_reset_retrials_operation_time",     DataType = t_float,   Desc = "Reset island trials counter if island OK in [s]"},
    {msgid = 0x75898A45, idx = 417, Name = "battery_placeholder[0].cells_stat[5].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[5].t_max.time"},
    {msgid = 0x75AE19ED, idx = 418, Name = "hw_test.hw_switch_time",                           DataType = t_float,   Desc = "hw_test.hw_switch_time"},
    {msgid = 0x7689BE6A, idx = 419, Name = "io_board.home_relay_sw_on_delay",                  DataType = t_float,   Desc = "Switching on delay [s]"},
    {msgid = 0x76C9A0BD, idx = 420, Name = "logger.minutes_soc_targ_log_ts",                   DataType = t_log_ts,  Desc = "logger.minutes_soc_targ_log_ts"},
    {msgid = 0x76CAA9BF, idx = 421, Name = "wifi.encryption_algorithm",                        DataType = t_string,  Desc = "wifi.encryption_algorithm"},
    {msgid = 0x770A6E7C, idx = 422, Name = "battery.cells_stat[0].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[0].u_max.index"},
    {msgid = 0x777DC0EB, idx = 423, Name = "iso_struct.r_min",                                 DataType = t_float,   Desc = "Minimum allowed insulation resistance [Ohm]"},
    {msgid = 0x77A9480F, idx = 424, Name = "battery_placeholder[0].minimum_discharge_voltage", DataType = t_float,   Desc = "Min. discharge voltage [V]"},
    {msgid = 0x77DD4364, idx = 425, Name = "hw_test.bt_time[5]",                               DataType = t_float,   Desc = "hw_test.bt_time[5]"},
    {msgid = 0x77E5CEF1, idx = 426, Name = "battery_placeholder[0].stack_software_version[0]", DataType = t_uint32,  Desc = "Software version stack 0"},
    {msgid = 0x78228507, idx = 427, Name = "battery_placeholder[0].stack_cycles[6]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[6]"},
    {msgid = 0x7839EBCB, idx = 428, Name = "battery_placeholder[0].cells_stat[3].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[3].u_min.time"},
    {msgid = 0x7924ABD9, idx = 429, Name = "inverter_sn",                                      DataType = t_string,  Desc = "Serial number"},
    {msgid = 0x792897C9, idx = 430, Name = "battery_placeholder[0].cells_stat[4].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[4].t_min.time"},
    {msgid = 0x792A7B79, idx = 431, Name = "io_board.s0_direction",                            DataType = t_enum,    Desc = "S0 inputs single or bidirectional"},
    {msgid = 0x7940547B, idx = 432, Name = "inv_struct.force_dh",                              DataType = t_bool,    Desc = "inv_struct.force_dh"},
    {msgid = 0x7946D888, idx = 433, Name = "i_dc_slow_time",                                   DataType = t_float,   Desc = "Time for slow DC-component of Iac [s]"},
    {msgid = 0x79C0A724, idx = 434, Name = "energy.e_ac_total_sum",                            DataType = t_float,   Desc = "energy.e_ac_total_sum"},
    {msgid = 0x79D7D617, idx = 435, Name = "battery_placeholder[0].current",                   DataType = t_float,   Desc = "Battery current [A]"},
    {msgid = 0x79E66CDF, idx = 436, Name = "battery_placeholder[0].cells_stat[6].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[6].t_min.index"},
    {msgid = 0x7A5C91F8, idx = 437, Name = "nsm.p_u[1][0]",                                    DataType = t_float,   Desc = "Point 2 P/Pn"},
    {msgid = 0x7A67E33B, idx = 438, Name = "can_bus.bms_update_response[1]",                   DataType = t_uint32,  Desc = "can_bus.bms_update_response[1]"},
    {msgid = 0x7A9091EA, idx = 439, Name = "rb485.u_l_grid[1]",                                DataType = t_float,   Desc = "Grid phase 2 voltage [V]"},
    {msgid = 0x7AB9B045, idx = 440, Name = "energy.e_dc_month[1]",                             DataType = t_float,   Desc = "Solar generator B month energy [Wh]"},
    {msgid = 0x7AE87E39, idx = 441, Name = "partition[2].last_id",                             DataType = t_int32,   Desc = "partition[2].last_id"},
    {msgid = 0x7AF0AD03, idx = 442, Name = "power_mng.schedule[9]",                            DataType = t_string,  Desc = "power_mng.schedule[9]"},
    {msgid = 0x7AF779C1, idx = 443, Name = "nsm.pu_mode",                                      DataType = t_bool,    Desc = "P(U) mode 0: Pn 1: Pload"},
    {msgid = 0x7B1F7FBE, idx = 444, Name = "wifi.gateway",                                     DataType = t_string,  Desc = "Gateway"},
    {msgid = 0x7B8E811E, idx = 445, Name = "battery_placeholder[0].cells_stat[6]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[6]"},
    {msgid = 0x7BF3886B, idx = 446, Name = "battery_placeholder[0].stack_cycles[2]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[2]"},
    {msgid = 0x7C0827C5, idx = 447, Name = "partition[5].last_id",                             DataType = t_int32,   Desc = "partition[5].last_id"},
    {msgid = 0x7C556C7A, idx = 448, Name = "io_board.io2_polarity",                            DataType = t_bool,    Desc = "Inverted signal on input I/O 2"},
    {msgid = 0x7C78CBAC, idx = 449, Name = "g_sync.q_ac_sum_lp",                               DataType = t_float,   Desc = "Reactive power [var]"},
    {msgid = 0x7C863EDB, idx = 450, Name = "battery_placeholder[0].cells[3]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[3]"},
    {msgid = 0x7D839AE6, idx = 451, Name = "battery_placeholder[0].cells_resist[2]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[2]"},
    {msgid = 0x7DA7D8B6, idx = 452, Name = "db.power_board.version_main",                      DataType = t_uint32,  Desc = "PIC software version"},
    {msgid = 0x7DDE352B, idx = 453, Name = "wifi.sockb_ip",                                    DataType = t_string,  Desc = "wifi.sockb_ip"},
    {msgid = 0x7E096024, idx = 454, Name = "energy.e_load_total_sum",                          DataType = t_float,   Desc = "energy.e_load_total_sum"},
    {msgid = 0x7E590128, idx = 455, Name = "battery.cells_stat[0].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[0].u_max.time"},
    {msgid = 0x7E75B17A, idx = 456, Name = "nsm.q_u_max_u_high_rel",                           DataType = t_float,   Desc = "Qmax at upper voltage level relative to Smax (positive = overexcited)"},
    {msgid = 0x7F42BB82, idx = 457, Name = "battery.cells_stat[6].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[6].u_max.index"},
    {msgid = 0x7F813D73, idx = 458, Name = "fault[3].flt",                                     DataType = t_uint32,  Desc = "Error bit field 4"},
    {msgid = 0x7FF6252C, idx = 459, Name = "battery.cells_stat[5].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[5].t_max.time"},
    {msgid = 0x804A3266, idx = 460, Name = "battery.cells_stat[6].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[6].u_max.value"},
    {msgid = 0x80835476, idx = 461, Name = "db.power_board.adc_p5V_W_meas",                    DataType = t_float,   Desc = "db.power_board.adc_p5V_W_meas"},
    {msgid = 0x8128228D, idx = 462, Name = "battery_placeholder[0].cells_stat[1].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[1].u_max.value"},
    {msgid = 0x812E5ADD, idx = 463, Name = "energy.e_dc_total_sum[1]",                         DataType = t_float,   Desc = "energy.e_dc_total_sum[1]"},
    {msgid = 0x8160539D, idx = 464, Name = "battery.cells_stat[4].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[4].t_max.value"},
    {msgid = 0x81AE960B, idx = 465, Name = "energy.e_dc_month[0]",                             DataType = t_float,   Desc = "Solar generator A month energy [Wh]"},
    {msgid = 0x81AF854E, idx = 466, Name = "nsm.pu_use",                                       DataType = t_bool,    Desc = "P(U) active"},
    {msgid = 0x82258C01, idx = 467, Name = "cs_neg[0]",                                        DataType = t_float,   Desc = "Miltiply value of the current sensor 0 by"},
    {msgid = 0x82CD1525, idx = 468, Name = "grid_mon[1].u_under.threshold",                    DataType = t_float,   Desc = "Min. voltage level 2 [V]"},
    {msgid = 0x82E3C121, idx = 469, Name = "g_sync.q_ac[1]",                                   DataType = t_float,   Desc = "Reactive power phase 2 [var]"},
    {msgid = 0x8320B84C, idx = 470, Name = "io_board.rse_data_delay",                          DataType = t_float,   Desc = "Delay for new K4..K1 data [s]"},
    {msgid = 0x8352F9DD, idx = 471, Name = "battery_placeholder[0].cells_stat[4].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[4].t_min.value"},
    {msgid = 0x83A5333A, idx = 472, Name = "nsm.cos_phi_p[0][0]",                              DataType = t_float,   Desc = "Point 1 [P/Pn]"},
    {msgid = 0x83BBEF0B, idx = 473, Name = "frt.u_max_begin",                                  DataType = t_float,   Desc = "FRT begin overvoltage threshold [V]"},
    {msgid = 0x84ABE3D8, idx = 474, Name = "energy.e_grid_feed_year_sum",                      DataType = t_float,   Desc = "energy.e_grid_feed_year_sum"},
    {msgid = 0x85886E2E, idx = 475, Name = "p_rec_lim[0]",                                     DataType = t_float,   Desc = "Max. compensation power [W]"},
    {msgid = 0x8594D11E, idx = 476, Name = "battery_placeholder[0].module_sn[6]",              DataType = t_string,  Desc = "Module 6 Serial Number"},
    {msgid = 0x86782D58, idx = 477, Name = "hw_test.bt_power[9]",                              DataType = t_float,   Desc = "hw_test.bt_power[9]"},
    {msgid = 0x867DEF7D, idx = 478, Name = "energy.e_grid_load_day",                           DataType = t_float,   Desc = "Day energy grid load [Wh]"},
    {msgid = 0x872F380B, idx = 479, Name = "io_board.load_set",                                DataType = t_float,   Desc = "Dummy household load [W]"},
    {msgid = 0x87E4387A, idx = 480, Name = "current_sensor_max",                               DataType = t_float,   Desc = "Power Sensor current range [A]"},
    {msgid = 0x8822EF35, idx = 481, Name = "battery_placeholder[0].stack_software_version[2]", DataType = t_uint32,  Desc = "Software version stack 2"},
    {msgid = 0x883DE9AB, idx = 482, Name = "g_sync.s_ac_lp[2]",                                DataType = t_float,   Desc = "Apparent power phase 3 [VA]"},
    {msgid = 0x885BB57E, idx = 483, Name = "battery.cells_stat[6].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[6].t_min.value"},
    {msgid = 0x887D43C4, idx = 484, Name = "g_sync.i_dr_lp[0]",                                DataType = t_float,   Desc = "Current phase 1 (average) [A]"},
    {msgid = 0x889DC27F, idx = 485, Name = "battery.cells_stat[0].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[0].u_min.value"},
    {msgid = 0x88BBF8CB, idx = 486, Name = "battery.cells_stat[5].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[5].t_min.value"},
    {msgid = 0x88C9707B, idx = 487, Name = "io_board.rse_table[15]",                           DataType = t_float,   Desc = "K4..K1: 1111"},
    {msgid = 0x88DEBCFE, idx = 488, Name = "nsm.q_u_max_u_high",                               DataType = t_float,   Desc = "Qmax at upper voltage level [var] (positive = overexcited)"},
    {msgid = 0x88DFDE8B, idx = 489, Name = "frt.u_max_end",                                    DataType = t_float,   Desc = "FRT end overvoltage threshold [V]"},
    {msgid = 0x88F36D45, idx = 490, Name = "io_board.rse_data",                                DataType = t_uint8,   Desc = "Actual K4..K1 data"},
    {msgid = 0x89B21223, idx = 491, Name = "frt.t_max[0]",                                     DataType = t_float,   Desc = "Point 1 time [s]"},
    {msgid = 0x89B25F4B, idx = 492, Name = "battery.stack_cycles[3]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[3]"},
    {msgid = 0x89EE3EB5, idx = 493, Name = "g_sync.i_dr_eff[0]",                               DataType = t_float,   Desc = "Current phase 1 [A]"},
    {msgid = 0x8A18539B, idx = 494, Name = "g_sync.u_zk_sum_avg",                              DataType = t_float,   Desc = "DC link voltage [V]"},
    {msgid = 0x8AFD1410, idx = 495, Name = "battery_placeholder[0].stack_cycles[4]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[4]"},
    {msgid = 0x8B4BE168, idx = 496, Name = "battery_placeholder[0].soc",                       DataType = t_float,   Desc = "SOC (State of charge)"},
    {msgid = 0x8B9FF008, idx = 497, Name = "battery.soc_target",                               DataType = t_float,   Desc = "Target SOC"},
    {msgid = 0x8BB08839, idx = 498, Name = "battery.cells_stat[6].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[6].t_min.time"},
    {msgid = 0x8C6E28E4, idx = 499, Name = "battery_placeholder[0].cells_stat[2].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[2].t_max.time"},
    {msgid = 0x8CA00014, idx = 500, Name = "wifi.result",                                      DataType = t_int8,    Desc = "WiFi result"},
    {msgid = 0x8D33B6BC, idx = 501, Name = "nsm.f_low_exit",                                   DataType = t_float,   Desc = "Exit frequency for P(f) under-frequency mode [Hz]"},
    {msgid = 0x8D8E19F7, idx = 502, Name = "line_mon.u_min",                                   DataType = t_float,   Desc = "Min line voltage [V]"},
    {msgid = 0x8DD1C728, idx = 503, Name = "dc_conv.dc_conv_struct[1].mpp.enable_scan",        DataType = t_bool,    Desc = "Enable rescan for global MPP on solar generator B"},
    {msgid = 0x8DFFDD33, idx = 504, Name = "battery.cells_stat[3].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[3].u_min.time"},
    {msgid = 0x8E41FC47, idx = 505, Name = "iso_struct.Rp",                                    DataType = t_float,   Desc = "Insulation resistance on positive DC input [Ohm]"},
    {msgid = 0x8EBF9574, idx = 506, Name = "power_mng.soc_min_island",                         DataType = t_float,   Desc = "Min SOC target (island)"},
    {msgid = 0x8EC23427, idx = 507, Name = "battery.cells_stat[4].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[4].u_max.time"},
    {msgid = 0x8EC4116E, idx = 508, Name = "display_struct.blink",                             DataType = t_bool,    Desc = "Display blinking enable"},
    {msgid = 0x8EF6FBBD, idx = 509, Name = "battery.cells[1]",                                 DataType = t_string,  Desc = "battery.cells[1]"},
    {msgid = 0x8EF9C9B8, idx = 510, Name = "battery.cells_stat[6].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[6].t_max.time"},
    {msgid = 0x8F0FF9F3, idx = 511, Name = "p_rec_available[1]",                               DataType = t_float,   Desc = "Available battery to grid power [W]"},
    {msgid = 0x8FC89B10, idx = 512, Name = "com_service",                                      DataType = t_enum,    Desc = "COM service"},
    {msgid = 0x902AFAFB, idx = 513, Name = "battery.temperature",                              DataType = t_float,   Desc = "Battery temperature [°C]"},
    {msgid = 0x903FE89E, idx = 514, Name = "hw_test.bt_time[8]",                               DataType = t_float,   Desc = "hw_test.bt_time[8]"},
    {msgid = 0x905F707B, idx = 515, Name = "rb485.f_wr[2]",                                    DataType = t_float,   Desc = "Power Storage phase 3 frequency [Hz]"},
    {msgid = 0x9061EA7B, idx = 516, Name = "grid_lt.granularity",                              DataType = t_float,   Desc = "Resolution"},
    {msgid = 0x907CD1DF, idx = 517, Name = "wifi.connect_service_max_duration",                DataType = t_int32,   Desc = "Service connection max duration [s]"},
    {msgid = 0x90832471, idx = 518, Name = "battery.cells_stat[1].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[1].u_max.time"},
    {msgid = 0x9095FD74, idx = 519, Name = "battery_placeholder[0].cells[5]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[5]"},
    {msgid = 0x90B53336, idx = 520, Name = "temperature.sink_temp_power_reduction",            DataType = t_float,   Desc = "Heat sink temperature target [°C]"},
    {msgid = 0x90C2AC13, idx = 521, Name = "battery_placeholder[0].stack_cycles[3]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[3]"},
    {msgid = 0x90F123FA, idx = 522, Name = "io_board.io1_usage",                               DataType = t_enum,    Desc = "Digital I/O 1 usage"},
    {msgid = 0x915CD4A4, idx = 523, Name = "grid_mon[1].f_over.threshold",                     DataType = t_float,   Desc = "Max. frequency level 2 [Hz]"},
    {msgid = 0x91617C58, idx = 524, Name = "g_sync.p_ac_grid_sum_lp",                          DataType = t_float,   Desc = "Total grid power [W]"},
    {msgid = 0x917E3622, idx = 525, Name = "energy.e_ext_year",                                DataType = t_float,   Desc = "External year energy [Wh]"},
    {msgid = 0x91C325D9, idx = 526, Name = "battery.cells_stat[0].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[0].t_min.time"},
    {msgid = 0x91FB68CD, idx = 527, Name = "battery.cells_stat[6].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[6].t_max.value"},
    {msgid = 0x920AFF34, idx = 528, Name = "battery_placeholder[0].cells_stat[1].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[1].t_max.index"},
    {msgid = 0x9214A00C, idx = 529, Name = "hw_test.booster_test_index",                       DataType = t_uint8,   Desc = "hw_test.booster_test_index"},
    {msgid = 0x921997EE, idx = 530, Name = "logger.month_egrid_feed_log_ts",                   DataType = t_log_ts,  Desc = "logger.month_egrid_feed_log_ts"},
    {msgid = 0x9247DB99, idx = 531, Name = "logger.minutes_egrid_load_log_ts",                 DataType = t_log_ts,  Desc = "logger.minutes_egrid_load_log_ts"},
    {msgid = 0x929394B7, idx = 532, Name = "svnversion_last_known",                            DataType = t_string,  Desc = "svnversion_last_known"},
    {msgid = 0x92BC682B, idx = 533, Name = "g_sync.i_dr_eff[2]",                               DataType = t_float,   Desc = "Current phase 3 [A]"},
    {msgid = 0x933F9A24, idx = 534, Name = "grid_mon[0].f_over.time",                          DataType = t_float,   Desc = "Max. frequency switch-off time level 1 [s]"},
    {msgid = 0x934E64E9, idx = 535, Name = "switch_on_cond.u_max",                             DataType = t_float,   Desc = "Max. voltage"},
    {msgid = 0x9350FE02, idx = 536, Name = "frt.u_max[2]",                                     DataType = t_float,   Desc = "Point 3 voltage [V]"},
    {msgid = 0x93971C36, idx = 537, Name = "frt.t_max[2]",                                     DataType = t_float,   Desc = "Point 3 time [s]"},
    {msgid = 0x93C0C2E2, idx = 538, Name = "power_mng.bat_calib_reqularity",                   DataType = t_uint32,  Desc = "Battery calibration interval [days]"},
    {msgid = 0x93E6918D, idx = 539, Name = "nsm.f_exit",                                       DataType = t_float,   Desc = "Exit frequency for P(f) over-frequency mode [Hz]"},
    {msgid = 0x93F976AB, idx = 540, Name = "rb485.u_l_grid[0]",                                DataType = t_float,   Desc = "Grid phase 1 voltage [V]"},
    {msgid = 0x940569AC, idx = 541, Name = "hw_test.bt_time[6]",                               DataType = t_float,   Desc = "hw_test.bt_time[6]"},
    {msgid = 0x947DDC38, idx = 542, Name = "battery_placeholder[0].cells_stat[0].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[0].t_min.index"},
    {msgid = 0x9486134F, idx = 543, Name = "battery_placeholder[0].cells_stat[1].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[1].t_max.time"},
    {msgid = 0x9558AD8A, idx = 544, Name = "rb485.f_grid[0]",                                  DataType = t_float,   Desc = "Grid phase1 frequency [Hz]"},
    {msgid = 0x959930BF, idx = 545, Name = "battery.soc",                                      DataType = t_float,   Desc = "SOC (State of charge)"},
    {msgid = 0x95E1E844, idx = 546, Name = "battery_placeholder[0].cells_stat[2].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[2].t_min.time"},
    {msgid = 0x961C8261, idx = 547, Name = "battery_placeholder[0].cells_stat[4].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[4].u_max.time"},
    {msgid = 0x96629BB9, idx = 548, Name = "can_bus.bms_update_state",                         DataType = t_uint8,   Desc = "can_bus.bms_update_state"},
    {msgid = 0x9680077F, idx = 549, Name = "nsm.cos_phi_p[2][0]",                              DataType = t_float,   Desc = "Point 3 [P/Pn]"},
    {msgid = 0x96E32D11, idx = 550, Name = "flash_param.erase_cycles",                         DataType = t_uint32,  Desc = "Erase cycles of flash parameter"},
    {msgid = 0x972B3029, idx = 551, Name = "power_mng.stop_discharge_voltage_buffer",          DataType = t_float,   Desc = "Stop discharge voltage buffer [V]"},
    {msgid = 0x97997C93, idx = 552, Name = "power_mng.soc_max",                                DataType = t_float,   Desc = "Max SOC target"},
    {msgid = 0x97DC2ECB, idx = 553, Name = "battery_placeholder[0].cells[1]",                  DataType = t_string,  Desc = "battery_placeholder[0].cells[1]"},
    {msgid = 0x97E203F9, idx = 554, Name = "power_mng.is_grid",                                DataType = t_bool,    Desc = "power_mng.is_grid"},
    {msgid = 0x97E3A6F2, idx = 555, Name = "power_mng.u_acc_lp",                               DataType = t_float,   Desc = "Battery voltage (inverter) [V]"},
    {msgid = 0x980C5525, idx = 556, Name = "battery_placeholder[0].max_cell_voltage",          DataType = t_float,   Desc = "battery_placeholder[0].max_cell_voltage"},
    {msgid = 0x98ACC1B8, idx = 557, Name = "io_board.rse_table[4]",                            DataType = t_float,   Desc = "K4..K1: 0100"},
    {msgid = 0x99396810, idx = 558, Name = "battery.module_sn[1]",                             DataType = t_string,  Desc = "Module 1 Serial Number"},
    {msgid = 0x993C06F6, idx = 559, Name = "battery.cells_resist[3]",                          DataType = t_string,  Desc = "battery.cells_resist[3]"},
    {msgid = 0x9981F1AC, idx = 560, Name = "db.power_board.adc_m9V_meas",                      DataType = t_float,   Desc = "db.power_board.adc_m9V_meas"},
    {msgid = 0x99EE89CB, idx = 561, Name = "power_mng.power_lim_src_index",                    DataType = t_enum,    Desc = "Power limit source"},
    {msgid = 0x9A33F9B7, idx = 562, Name = "power_mng.schedule[5]",                            DataType = t_string,  Desc = "power_mng.schedule[5]"},
    {msgid = 0x9A51A23B, idx = 563, Name = "logger.log_rate",                                  DataType = t_uint16,  Desc = "Data log resolution [s]"},
    {msgid = 0x9A67600D, idx = 564, Name = "p_rec_lim[2]",                                     DataType = t_float,   Desc = "Pac max. [W]"},
    {msgid = 0x9AAA9CAA, idx = 565, Name = "battery_placeholder[0].stack_cycles[5]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[5]"},
    {msgid = 0x9B92023F, idx = 566, Name = "io_board.rse_table[7]",                            DataType = t_float,   Desc = "K4..K1: 0111"},
    {msgid = 0x9C75BD89, idx = 567, Name = "frt.t_min[0]",                                     DataType = t_float,   Desc = "Point 1 time [s]"},
    {msgid = 0x9C8FE559, idx = 568, Name = "pas.period",                                       DataType = t_uint32,  Desc = "pas.period"},
    {msgid = 0x9D785E8C, idx = 569, Name = "battery.bms_software_version",                     DataType = t_uint32,  Desc = "Software version BMS Master"},
    {msgid = 0x9DC927AA, idx = 570, Name = "bat_mng_struct.profile_load",                      DataType = t_string,  Desc = "bat_mng_struct.profile_load"},
    {msgid = 0x9E1A88F5, idx = 571, Name = "dc_conv.dc_conv_struct[0].mpp.fixed_voltage",      DataType = t_float,   Desc = "Fixed voltage Solar generator A [V]"},
    {msgid = 0x9E314430, idx = 572, Name = "battery.cells_stat[2].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[2].u_max.time"},
    {msgid = 0x9F52F968, idx = 573, Name = "power_mng.feed_asymmetrical",                      DataType = t_bool,    Desc = "Allow asymmetrical feed"},
    {msgid = 0xA10D9A4B, idx = 574, Name = "battery.min_cell_temperature",                     DataType = t_float,   Desc = "battery.min_cell_temperature"},
    {msgid = 0xA1266D6B, idx = 575, Name = "line_mon.time_lim",                                DataType = t_float,   Desc = "Switch off time line voltage [s]"},
    {msgid = 0xA12BE39C, idx = 576, Name = "energy.e_load_month_sum",                          DataType = t_float,   Desc = "energy.e_load_month_sum"},
    {msgid = 0xA12E9B43, idx = 577, Name = "phase_marker",                                     DataType = t_int16,   Desc = "Next phase after phase 1"},
    {msgid = 0xA1D2B565, idx = 578, Name = "wifi.service_port",                                DataType = t_int32,   Desc = "wifi.service_port"},
    {msgid = 0xA23FE8B9, idx = 579, Name = "battery_placeholder[0].cells_stat[6].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[6].t_min.value"},
    {msgid = 0xA2F87161, idx = 580, Name = "battery_placeholder[0].cells_stat[0].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[0].u_max.time"},
    {msgid = 0xA305214D, idx = 581, Name = "logger.buffer",                                    DataType = t_string,  Desc = "logger.buffer"},
    {msgid = 0xA3393749, idx = 582, Name = "io_board.check_start",                             DataType = t_uint8,   Desc = "io_board.check_start"},
    {msgid = 0xA33D0954, idx = 583, Name = "nsm.q_u_hysteresis",                               DataType = t_bool,    Desc = "Curve with hysteresis"},
    {msgid = 0xA3E48B21, idx = 584, Name = "battery.cells_stat[2].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[2].t_min.value"},
    {msgid = 0xA40906BF, idx = 585, Name = "battery.stack_software_version[4]",                DataType = t_uint32,  Desc = "Software version stack 4"},
    {msgid = 0xA5044DCD, idx = 586, Name = "nsm.p_u[2][0]",                                    DataType = t_float,   Desc = "Point 3 P/Pn"},
    {msgid = 0xA5341F4A, idx = 587, Name = "energy.e_grid_feed_month_sum",                     DataType = t_float,   Desc = "energy.e_grid_feed_month_sum"},
    {msgid = 0xA54C4685, idx = 588, Name = "battery.stack_software_version[1]",                DataType = t_uint32,  Desc = "Software version stack 1"},
    {msgid = 0xA59C8428, idx = 589, Name = "energy.e_ext_total",                               DataType = t_float,   Desc = "External total energy [Wh]"},
    {msgid = 0xA60082A9, idx = 590, Name = "logger.minutes_egrid_feed_log_ts",                 DataType = t_log_ts,  Desc = "logger.minutes_egrid_feed_log_ts"},
    {msgid = 0xA616B022, idx = 591, Name = "battery.soc_target_low",                           DataType = t_float,   Desc = "SOC target low"},
    {msgid = 0xA6271C2E, idx = 592, Name = "grid_mon[0].u_over.threshold",                     DataType = t_float,   Desc = "Max. voltage level 1 [V]"},
    {msgid = 0xA6871A4D, idx = 593, Name = "battery.cells_stat[4].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[4].t_min.index"},
    {msgid = 0xA6C4FD4A, idx = 594, Name = "battery.stack_cycles[0]",                          DataType = t_uint16,  Desc = "battery.stack_cycles[0]"},
    {msgid = 0xA7447FC4, idx = 595, Name = "temperature.bat_temp_power_reduction",             DataType = t_float,   Desc = "Battery actuator temperature target [°C]"},
    {msgid = 0xA76AE9CA, idx = 596, Name = "relays.bits_real",                                 DataType = t_uint16,  Desc = "relays.bits_real"},
    {msgid = 0xA7C708EB, idx = 597, Name = "logger.minutes_eload_log_ts",                      DataType = t_log_ts,  Desc = "logger.minutes_eload_log_ts"},
    {msgid = 0xA7DBD28C, idx = 598, Name = "battery.cells_stat[2].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[2].t_max.index"},
    {msgid = 0xA7F4123B, idx = 599, Name = "battery_placeholder[0].stack_software_version[6]", DataType = t_uint32,  Desc = "Software version stack 6"},
    {msgid = 0xA7FA5C5D, idx = 600, Name = "power_mng.u_acc_mix_lp",                           DataType = t_float,   Desc = "Battery voltage [V]"},
    {msgid = 0xA7FE5C0C, idx = 601, Name = "battery.cells_stat[2].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[2].t_min.index"},
    {msgid = 0xA81176D0, idx = 602, Name = "battery_placeholder[0].cells_stat[1].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[1].u_min.time"},
    {msgid = 0xA83F291F, idx = 603, Name = "battery_placeholder[0].cells_stat[6].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[6].u_min.value"},
    {msgid = 0xA8FEAEB9, idx = 604, Name = "battery_placeholder[0].cells_resist[5]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[5]"},
    {msgid = 0xA9033880, idx = 605, Name = "battery.used_energy",                              DataType = t_float,   Desc = "Total energy flow from battery [Wh]"},
    {msgid = 0xA95AD038, idx = 606, Name = "grid_mon[0].f_under.threshold",                    DataType = t_float,   Desc = "Min. frequency level 1 [Hz]"},
    {msgid = 0xA95EE214, idx = 607, Name = "power_mng.model.bat_power_change",                 DataType = t_float,   Desc = "power_mng.model.bat_power_change"},
    {msgid = 0xA9CF517D, idx = 608, Name = "power_spring_down",                                DataType = t_float,   Desc = "power_spring_down"},
    {msgid = 0xAA911BEE, idx = 609, Name = "battery_placeholder[0].cells_stat[4].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[4].t_max.value"},
    {msgid = 0xAA9AA253, idx = 610, Name = "dc_conv.dc_conv_struct[1].p_dc",                   DataType = t_float,   Desc = "Solar generator B power [W]"},
    {msgid = 0xAACAC898, idx = 611, Name = "battery.cells_stat[4].t_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[4].t_max.time"},
    {msgid = 0xAACE057A, idx = 612, Name = "io_board.io1_s0_min_duration",                     DataType = t_float,   Desc = "Minimum S0 signal duration on I/O 1 [s]"},
    {msgid = 0xABA015FC, idx = 613, Name = "battery_placeholder[0].module_sn[1]",              DataType = t_string,  Desc = "Module 1 Serial Number"},
    {msgid = 0xAC2E2A56, idx = 614, Name = "io_board.rse_table[5]",                            DataType = t_float,   Desc = "K4..K1: 0101"},
    {msgid = 0xACF7666B, idx = 615, Name = "battery.efficiency",                               DataType = t_float,   Desc = "Battery efficiency (used energy / stored energy)"},
    {msgid = 0xAE99F87A, idx = 616, Name = "battery_placeholder[0].cells_stat[5].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[5].t_min.time"},
    {msgid = 0xAEF76FA1, idx = 617, Name = "power_mng.minimum_discharge_voltage",              DataType = t_float,   Desc = "Min. battery discharge voltage [V]"},
    {msgid = 0xAF64D0FE, idx = 618, Name = "energy.e_dc_year[0]",                              DataType = t_float,   Desc = "Solar generator A year energy [Wh]"},
    {msgid = 0xB0041187, idx = 619, Name = "g_sync.u_sg_avg[1]",                               DataType = t_float,   Desc = "Solar generator B voltage [V]"},
    {msgid = 0xB0307591, idx = 620, Name = "db.power_board.status",                            DataType = t_uint16,  Desc = "Power board status"},
    {msgid = 0xB082C4D7, idx = 621, Name = "hw_test.bt_power[5]",                              DataType = t_float,   Desc = "hw_test.bt_power[5]"},
    {msgid = 0xB0EBE75A, idx = 622, Name = "battery.minimum_discharge_voltage",                DataType = t_float,   Desc = "Min. discharge voltage [V]"},
    {msgid = 0xB0FA4D23, idx = 623, Name = "acc_conv.i_charge_max",                            DataType = t_float,   Desc = "Max. battery converter charge current [A]"},
    {msgid = 0xB130B8D6, idx = 624, Name = "battery_placeholder[0].cells_stat[1].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[1].t_min.time"},
    {msgid = 0xB1D1BE71, idx = 625, Name = "osci_struct.cmd_response_time",                    DataType = t_float,   Desc = "osci_struct.cmd_response_time"},
    {msgid = 0xB1D465C7, idx = 626, Name = "battery_placeholder[0].cells_stat[4].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[4].u_min.value"},
    {msgid = 0xB1EF67CE, idx = 627, Name = "energy.e_ac_total",                                DataType = t_float,   Desc = "Total energy [Wh]"},
    {msgid = 0xB20D1AD6, idx = 628, Name = "logger.day_egrid_feed_log_ts",                     DataType = t_log_ts,  Desc = "logger.day_egrid_feed_log_ts"},
    {msgid = 0xB221BCFA, idx = 629, Name = "g_sync.p_ac_sc[2]",                                DataType = t_float,   Desc = "Grid power phase 3 [W]"},
    {msgid = 0xB228EC94, idx = 630, Name = "battery_placeholder[0].cells_stat[3].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[3].t_max.time"},
    {msgid = 0xB238942F, idx = 631, Name = "last_successfull_flash_op",                        DataType = t_int16,   Desc = "last_successfull_flash_op"},
    {msgid = 0xB298395D, idx = 632, Name = "dc_conv.dc_conv_struct[0].u_sg_lp",                DataType = t_float,   Desc = "Solar generator A voltage [V]"},
    {msgid = 0xB2FB9A90, idx = 633, Name = "bat_mng_struct.k_trust",                           DataType = t_float,   Desc = "How fast the actual prediction can be trusted"},
    {msgid = 0xB399B5B3, idx = 634, Name = "battery_placeholder[0].cells_stat[4].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[4].u_min.index"},
    {msgid = 0xB403A7E6, idx = 635, Name = "battery_placeholder[0].soc_update_since",          DataType = t_float,   Desc = "battery_placeholder[0].soc_update_since"},
    {msgid = 0xB408E40A, idx = 636, Name = "acc_conv.i_acc_lp_slow",                           DataType = t_float,   Desc = "acc_conv.i_acc_lp_slow"},
    {msgid = 0xB4222BDE, idx = 637, Name = "wifi.state",                                       DataType = t_uint8,   Desc = "wifi.state"},
    {msgid = 0xB45FE275, idx = 638, Name = "p_rec_available[0]",                               DataType = t_float,   Desc = "Available compensation power [W]"},
    {msgid = 0xB4E053D4, idx = 639, Name = "battery.cells_stat[1].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[1].u_min.value"},
    {msgid = 0xB5317B78, idx = 640, Name = "dc_conv.dc_conv_struct[0].p_dc",                   DataType = t_float,   Desc = "Solar generator A power [W]"},
    {msgid = 0xB55BA2CE, idx = 641, Name = "g_sync.u_sg_avg[0]",                               DataType = t_float,   Desc = "Solar generator A voltage [V]"},
    {msgid = 0xB57B59BD, idx = 642, Name = "battery.ah_capacity",                              DataType = t_float,   Desc = "Battery capacity [Ah]"},
    {msgid = 0xB5EDA8EC, idx = 643, Name = "battery_placeholder[0].cells_stat[3].u_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[3].u_max.value"},
    {msgid = 0xB6623608, idx = 644, Name = "power_mng.bat_next_calib_date",                    DataType = t_uint32,  Desc = "Next battery calibration"},
    {msgid = 0xB69171C4, idx = 645, Name = "db.power_board.Current_AC_RMS",                    DataType = t_float,   Desc = "db.power_board.Current_AC_RMS"},
    {msgid = 0xB70D1703, idx = 646, Name = "battery_placeholder[0].cells_stat[5].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[5].u_max.index"},
    {msgid = 0xB76E2B4C, idx = 647, Name = "nsm.cos_phi_const",                                DataType = t_float,   Desc = "Cos phi constant value (positive = overexcited)"},
    {msgid = 0xB7B2967F, idx = 648, Name = "energy.e_dc_total_sum[0]",                         DataType = t_float,   Desc = "energy.e_dc_total_sum[0]"},
    {msgid = 0xB7C85C51, idx = 649, Name = "wifi.use_ethernet",                                DataType = t_bool,    Desc = "wifi.use_ethernet"},
    {msgid = 0xB7FEA209, idx = 650, Name = "wifi.connect_service_timestamp",                   DataType = t_int32,   Desc = "Service auto disconnect time"},
    {msgid = 0xB81FB399, idx = 651, Name = "battery.cells_stat[2].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[2].u_min.time"},
    {msgid = 0xB836B50C, idx = 652, Name = "dc_conv.dc_conv_struct[1].rescan_correction",      DataType = t_float,   Desc = "Last global rescan MPP correction on input B [V]"},
    {msgid = 0xB84A38AB, idx = 653, Name = "battery.soc_target_high",                          DataType = t_float,   Desc = "SOC target high"},
    {msgid = 0xB84FDCF9, idx = 654, Name = "adc.u_acc",                                        DataType = t_float,   Desc = "Battery voltage (inverter) [V]"},
    {msgid = 0xB851FA70, idx = 655, Name = "io_board.rse_table[11]",                           DataType = t_float,   Desc = "K4..K1: 1011"},
    {msgid = 0xB98C8194, idx = 656, Name = "nsm.min_cos_phi",                                  DataType = t_float,   Desc = "Minimum allowed cos(phi) [0..1]"},
    {msgid = 0xB9928C51, idx = 657, Name = "g_sync.p_ac_lp[2]",                                DataType = t_float,   Desc = "AC power phase 3 [W]"},
    {msgid = 0xB9A026F9, idx = 658, Name = "energy.e_ext_day",                                 DataType = t_float,   Desc = "External day energy [Wh]"},
    {msgid = 0xB9E09F78, idx = 659, Name = "battery.cells_stat[5].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[5].u_min.index"},
    {msgid = 0xBA046C03, idx = 660, Name = "battery_placeholder[0].cells_stat[5].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[5].t_max.value"},
    {msgid = 0xBA8B8515, idx = 661, Name = "dc_conv.dc_conv_struct[0].mpp.mpp_step",           DataType = t_float,   Desc = "MPP search step on input A [V]"},
    {msgid = 0xBB302278, idx = 662, Name = "battery.cells_stat[1].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[1].t_min.time"},
    {msgid = 0xBB617E51, idx = 663, Name = "nsm.u_q_u[1]",                                     DataType = t_float,   Desc = "Low voltage max. point [V]"},
    {msgid = 0xBBE6B9DF, idx = 664, Name = "io_board.p_rse_rise_grad",                         DataType = t_float,   Desc = "Power rise gradient [P/Pn/s]"},
    {msgid = 0xBCA77559, idx = 665, Name = "g_sync.q_ac[2]",                                   DataType = t_float,   Desc = "Reactive power phase 3 [var]"},
    {msgid = 0xBCC6F92F, idx = 666, Name = "io_board.home_relay_threshold",                    DataType = t_float,   Desc = "Switching on threshold [W]"},
    {msgid = 0xBD008E29, idx = 667, Name = "power_mng.battery_power_extern",                   DataType = t_float,   Desc = "Battery target power [W] (positive = discharge)"},
    {msgid = 0xBD3A23C3, idx = 668, Name = "power_mng.soc_charge",                             DataType = t_float,   Desc = "SOC min maintenance charge"},
    {msgid = 0xBD4147B0, idx = 669, Name = "can_bus.set_cell_resist",                          DataType = t_uint32,  Desc = "can_bus.set_cell_resist"},
    {msgid = 0xBD55905F, idx = 670, Name = "energy.e_ac_day",                                  DataType = t_float,   Desc = "Day energy [Wh]"},
    {msgid = 0xBD55D796, idx = 671, Name = "energy.e_dc_year[1]",                              DataType = t_float,   Desc = "Solar generator B year energy [Wh]"},
    {msgid = 0xBD95C46C, idx = 672, Name = "battery_placeholder[0].ah_capacity",               DataType = t_float,   Desc = "Battery capacity [Ah]"},
    {msgid = 0xBDE3BF0A, idx = 673, Name = "battery.cells_stat[6].t_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[6].t_max.index"},
    {msgid = 0xBDFE5547, idx = 674, Name = "io_board.rse_table[3]",                            DataType = t_float,   Desc = "K4..K1: 0011"},
    {msgid = 0xBF9B6042, idx = 675, Name = "svnversion_factory",                               DataType = t_string,  Desc = "Control software factory version"},
    {msgid = 0xBFFF3CAD, idx = 676, Name = "net.n_slaves",                                     DataType = t_uint8,   Desc = "net.n_slaves"},
    {msgid = 0xC03462F6, idx = 677, Name = "g_sync.p_ac[2]",                                   DataType = t_float,   Desc = "AC3"},
    {msgid = 0xC04A5F3A, idx = 678, Name = "battery_placeholder[0].bms_software_version",      DataType = t_uint32,  Desc = "Software version BMS Master"},
    {msgid = 0xC0680302, idx = 679, Name = "battery.cells_stat[2].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[2].t_min.time"},
    {msgid = 0xC07E02CE, idx = 680, Name = "nsm.q_u_sel",                                      DataType = t_enum,    Desc = "Voltage selection"},
    {msgid = 0xC0A7074F, idx = 681, Name = "net.slave_data",                                   DataType = t_string,  Desc = "net.slave_data"},
    {msgid = 0xC0B7C4D2, idx = 682, Name = "db.power_board.afi_t30",                           DataType = t_float,   Desc = "AFI 30 mA switching off time [s]"},
    {msgid = 0xC0CC81B6, idx = 683, Name = "energy.e_ac_year",                                 DataType = t_float,   Desc = "Year energy [Wh]"},
    {msgid = 0xC0DF2978, idx = 684, Name = "battery.cycles",                                   DataType = t_int32,   Desc = "Battery charge / discharge cycles"},
    {msgid = 0xC198B25B, idx = 685, Name = "g_sync.u_zk_p_avg",                                DataType = t_float,   Desc = "Positive buffer capacitor voltage [V]"},
    {msgid = 0xC1C82889, idx = 686, Name = "hw_test.bt_power[1]",                              DataType = t_float,   Desc = "hw_test.bt_power[1]"},
    {msgid = 0xC1D051EC, idx = 687, Name = "display_struct.variate_contrast",                  DataType = t_uint8,   Desc = "display_struct.variate_contrast"},
    {msgid = 0xC24E85D0, idx = 688, Name = "db.core_temp",                                     DataType = t_float,   Desc = "Core temperature [°C]"},
    {msgid = 0xC3352B17, idx = 689, Name = "nsm.rpm",                                          DataType = t_enum,    Desc = "nsm.rpm"},
    {msgid = 0xC36675D4, idx = 690, Name = "i_ac_max_set",                                     DataType = t_float,   Desc = "Maximum AC throttle current [A]"},
    {msgid = 0xC3A3F070, idx = 691, Name = "i_ac_extern_connected",                            DataType = t_bool,    Desc = "Current sensors detected"},
    {msgid = 0xC3C7325E, idx = 692, Name = "hw_test.bt_time[4]",                               DataType = t_float,   Desc = "hw_test.bt_time[4]"},
    {msgid = 0xC3DD7850, idx = 693, Name = "partition[6].last_id",                             DataType = t_int32,   Desc = "partition[6].last_id"},
    {msgid = 0xC40D5688, idx = 694, Name = "prim_sm.state_source",                             DataType = t_uint32,  Desc = "prim_sm.state_source"},
    {msgid = 0xC42F5807, idx = 695, Name = "battery.cells_stat[1].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[1].u_max.index"},
    {msgid = 0xC46E9CA4, idx = 696, Name = "nsm.u_lock_out",                                   DataType = t_float,   Desc = "Cos phi(P) lock out voltage [V]"},
    {msgid = 0xC4D87E96, idx = 697, Name = "prim_sm.island_retrials",                          DataType = t_uint16,  Desc = "Island trials counter"},
    {msgid = 0xC4FA4E33, idx = 698, Name = "frt.u_min[1]",                                     DataType = t_float,   Desc = "Point 2 voltage [V]"},
    {msgid = 0xC55EF32E, idx = 699, Name = "logger.year_egrid_load_log_ts",                    DataType = t_log_ts,  Desc = "logger.year_egrid_load_log_ts"},
    {msgid = 0xC56A1346, idx = 700, Name = "battery_placeholder[0].cells_stat[4].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[4].t_max.index"},
    {msgid = 0xC642B9D6, idx = 701, Name = "acc_conv.i_discharge_max",                         DataType = t_float,   Desc = "Max. battery converter discharge current [A]"},
    {msgid = 0xC66665E8, idx = 702, Name = "battery_placeholder[0].temperature",               DataType = t_float,   Desc = "Battery temperature [°C]"},
    {msgid = 0xC66A522B, idx = 703, Name = "hw_test.bt_time[1]",                               DataType = t_float,   Desc = "hw_test.bt_time[1]"},
    {msgid = 0xC6DA81A0, idx = 704, Name = "battery.cells_stat[6].u_max.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[6].u_max.time"},
    {msgid = 0xC707102E, idx = 705, Name = "hw_test.bt_power[3]",                              DataType = t_float,   Desc = "hw_test.bt_power[3]"},
    {msgid = 0xC71155B5, idx = 706, Name = "battery_placeholder[0].cells_stat[2].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[2].t_min.index"},
    {msgid = 0xC717D1FB, idx = 707, Name = "iso_struct.Riso",                                  DataType = t_float,   Desc = "Total insulation resistance [Ohm]"},
    {msgid = 0xC7459513, idx = 708, Name = "power_mng.force_inv_class",                        DataType = t_enum,    Desc = "Change inverter class"},
    {msgid = 0xC7605E16, idx = 709, Name = "io_board.s0_sum",                                  DataType = t_float,   Desc = "io_board.s0_sum"},
    {msgid = 0xC7D3B479, idx = 710, Name = "energy.e_load_year",                               DataType = t_float,   Desc = "Household year energy [Wh]"},
    {msgid = 0xC7E85F32, idx = 711, Name = "battery_placeholder[0].cells_stat[4].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[4].t_max.time"},
    {msgid = 0xC8609C8E, idx = 712, Name = "battery.cells[3]",                                 DataType = t_string,  Desc = "battery.cells[3]"},
    {msgid = 0xC88EB032, idx = 713, Name = "battery.cells_stat[0].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[0].u_min.time"},
    {msgid = 0xC8BA1729, idx = 714, Name = "battery.stack_software_version[2]",                DataType = t_uint32,  Desc = "Software version stack 2"},
    {msgid = 0xC8E56803, idx = 715, Name = "battery_placeholder[0].maximum_charge_voltage",    DataType = t_float,   Desc = "Max. charge voltage [V]"},
    {msgid = 0xC937D38D, idx = 716, Name = "battery_placeholder[0].stack_cycles[0]",           DataType = t_uint16,  Desc = "battery_placeholder[0].stack_cycles[0]"},
    {msgid = 0xC9900716, idx = 717, Name = "power_mng.is_island_only",                         DataType = t_bool,    Desc = "Island without power switch support"},
    {msgid = 0xC9D76279, idx = 718, Name = "energy.e_dc_day_sum[0]",                           DataType = t_float,   Desc = "energy.e_dc_day_sum[0]"},
    {msgid = 0xCA4E0C03, idx = 719, Name = "battery_placeholder[0].cells_stat[5].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[5].u_max.time"},
    {msgid = 0xCA6D6472, idx = 720, Name = "logger.day_eload_log_ts",                          DataType = t_log_ts,  Desc = "logger.day_eload_log_ts"},
    {msgid = 0xCABC44CA, idx = 721, Name = "g_sync.s_ac[0]",                                   DataType = t_float,   Desc = "Apparent power phase 1 [VA]"},
    {msgid = 0xCB1B3B10, idx = 722, Name = "io_board.io2_s0_min_duration",                     DataType = t_float,   Desc = "Minimum S0 signal duration on I/O 2 [s]"},
    {msgid = 0xCB78F611, idx = 723, Name = "frt.t_max[1]",                                     DataType = t_float,   Desc = "Point 2 time [s]"},
    {msgid = 0xCB85C397, idx = 724, Name = "battery_placeholder[0].cells_stat[3].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[3].u_min.value"},
    {msgid = 0xCB9E1E6C, idx = 725, Name = "nsm.Q_const",                                      DataType = t_float,   Desc = "Constant reactive power [var] (positive = overexcited)"},
    {msgid = 0xCBBEEB21, idx = 726, Name = "battery_placeholder[0].cells_stat[2].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[2].u_max.time"},
    {msgid = 0xCBDAD315, idx = 727, Name = "logger.minutes_ebat_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_ebat_log_ts"},
    {msgid = 0xCBEC8200, idx = 728, Name = "hw_test.timer2",                                   DataType = t_float,   Desc = "hw_test.timer2"},
    {msgid = 0xCCB51399, idx = 729, Name = "nsm.q_u_max_u_low",                                DataType = t_float,   Desc = "Qmax at lower voltage level [var] (positive = overexcited)"},
    {msgid = 0xCD8EDAD3, idx = 730, Name = "battery_placeholder[0].cells_stat[3].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[3].t_min.value"},
    {msgid = 0xCE266F0F, idx = 731, Name = "power_mng.soc_min",                                DataType = t_float,   Desc = "Min SOC target"},
    {msgid = 0xCE49EB86, idx = 732, Name = "battery_placeholder[0].cells_stat[2].t_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[2].t_max.index"},
    {msgid = 0xCF005C54, idx = 733, Name = "prim_sm.phase_3_mode",                             DataType = t_bool,    Desc = "prim_sm.phase_3_mode"},
    {msgid = 0xCF053085, idx = 734, Name = "g_sync.u_l_rms[0]",                                DataType = t_float,   Desc = "AC voltage phase 1 [V]"},
    {msgid = 0xCF096A6B, idx = 735, Name = "battery_placeholder[0].stack_software_version[4]", DataType = t_uint32,  Desc = "Software version stack 4"},
    {msgid = 0xD0C47326, idx = 736, Name = "battery.cells_stat[1].t_min.value",                DataType = t_float,   Desc = "battery.cells_stat[1].t_min.value"},
    {msgid = 0xD143A391, idx = 737, Name = "can_bus.set_cell_v_t",                             DataType = t_uint32,  Desc = "can_bus.set_cell_v_t"},
    {msgid = 0xD166D94D, idx = 738, Name = "flash_rtc.time_stamp",                             DataType = t_uint32,  Desc = "Actual date/time"},
    {msgid = 0xD197CBE0, idx = 739, Name = "power_mng.stop_charge_current",                    DataType = t_float,   Desc = "Stop charge current [A]"},
    {msgid = 0xD1DFC969, idx = 740, Name = "power_mng.soc_target_set",                         DataType = t_float,   Desc = "Force SOC target"},
    {msgid = 0xD1F9D017, idx = 741, Name = "battery_placeholder[0].cells_stat[4].u_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[4].u_min.time"},
    {msgid = 0xD2DEA4B1, idx = 742, Name = "battery_placeholder[0].cells_stat[5].t_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[5].t_min.index"},
    {msgid = 0xD3085D80, idx = 743, Name = "net.soc_av",                                       DataType = t_float,   Desc = "net.soc_av"},
    {msgid = 0xD3E94E6B, idx = 744, Name = "logger.minutes_temp_bat_log_ts",                   DataType = t_log_ts,  Desc = "logger.minutes_temp_bat_log_ts"},
    {msgid = 0xD3F492EB, idx = 745, Name = "battery_placeholder[0].cells_stat[0].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[0].t_max.time"},
    {msgid = 0xD451EF88, idx = 746, Name = "cs_map[2]",                                        DataType = t_uint8,   Desc = "Associate current sensor 2 with phase L"},
    {msgid = 0xD45913EC, idx = 747, Name = "io_board.rse_table[13]",                           DataType = t_float,   Desc = "K4..K1: 1101"},
    {msgid = 0xD4C4A941, idx = 748, Name = "hw_test.bt_time[7]",                               DataType = t_float,   Desc = "hw_test.bt_time[7]"},
    {msgid = 0xD5205A45, idx = 749, Name = "net.slave_timeout",                                DataType = t_float,   Desc = "net.slave_timeout"},
    {msgid = 0xD536E7E9, idx = 750, Name = "frt.u_max[1]",                                     DataType = t_float,   Desc = "Point 2 voltage [V]"},
    {msgid = 0xD5567470, idx = 751, Name = "partition[4].last_id",                             DataType = t_int32,   Desc = "partition[4].last_id"},
    {msgid = 0xD5790CE1, idx = 752, Name = "wifi.use_wifi",                                    DataType = t_bool,    Desc = "Enable Wi-Fi Access Point"},
    {msgid = 0xD580567B, idx = 753, Name = "nsm.u_lock_in",                                    DataType = t_float,   Desc = "Cos phi(P) lock in voltage [V]"},
    {msgid = 0xD60E7A2F, idx = 754, Name = "battery.cells_stat[1].u_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[1].u_min.time"},
    {msgid = 0xD81471DF, idx = 755, Name = "battery_placeholder[0].cells_stat[6].t_max.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[6].t_max.value"},
    {msgid = 0xD82F2D0B, idx = 756, Name = "battery_placeholder[0].cells_stat[3].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[3].u_min.index"},
    {msgid = 0xD83DC6AC, idx = 757, Name = "wifi.server_port",                                 DataType = t_int32,   Desc = "wifi.server_port"},
    {msgid = 0xD876A4AC, idx = 758, Name = "battery_placeholder[0].cells_stat[0].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[0].u_min.index"},
    {msgid = 0xD884AF95, idx = 759, Name = "nsm.pf_desc_grad",                                 DataType = t_float,   Desc = "Power decrease gradient for P(f) mode [P/(Pn*s)]"},
    {msgid = 0xD9D66B76, idx = 760, Name = "energy.e_grid_load_year_sum",                      DataType = t_float,   Desc = "energy.e_grid_load_year_sum"},
    {msgid = 0xD9E721A5, idx = 761, Name = "grid_lt.timeframe",                                DataType = t_float,   Desc = "Timeframe"},
    {msgid = 0xD9F9F35B, idx = 762, Name = "acc_conv.state_slow",                              DataType = t_uint8,   Desc = "acc_conv.state_slow"},
    {msgid = 0xDA207111, idx = 763, Name = "energy.e_grid_load_month_sum",                     DataType = t_float,   Desc = "energy.e_grid_load_month_sum"},
    {msgid = 0xDABD323E, idx = 764, Name = "osci_struct.error",                                DataType = t_int16,   Desc = "Communication error"},
    {msgid = 0xDAC7DD86, idx = 765, Name = "io_board.p_rse_desc_grad",                         DataType = t_float,   Desc = "Power descent gradient [P/Pn/s]"},
    {msgid = 0xDB11855B, idx = 766, Name = "dc_conv.dc_conv_struct[0].p_dc_lp",                DataType = t_float,   Desc = "Solar generator A power [W]"},
    {msgid = 0xDB2D69AE, idx = 767, Name = "g_sync.p_ac_sum_lp",                               DataType = t_float,   Desc = "AC power [W]"},
    {msgid = 0xDB45ABD0, idx = 768, Name = "dc_conv.dc_conv_struct[0].rescan_correction",      DataType = t_float,   Desc = "Last global rescan MPP correction on input A [V]"},
    {msgid = 0xDB62DCB7, idx = 769, Name = "net.n_devices",                                    DataType = t_uint8,   Desc = "net.n_devices"},
    {msgid = 0xDC667958, idx = 770, Name = "power_mng.state",                                  DataType = t_uint8,   Desc = "Battery state machine"},
    {msgid = 0xDCA1CF26, idx = 771, Name = "g_sync.s_ac_sum_lp",                               DataType = t_float,   Desc = "Apparent power [VA]"},
    {msgid = 0xDCAC0EA9, idx = 772, Name = "g_sync.i_dr_lp[1]",                                DataType = t_float,   Desc = "Current phase 2 (average) [A]"},
    {msgid = 0xDD5930A2, idx = 773, Name = "battery.cells_stat[0].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[0].t_min.index"},
    {msgid = 0xDD90A328, idx = 774, Name = "flash_rtc.time_stamp_update",                      DataType = t_uint32,  Desc = "Last update date"},
    {msgid = 0xDDD1C2D0, idx = 775, Name = "svnversion",                                       DataType = t_string,  Desc = "Control software version"},
    {msgid = 0xDE17F021, idx = 776, Name = "energy.e_grid_load_year",                          DataType = t_float,   Desc = "Year energy grid load [Wh]"},
    {msgid = 0xDE68F62D, idx = 777, Name = "bat_mng_struct.profile_pext",                      DataType = t_string,  Desc = "bat_mng_struct.profile_pext"},
    {msgid = 0xDE9CBCB0, idx = 778, Name = "battery.cells_stat[5].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[5].t_max.value"},
    {msgid = 0xDEE1957F, idx = 779, Name = "battery.cells_resist[4]",                          DataType = t_string,  Desc = "battery.cells_resist[4]"},
    {msgid = 0xDF0A735C, idx = 780, Name = "battery.maximum_discharge_current",                DataType = t_float,   Desc = "Max. discharge current [A]"},
    {msgid = 0xDF6EA121, idx = 781, Name = "bat_mng_struct.profile_pdc",                       DataType = t_string,  Desc = "bat_mng_struct.profile_pdc"},
    {msgid = 0xDFB53AF3, idx = 782, Name = "db.power_board.Current_Mean_Mean_AC",              DataType = t_float,   Desc = "db.power_board.Current_Mean_Mean_AC"},
    {msgid = 0xDFF966E3, idx = 783, Name = "battery.cells_stat[6].t_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[6].t_min.index"},
    {msgid = 0xE04C3900, idx = 784, Name = "logger.day_eac_log_ts",                            DataType = t_log_ts,  Desc = "logger.day_eac_log_ts"},
    {msgid = 0xE0E16E63, idx = 785, Name = "cs_map[0]",                                        DataType = t_uint8,   Desc = "Associate current sensor 0 with phase L"},
    {msgid = 0xE14B8679, idx = 786, Name = "i_dc_slow_max",                                    DataType = t_float,   Desc = "Max. slow DC-component of Iac [A]"},
    {msgid = 0xE14F1CBA, idx = 787, Name = "battery_placeholder[0].cells_stat[4]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[4]"},
    {msgid = 0xE19C8B79, idx = 788, Name = "battery_placeholder[0].cells_resist[1]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[1]"},
    {msgid = 0xE1F49459, idx = 789, Name = "frt.t_min[2]",                                     DataType = t_float,   Desc = "Point 3 time [s]"},
    {msgid = 0xE24B00BD, idx = 790, Name = "power_mng.schedule[1]",                            DataType = t_string,  Desc = "power_mng.schedule[1]"},
    {msgid = 0xE271C6D2, idx = 791, Name = "nsm.u_q_u[2]",                                     DataType = t_float,   Desc = "High voltage min. point [V]"},
    {msgid = 0xE29C24EB, idx = 792, Name = "logger.minutes_eac3_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_eac3_log_ts"},
    {msgid = 0xE31F8B17, idx = 793, Name = "prim_sm.Uzk_pump_grad[0]",                         DataType = t_float,   Desc = "start power [W]"},
    {msgid = 0xE3F4D1DF, idx = 794, Name = "acc_conv.i_max",                                   DataType = t_float,   Desc = "Max. battery converter current [A]"},
    {msgid = 0xE49BE3ED, idx = 795, Name = "nsm.pf_rise_grad",                                 DataType = t_float,   Desc = "Power increase gradient after P(f) restriction [P/(Pn*s)]"},
    {msgid = 0xE4DC040A, idx = 796, Name = "logger.month_eext_log_ts",                         DataType = t_log_ts,  Desc = "logger.month_eext_log_ts"},
    {msgid = 0xE52B89FA, idx = 798, Name = "io_board.home_relay_off_threshold",                DataType = t_float,   Desc = "Switching off threshold [W]"},
    {msgid = 0xE5FBCC6F, idx = 799, Name = "logger.year_eload_log_ts",                         DataType = t_log_ts,  Desc = "logger.year_eload_log_ts"},
    {msgid = 0xE6248312, idx = 800, Name = "hw_test.bt_power[8]",                              DataType = t_float,   Desc = "hw_test.bt_power[8]"},
    {msgid = 0xE635A6C4, idx = 801, Name = "battery_placeholder[0].module_sn[2]",              DataType = t_string,  Desc = "Module 2 Serial Number"},
    {msgid = 0xE63A3529, idx = 802, Name = "flash_result",                                     DataType = t_uint16,  Desc = "Flash result"},
    {msgid = 0xE6F1CB83, idx = 803, Name = "nsm.pu_ts",                                        DataType = t_float,   Desc = "Time const for filter [s]"},
    {msgid = 0xE7177DEE, idx = 804, Name = "battery.cells_stat[2].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[2].u_max.value"},
    {msgid = 0xE7B0E692, idx = 805, Name = "battery.bat_impedance.impedance_fine",             DataType = t_float,   Desc = "Battery circuit impedance"},
    {msgid = 0xE87B1F4B, idx = 806, Name = "battery_placeholder[0].cells_stat[0].u_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[0].u_min.value"},
    {msgid = 0xE94C2EFC, idx = 807, Name = "g_sync.q_ac[0]",                                   DataType = t_float,   Desc = "Reactive power phase 1 [var]"},
    {msgid = 0xE952FF2D, idx = 808, Name = "nsm.q_u_max_u_low_rel",                            DataType = t_float,   Desc = "Qmax at lower voltage level relative to Smax (positive = overexcited)"},
    {msgid = 0xE96F1844, idx = 809, Name = "io_board.s0_external_power",                       DataType = t_float,   Desc = "io_board.s0_external_power"},
    {msgid = 0xE9BBF6E4, idx = 810, Name = "power_mng.amp_hours_measured",                     DataType = t_float,   Desc = "Measured battery capacity [Ah]"},
    {msgid = 0xEA399EA8, idx = 811, Name = "battery_placeholder[0].min_cell_voltage",          DataType = t_float,   Desc = "battery_placeholder[0].min_cell_voltage"},
    {msgid = 0xEA77252E, idx = 812, Name = "battery.minimum_discharge_voltage_constant_u",     DataType = t_float,   Desc = "Min. discharge voltage [V]"},
    {msgid = 0xEAEEB3CA, idx = 813, Name = "energy.e_dc_month_sum[0]",                         DataType = t_float,   Desc = "energy.e_dc_month_sum[0]"},
    {msgid = 0xEB4C2597, idx = 814, Name = "battery.cells_resist[6]",                          DataType = t_string,  Desc = "battery.cells_resist[6]"},
    {msgid = 0xEB7773BF, idx = 815, Name = "nsm.p_u[1][1]",                                    DataType = t_float,   Desc = "Point 2 voltage [V]"},
    {msgid = 0xEB7BCB93, idx = 816, Name = "battery_placeholder[0].bms_sn",                    DataType = t_string,  Desc = "BMS Serial Number"},
    {msgid = 0xEBC62737, idx = 817, Name = "android_description",                              DataType = t_string,  Desc = "Device name"},
    {msgid = 0xEBF7A4E8, idx = 818, Name = "grid_mon[0].f_over.threshold",                     DataType = t_float,   Desc = "Max. frequency level 1 [Hz]"},
    {msgid = 0xECABB6CF, idx = 819, Name = "switch_on_cond.test_time",                         DataType = t_float,   Desc = "Test time"},
    {msgid = 0xEE049B1F, idx = 820, Name = "nsm.pf_hysteresis",                                DataType = t_bool,    Desc = "Hysteresis mode"},
    {msgid = 0xEEA3F59B, idx = 821, Name = "battery.stack_software_version[5]",                DataType = t_uint32,  Desc = "Software version stack 5"},
    {msgid = 0xEEC44AA0, idx = 822, Name = "battery_placeholder[0].cells_stat[2].u_min.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[2].u_min.index"},
    {msgid = 0xEECDFEFC, idx = 823, Name = "battery.cells_stat[2].u_min.value",                DataType = t_float,   Desc = "battery.cells_stat[2].u_min.value"},
    {msgid = 0xEF89568B, idx = 824, Name = "grid_mon[0].u_under.time",                         DataType = t_float,   Desc = "Min. voltage switch-off time level 1 [s]"},
    {msgid = 0xEFD3EC8A, idx = 825, Name = "battery.cells_stat[5].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[5].t_min.time"},
    {msgid = 0xEFF4B537, idx = 826, Name = "energy.e_load_total",                              DataType = t_float,   Desc = "Household total energy [Wh]"},
    {msgid = 0xF03133E2, idx = 827, Name = "partition[0].last_id",                             DataType = t_int32,   Desc = "partition[0].last_id"},
    {msgid = 0xF044EDA0, idx = 828, Name = "battery.cells_stat[3].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[3].t_max.value"},
    {msgid = 0xF0527539, idx = 829, Name = "db.power_board.adc_p3V3_meas",                     DataType = t_float,   Desc = "db.power_board.adc_p3V3_meas"},
    {msgid = 0xF09CC4A2, idx = 830, Name = "grid_mon[1].u_over.time",                          DataType = t_float,   Desc = "Max. voltage switch-off time level 2 [s]"},
    {msgid = 0xF0A03A20, idx = 831, Name = "bat_mng_struct.k",                                 DataType = t_float,   Desc = "Forecast correction"},
    {msgid = 0xF0B436DD, idx = 832, Name = "g_sync.p_ac_load[2]",                              DataType = t_float,   Desc = "Load household phase 3 [W]"},
    {msgid = 0xF0BE6429, idx = 833, Name = "energy.e_load_month",                              DataType = t_float,   Desc = "Household month energy [Wh]"},
    {msgid = 0xF1342795, idx = 834, Name = "power_mng.stop_discharge_current",                 DataType = t_float,   Desc = "Stop discharge current [A]"},
    {msgid = 0xF168B748, idx = 835, Name = "power_mng.soc_strategy",                           DataType = t_enum,    Desc = "SOC target selection"},
    {msgid = 0xF1DE6E99, idx = 836, Name = "battery_placeholder[0].cells_resist[3]",           DataType = t_string,  Desc = "battery_placeholder[0].cells_resist[3]"},
    {msgid = 0xF1FA5BB9, idx = 837, Name = "grid_mon[1].f_under.time",                         DataType = t_float,   Desc = "Min. frequency switch-off time level 2 [s]"},
    {msgid = 0xF23D4595, idx = 838, Name = "battery_placeholder[0].cells_stat[1].t_min.value", DataType = t_float,   Desc = "battery_placeholder[0].cells_stat[1].t_min.value"},
    {msgid = 0xF2405AC6, idx = 839, Name = "nsm.p_limit",                                      DataType = t_float,   Desc = "Max. grid power [W]"},
    {msgid = 0xF247BB16, idx = 840, Name = "display_struct.contrast",                          DataType = t_uint8,   Desc = "Display contrast"},
    {msgid = 0xF25591AA, idx = 841, Name = "nsm.cos_phi_p[3][0]",                              DataType = t_float,   Desc = "Point 4 [P/Pn]"},
    {msgid = 0xF257D342, idx = 842, Name = "battery.cells_stat[1].t_max.value",                DataType = t_float,   Desc = "battery.cells_stat[1].t_max.value"},
    {msgid = 0xF25C339B, idx = 843, Name = "g_sync.u_ptp_rms[2]",                              DataType = t_float,   Desc = "Phase to phase voltage 3 [V]"},
    {msgid = 0xF28341E2, idx = 844, Name = "logger.month_eac_log_ts",                          DataType = t_log_ts,  Desc = "logger.month_eac_log_ts"},
    {msgid = 0xF2BE0C9C, idx = 845, Name = "p_buf_available",                                  DataType = t_float,   Desc = "Available buffer power [W]"},
    {msgid = 0xF393B7B0, idx = 846, Name = "power_mng.calib_charge_power",                     DataType = t_float,   Desc = "Calibration charge power [W]"},
    {msgid = 0xF3FD6C4C, idx = 847, Name = "nsm.pf_use_p_max",                                 DataType = t_bool,    Desc = "By over-frequency in P(f) use Pmax instead of Pmom (instant P)."},
    {msgid = 0xF3FD8CE6, idx = 848, Name = "battery.cells_resist[2]",                          DataType = t_string,  Desc = "battery.cells_resist[2]"},
    {msgid = 0xF42D4DD0, idx = 849, Name = "io_board.alarm_home_value",                        DataType = t_enum,    Desc = "Evaluated value"},
    {msgid = 0xF451E935, idx = 850, Name = "battery_placeholder[0].cells_stat[0].t_min.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[0].t_min.time"},
    {msgid = 0xF473BC5E, idx = 851, Name = "buf_v_control.power_reduction_max_solar_grid",     DataType = t_float,   Desc = "Max. allowed grid feed-in power [W]"},
    {msgid = 0xF49F58F2, idx = 852, Name = "nsm.p_u[2][1]",                                    DataType = t_float,   Desc = "Point 3 voltage [V]"},
    {msgid = 0xF52C0B50, idx = 853, Name = "power_mng.schedule[7]",                            DataType = t_string,  Desc = "power_mng.schedule[7]"},
    {msgid = 0xF54BC06D, idx = 854, Name = "battery.cells_stat[4].u_max.value",                DataType = t_float,   Desc = "battery.cells_stat[4].u_max.value"},
    {msgid = 0xF5584F90, idx = 855, Name = "g_sync.p_ac_sc[1]",                                DataType = t_float,   Desc = "Grid power phase 2 [W]"},
    {msgid = 0xF644DCA7, idx = 856, Name = "bat_mng_struct.k_reserve",                         DataType = t_float,   Desc = "Main reservation coefficient [0..2]"},
    {msgid = 0xF677D737, idx = 857, Name = "battery_placeholder[0].cells_stat[6].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[6].u_max.time"},
    {msgid = 0xF68ECC1F, idx = 858, Name = "battery_placeholder[0].cells_stat[1].u_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[1].u_max.time"},
    {msgid = 0xF6A85818, idx = 859, Name = "nsm.f_entry",                                      DataType = t_float,   Desc = "Entry frequency for P(f) over-frequency mode [Hz]"},
    {msgid = 0xF742C6BA, idx = 860, Name = "battery_placeholder[0].cells_stat[1].u_max.index", DataType = t_uint8,   Desc = "battery_placeholder[0].cells_stat[1].u_max.index"},
    {msgid = 0xF76DE445, idx = 861, Name = "logger.minutes_temp_log_ts",                       DataType = t_log_ts,  Desc = "logger.minutes_temp_log_ts"},
    {msgid = 0xF79D41D9, idx = 862, Name = "db.temp1",                                         DataType = t_float,   Desc = "Heat sink temperature [°C]"},
    {msgid = 0xF87A2A1E, idx = 863, Name = "dc_conv.last_rescan",                              DataType = t_uint32,  Desc = "Last global rescan"},
    {msgid = 0xF8C0D255, idx = 864, Name = "battery.cells[0]",                                 DataType = t_string,  Desc = "battery.cells[0]"},
    {msgid = 0xF8DECCE6, idx = 865, Name = "wifi.connected_ap_ssid",                           DataType = t_string,  Desc = "WiFi associated AP"},
    {msgid = 0xF99E8CC8, idx = 866, Name = "battery.cells_stat[6]",                            DataType = t_string,  Desc = "battery.cells_stat[6]"},
    {msgid = 0xF9FD0D61, idx = 867, Name = "wifi.service_ip",                                  DataType = t_string,  Desc = "wifi.service_ip"},
    {msgid = 0xFA3276DC, idx = 868, Name = "battery.cells_stat[3].t_min.time",                 DataType = t_uint32,  Desc = "battery.cells_stat[3].t_min.time"},
    {msgid = 0xFA7DB323, idx = 869, Name = "io_board.check_s0_result",                         DataType = t_uint16,  Desc = "io_board.check_s0_result"},
    {msgid = 0xFAA837C8, idx = 870, Name = "nsm.f_low_rise_grad",                              DataType = t_float,   Desc = "Power rise gradient for P(f) under-frequency mode without battery [1/Pn*Hz]"},
    {msgid = 0xFAE429C5, idx = 871, Name = "rb485.f_grid[1]",                                  DataType = t_float,   Desc = "Grid phase 2 frequency [Hz]"},
    {msgid = 0xFB57BA65, idx = 872, Name = "bat_mng_struct.count",                             DataType = t_string,  Desc = "bat_mng_struct.count"},
    {msgid = 0xFB5DE9C5, idx = 873, Name = "prim_sm.minigrid_flag",                            DataType = t_bool,    Desc = "Minigrid support"},
    {msgid = 0xFB796780, idx = 874, Name = "battery.cells_stat[1]",                            DataType = t_string,  Desc = "battery.cells_stat[1]"},
    {msgid = 0xFBD94C1F, idx = 875, Name = "power_mng.amp_hours",                              DataType = t_float,   Desc = "Battery energy [Ah]"},
    {msgid = 0xFBF3CE97, idx = 876, Name = "energy.e_dc_day[1]",                               DataType = t_float,   Desc = "Solar generator B day energy [Wh]"},
    {msgid = 0xFBF6D834, idx = 877, Name = "battery.module_sn[0]",                             DataType = t_string,  Desc = "Module 0 Serial Number"},
    {msgid = 0xFBF8D63C, idx = 878, Name = "energy.e_grid_load_day_sum",                       DataType = t_float,   Desc = "energy.e_grid_load_day_sum"},
    {msgid = 0xFC1C614E, idx = 879, Name = "energy.e_ac_month_sum",                            DataType = t_float,   Desc = "energy.e_ac_month_sum"},
    {msgid = 0xFC1F8C65, idx = 880, Name = "battery_placeholder[0].cells_stat[6].t_max.time",  DataType = t_uint32,  Desc = "battery_placeholder[0].cells_stat[6].t_max.time"},
    {msgid = 0xFC5AA529, idx = 881, Name = "bat_mng_struct.bat_calib_soc_threshold",           DataType = t_float,   Desc = "SOC threshold for battery calibration in advance"},
    {msgid = 0xFC724A9E, idx = 882, Name = "energy.e_dc_total[0]",                             DataType = t_float,   Desc = "Solar generator A total energy [Wh]"},
    {msgid = 0xFCA1CBB5, idx = 883, Name = "battery_placeholder[0].voltage",                   DataType = t_float,   Desc = "Battery voltage [V]"},
    {msgid = 0xFCC39293, idx = 884, Name = "nsm.rpm_lock_in_power",                            DataType = t_float,   Desc = "Reactive Power Mode lock-in power [P/Pn]"},
    {msgid = 0xFCF4E78D, idx = 885, Name = "logger.day_ea_log_ts",                             DataType = t_log_ts,  Desc = "logger.day_ea_log_ts"},
    {msgid = 0xFD4F17C4, idx = 886, Name = "grid_mon[1].f_over.time",                          DataType = t_float,   Desc = "Max. frequency switch-off time level 2 [s]"},
    {msgid = 0xFD72CC0D, idx = 887, Name = "frt.enabled",                                      DataType = t_bool,    Desc = "Enable FRT"},
    {msgid = 0xFDB81124, idx = 888, Name = "energy.e_grid_feed_day_sum",                       DataType = t_float,   Desc = "energy.e_grid_feed_day_sum"},
    {msgid = 0xFDBD9EE9, idx = 889, Name = "battery.cells_stat[3].u_max.index",                DataType = t_uint8,   Desc = "battery.cells_stat[3].u_max.index"},
    {msgid = 0xFE1AA500, idx = 890, Name = "buf_v_control.power_reduction",                    DataType = t_float,   Desc = "External power reduction based on solar plant peak power [0..1]"},
    {msgid = 0xFE38B227, idx = 891, Name = "battery_placeholder[0].cells_stat[5]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[5]"},
    {msgid = 0xFE44BA26, idx = 892, Name = "battery.cells_stat[0].u_min.index",                DataType = t_uint8,   Desc = "battery.cells_stat[0].u_min.index"},
    {msgid = 0xFED51BD2, idx = 893, Name = "dc_conv.dc_conv_struct[1].enabled",                DataType = t_bool,    Desc = "Solar generator B connected"},
    {msgid = 0xFF2A258B, idx = 894, Name = "wifi.server_ip",                                   DataType = t_string,  Desc = "wifi.server_ip"},
    {msgid = 0xFF5B8A54, idx = 895, Name = "battery_placeholder[0].cells_stat[3]",             DataType = t_string,  Desc = "battery_placeholder[0].cells_stat[3]"},
}

function rct_entry_name(entry)
    if entry == nil then
        return "unknown"
    end

    return entry.Name
end

function rct_find_entry(id)
    --id = id:get_index(0) * 0x1000000 + id:get_index(1) * 0x10000 + id:get_index(2) * 0x100 + id:get_index(3) 
    for key,entry in ipairs(rct_id) do
        if entry.msgid == id then
            return entry
        end
    end

    return nil
end