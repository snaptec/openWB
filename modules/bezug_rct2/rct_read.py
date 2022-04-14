#!/usr/bin/python3
import fnmatch
import sys, traceback
import time
from typing import List
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
            rct.dbglog("Overall processing time: {:.3f} seconds".format(time.time() - start_time))
            rct.dbglog(response.format_list())
        except:
            print("-"*100)
            traceback.print_exc(file=sys.stdout)
            rct.close()

    rct = None

if __name__ == "__main__":
    main(sys.argv[1:])
