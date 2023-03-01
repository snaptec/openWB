import time

import parameters
import soclogging
import state


def ackExternalTrigger():
    try:
        f = open(parameters.getParameter('timerFile'), 'w')
        f.write(str(0))
        f.close()
    except:
        raise

    return


def ackTimerTrigger():
    try:
        now = int(time.time())
        state.setState('lastRun', now)
    except:
        raise

    return


def isExternalTriggered():
    trigger = 0

    try:
        f = open(parameters.getParameter('timerFile'), 'r')
        ticksLeft = int(f.read())
        f.close()
    except:
        ticksLeft = 0
        pass

    if ticksLeft > 0:
        trigger = 1
        soclogging.logDebug(1, "SoC download triggered externally")

    return trigger


def isMinimumTimerExpired():
    now = int(time.time())
    secSince = now - state.getState('lastRun')

    if secSince < parameters.getParameter('timerMinInterval'):
        trigger = 0
    else:
        trigger = 1

    return trigger


def isTimerExpired():
    now = int(time.time())

    if state.isPlugged() == 1:
        secLeft = (state.getState('lastRun') + (parameters.getParameter('timerInterval') * 60)) - now
    else:
        secLeft = (state.getState('lastRun') + (parameters.getParameter('timerIntervalUnplug') * 60)) - now

    if secLeft < 0:
        trigger = 1
        soclogging.logDebug(1, "SoC download triggered by timer")
    else:
        trigger = 0
        soclogging.logDebug(2, "Next Update: " + '{:.1f}'.format(secLeft / 60) + " minutes")

    return trigger


def isDownloadTriggered():
    trigger = 0
    external = 0

    try:
        if isExternalTriggered() == 1:
            ackExternalTrigger()
            soclogging.logDebug(1, "Manual update or charge starts")
            trigger = 1
            external = 1
        elif isTimerExpired() == 1:
            trigger = 1
        else:
            trigger = 0

        if trigger == 1:
            if isMinimumTimerExpired() == 1:
                ackTimerTrigger()
                trigger = 1
            elif external == 1:
                trigger = 1
            else:
                soclogging.logDebug(1, "Last Download less then " + '{:.0f}'.format(
                    parameters.getParameter('timerMinInterval') / 60) + " minutes ago. Cancelling download")
                trigger = 0

        if trigger == 1:
            if (state.getState('charged') == 0) and (state.getState('unplug') == 0) and (external == 0):
                trigger = 0
                soclogging.logDebug(1, "Vehicle was not unplugged or charging since last download. Cancelling download")

    except:
        raise

    return trigger
