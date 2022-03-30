#!/usr/bin/python3
import sys
import time
import rct_lib
import fnmatch


# Entry point with parameter check
def main():
    start_time = time.time()
    rct_lib.init(sys.argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:
        try:
            MyTab = []
            for obj in rct_lib.id_tab:
                if rct_lib.search_id > 0 and obj.id != rct_lib.search_id:
                    continue

                if rct_lib.search_name is not None and fnmatch.fnmatch(obj.name, rct_lib.search_name) is False:
                    continue

                rct_lib.add_by_id(MyTab, obj.id)

            response = rct_lib.read(clientsocket, MyTab)
            rct_lib.close(clientsocket)

            # output all response elements
            rct_lib.dbglog("Overall access time: {:.3f} seconds".format(time.time() - start_time))
            rct_lib.dbglog(rct_lib.format_list(response))
        except Exception as e:
            rct_lib.close(clientsocket)
            raise(e)

if __name__ == "__main__":
    main()
