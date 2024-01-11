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
            appid = "1518dd6b-2759-4995-9ae5-c9ad4a9ddad1"
            secret_ba = bytearray.fromhex("C0B4D5C7089D987F027C96015929C70FA9D2B2AA99530CFD017E4B243C4BA5C5DED96DEB128EEB5DD3963DFC12432C9073EF")

        if brand == 'hyundai':
            appid = "014d2225-8495-4735-812d-2616334fd15d"
            secret_ba = bytearray.fromhex("445B6846AFEF0D726646776865A650C9F3A8B7B3AB22A195163F7A898D962F7CB21F967FA54BE5521AA60B10F6B7E0FADC3B")
    
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
