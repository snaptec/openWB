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
            appid = "e7bcd186-a5fd-410d-92cb-6876a42288bd"
            secret_ba = bytearray.fromhex("C0B4D5C7089D987F027C96015929C70FCE5B94FC9AE938CA6EE1E02F6142AFE2A1F20C7EB9C902C93E56EE1E0D81B9F7CEA3")

        if brand == 'hyundai':
            appid = "014d2225-8495-4735-812d-2616334fd15d"
            secret_ba = bytearray.fromhex("445B6846AFEF0D726646776865A650C9F3A8B7B3AB22A195163F7A898D962F7CB21F967FA54BE5521AA60B10F6B7E0FA89E1")
    
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
