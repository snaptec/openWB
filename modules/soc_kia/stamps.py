import time

import parameters

import stamps_kia
import stamps_hyundai

def getStamp():
    now = int(time.time())
    stamp = ""
    brand = parameters.getParameter('brand')
    
    try:
        if brand == 'kia':
            index = max(min(int((now - stamps_kia.start) / stamps_kia.step) - 1,len(stamps_kia.stamps) - 1), 0)
            stamp = stamps_kia.stamps[index]
        
        if brand == 'hyundai':
            index = max(min(int((now - stamps_hyundai.start) / stamps_hyundai.step) - 1,len(stamps_hyundai.stamps) - 1), 0)
            stamp = stamps_hyundai.stamps[index]
    except:
        raise
        
    if stamp == "":
        raise
    
    return stamp