import teslajson
import json
import sys
usern = str(sys.argv[1])
passw = str(sys.argv[2])
carnumb = int(sys.argv[3])

c = teslajson.Connection(usern, passw)
v = c.vehicles[carnumb]
v.wake_up()
result = v.data_request('charge_state')
newr = json.dumps(result)
print newr

