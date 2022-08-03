import time
import json

import parameters

stateDict = {}


def getState(key):
    global stateDict

    try:
        f = open(parameters.getParameter('stateFile'), 'r')
        stateStr = f.read()
        stateDict = json.loads(stateStr)
        f.close()

        value = stateDict[key]
    except:
        value = 0

        if key == 'lastTick':
            value = 0
        if key == 'lastRun':
            value = 0
        if key == 'lastSoc':
            value = 0
        if key == 'lastMeter':
            value = 0
        if key == 'charged':
            value = 1
        if key == 'unplug':
            value = 1
        if key == 'lastSuccess':
            value = 1

        pass

    return value


def setState(key, value):
    global stateDict

    try:
        f = open(parameters.getParameter('stateFile'), 'r')
        stateStr = f.read()
        stateDict = json.loads(stateStr)
        f.close()
    except:
        pass

    stateDict[key] = value

    try:
        f = open(parameters.getParameter('stateFile'), 'w')
        stateStr = json.dumps(stateDict)
        f.write(stateStr)
        f.close()
    except:
        raise

    return


def isCharging():
    try:
        f = open(parameters.getParameter('isChargingFile'), 'r')
        chargeState = int(f.read())
        f.close()
    except:
        raise

    return chargeState


def isPlugged():
    try:
        f = open(parameters.getParameter('isPluggedFile'), 'r')
        plugState = int(f.read())
        f.close()
    except:
        raise

    return plugState


def saveUnplugState():
    try:
        now = int(time.time())
        secsSinceLastTick = now - getState('lastTick')

        if (isPlugged() == 0) or (secsSinceLastTick > 60):
            setState('unplug', 1)

    except:
        raise

    return


def saveChargedState():
    try:
        if isCharging() == 1:
            setState('charged', 1)
    except:
        raise

    return


def saveTickTime():
    try:
        now = int(time.time())
        setState('lastTick', now)
    except:
        raise

    return
