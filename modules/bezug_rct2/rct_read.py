#!/usr/bin/python3
import sys
import rct_lib
import fnmatch
#  date --date @1631599500 +"%d.%m.%Y %H:%M"


# Entry point with parameter check
def main():
    rct_lib.init(sys.argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:
        fmt = '#0x{:08X} {:'+str(rct_lib.param_len)+'}'# {:'+str(rct_lib.desc_len)+'}:'
        for obj in rct_lib.id_tab:
            if rct_lib.search_id > 0 and obj.id != rct_lib.search_id:
                #rct_lib.dbglog( obj.id, obj.name)
                continue
            
            if rct_lib.search_name is not None and fnmatch.fnmatch(obj.name, rct_lib.search_name) == False:
                continue
            
            value = rct_lib.read(clientsocket, obj.id)

            if rct_lib.dbglog(fmt.format(obj.id, obj.name), value) == False:
                print( value )

        rct_lib.close(clientsocket)

    sys.exit(0)
    
if __name__ == "__main__":
    main()
