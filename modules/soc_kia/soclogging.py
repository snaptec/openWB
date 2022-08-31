from datetime import datetime

import parameters


def logDebug(msgLevel, msgText):
    if parameters.getParameter('debugLevel') >= msgLevel:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        line = timestamp + ": " + msgText + "\n"

        f = open(parameters.getParameter('logFile'), 'a')
        f.write(line)
        f.close()

    return
