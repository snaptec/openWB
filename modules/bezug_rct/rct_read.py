#!/usr/bin/python
import sys
import rct
import fnmatch


# Entry point with parameter check
def main():
    rct.init(sys.argv)

    clientsocket = rct.connect_to_server()
    if clientsocket is not None:
        fmt = '#0x{:08X} {:'+str(rct.param_len)+'}'  # {:'+str(rct.desc_len)+'}:'
        for obj in rct.id_tab:
            if rct.search_id > 0 and obj.id != rct.search_id:
                continue

            if rct.search_name is not None and fnmatch.fnmatch(obj.name, rct.search_name) is False:
                continue

            value = rct.read(clientsocket, obj.id)
            if rct.dbglog(fmt.format(obj.id, obj.name), value) is False:
                print(value)
        rct.close(clientsocket)
    sys.exit(0)


if __name__ == "__main__":
    main()
