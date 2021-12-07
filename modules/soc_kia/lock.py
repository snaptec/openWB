import time

import parameters

def checkLockFile():
    
    try:
        f = open(parameters.getParameter('lockFile'), 'r')
        lockTime = int(f.read())
        f.close()
    except:
        lockTime = 0
        
    now = time.time()
    if lockTime > (now - 10*60):
        raise RuntimeError
        
    return

def createLockFile():
  
    try:
        f = open(parameters.getParameter('lockFile'), 'w')
        f.write(str(int(time.time())))
        f.close()
    except:
        raise
        
    return

def purgeLockFile():
    
    try:
        f = open(parameters.getParameter('lockFile'), 'w')
        f.write(str(0))
        f.close()
    except:
        raise
        
    return