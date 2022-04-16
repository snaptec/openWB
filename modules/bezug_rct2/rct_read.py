#!/usr/bin/python3
from typing import List
import os, sys, traceback, time, fnmatch
try: # make script callable from command line and LRS
    from bezug_rct2 import rct_lib
except:
    import rct_lib

# Entry point with parameter check
def main(argv: List[str]):
    start_time = time.time()
    rct = rct_lib.RCT(argv)

    if rct.connect_to_server() == True:
        try:
            MyTab = []
            for obj in rct.id_tab:
                if rct.search_id > 0 and obj.id != rct.search_id:
                    continue

                if rct.search_name is not None and fnmatch.fnmatch(obj.name, rct.search_name) is False:
                    continue

                rct.add_by_id(MyTab, obj.id)

            response = rct.read(MyTab)
            rct.close()

            # debug output of processing time and all response elements
            rct.dbglog(response.format_list(time.time() - start_time))
        except:
            print("-"*100)
            traceback.print_exc(file=sys.stdout)
            rct.close()

    rct = None

if __name__ == "__main__":
    main(sys.argv[1:])
