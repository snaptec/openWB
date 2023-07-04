import base64
import time

import parameters


def getStamp():
    try:
        # Timestamp in ms an string
        now = str(int(time.time()) * 1000)
        
        # Set App-ID and App-ID specific key
        brand = parameters.getParameter('brand')
        if brand == 'kia':
            appid = "a2b8469b-30a3-4361-8e13-6fceea8fbe74"
            secret_ba = bytearray.fromhex("C0B4D5C7089D987F027C96015929C70FA13486E934A33762BB2801E212E43395C283300BD43939B04DFA77F6F1E4F14C6D9B")

        if brand == 'hyundai':
            appid = "1eba27d2-9a5b-4eba-8ec7-97eb6c62fb51"
            secret_ba = bytearray.fromhex("445B6846AFEF0D726646776865A650C9AEF98E51A474DCB7EC9B1B67D29C66EAAEF621CA02522A0B80A8087F7A3A7BB0F71B")
    
        # Combine plaintext and convert to bytearray
        plaintext = appid + ":" + now
        plaintext_ba = bytearray(plaintext.encode())
    
        # XOR plaintext and key
        stamp_ba = bytes(a ^ b for (a, b) in zip(plaintext_ba, secret_ba))
    
        # Convert result to base64-string
        stamp_b64_ba = base64.b64encode(stamp_ba)
        stamp = stamp_b64_ba.decode()
        
    except:
        raise

    return stamp
