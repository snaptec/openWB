####
# Modul: Awattar Hourly Cap
# Berechnet den SYNC-Bonus des Awattar Hourly-Cap Tarifs für Deutschland aus den stündlichen Preisen
#
# ToDo:
# - Feiertagserkennung (müssen wie Sonntage behandelt werden)
# - 23/25-Stunden-Tage
####

# --- Imports ---

from datetime import datetime, timedelta, time
import json
import requests
import os
import sys

import factors

# --- Globale Variablen ---

debug = 0
priceFileToday = "/var/www/html/openWB/ramdisk/et_price_d0"
priceFileTomorrow = "/var/www/html/openWB/ramdisk/et_price_d1"
curveFile = "/var/www/html/openWB/ramdisk/etprovidergraphlist"
currentFile = "/var/www/html/openWB/ramdisk/etproviderprice"
priceUrl = "https://api.awattar.de/v1/marketdata?start="

# --- Helper-Funktionen ---

def logDebug(msgLevel, msgText):
    try:
        if debug >= msgLevel:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            line = timestamp + ": " + str(msgText) + "\n"
            with open('/var/www/html/openWB/ramdisk/openWB.log', 'a') as f:
                f.write(line)
    except:
        pass
        
    return
    
def getWeekday(time):
    # 0=Montag,...,6=Sonntag
    dow = datetime.fromtimestamp(time).weekday()
    
    return dow
    
def getSeason(time):
    # 0=Sommer, 1=Winter, 2=Übergang
    month = datetime.fromtimestamp(time).month
    day = datetime.fromtimestamp(time).month
    
    if ((month == 5) and (day >= 15)) or (month == 6) or (month == 7) or (month == 8) or ((month == 9) and (day < 15)):
        season = 0
    elif (month == 11) or (month == 12) or (month == 1) or (month == 2) or ((month == 3) and (day < 21)):
        season = 1
    elif ((month == 3) and (day >= 21)) or (month == 4) or ((month == 5) and (day < 15)):
        season = 2
    elif ((month == 9) and (day >= 15)) or (month == 10):
        season = 2
    else:
        raise ValueError
    
    return season
   
# --- Funktionen ---

def checkPrices(fileName, time):
    try:
        data = loadPrices(fileName)
        fileTime = data['data'][0]['start_timestamp']
    except:
        return False
    
    if fileTime == (time * 1000):
        return True
    
    return False

def downloadPrices(time):
    try:
        url = priceUrl + str(time) + "000"
        jsond = requests.get(url, allow_redirects = True)
        data = json.loads(jsond.text)
    except:
        return 0
    
    return data

def loadPrices(fileName):
    try:
        with open(fileName, 'r') as f:
            data = json.loads(f.read())
    except:
        return 0
    
    return data
    
def savePrices(fileName, data):
    try:
        with open(fileName, 'w') as f:
            f.write(json.dumps(data))
    except:
        return
    
    return
    
def calculateCurve(data, time):   
    try:
        season = getSeason(time)
        weekday = getWeekday(time)
        avgprice = 0
        pricecurve = {}
        
        for hour in range(24):
            factor = factors.getFactor(season, weekday, hour)
            hourprice = float(data['data'][hour]['marketprice'])
            avgprice = avgprice + (factor * hourprice)
            
        for hour in range(24):
            hourprice = data['data'][hour]['marketprice']
            pricecurve[hour] = round(((hourprice - avgprice) * 1.19) / 10, 2)        
    except:
        raise
        
    return pricecurve

def savePriceCurve(curve1, curve2, time1, time2):
    try:    
        with open(curveFile, 'w') as f: 
            f.write("awattarcap_de\n")
            for hour in range(datetime.now().hour, 24):
                f.write(str(time1 + (hour*60*60)) + "," + str(curve1[hour]) + "\n") 
            for hour in range(24):
                f.write(str(time2 + (hour*60*60)) + "," + str(curve2[hour]) + "\n")     
    except:
        raise
        
    return
    
def saveCurrentPrice(curve1, time1):
    try:
        with open(currentFile, 'w') as f:    
            f.write(str(curve1[datetime.now().hour])) 
    except:
        raise
        
    return
        
def publishPrices():
    os.system('mosquitto_pub -r -t openWB/global/awattar/pricelist -m "$(cat ' + curveFile + ')"')
    os.system('mosquitto_pub -r -t openWB/global/awattar/ActualPriceForCharging -m "$(cat ' + currentFile + ')"')
    return
        
# --- Hauptprogramm --

def main():
    try:
        debug = int(sys.argv[1])
        timeToday = int(datetime.combine(datetime.today(), time.min).timestamp())
        timeTomorrow = int(timeToday + (24*60*60))
    except:
        raise
    
    try:
        if checkPrices(priceFileToday, timeToday):
            dataToday = loadPrices(priceFileToday)
        else:
            dataToday = downloadPrices(timeToday)
            savePrices(priceFileToday, dataToday)
        
        curveToday = calculateCurve(dataToday, timeToday)
    except:
        curveToday = {}
        for hour in range(24):
            curveToday[hour] = 0
        pass
    
    try:
        if checkPrices(priceFileTomorrow, timeTomorrow):
            dataTomorrow = loadPrices(priceFileTomorrow)
        else:
            dataTomorrow = downloadPrices(timeTomorrow)
            savePrices(priceFileTomorrow, dataTomorrow)
            
        curveTomorrow = calculateCurve(dataTomorrow, timeTomorrow)
    except:
        curveTomorrow = {}
        for hour in range(24):
            curveTomorrow[hour] = 0
        pass
        
    try:
        savePriceCurve(curveToday, curveTomorrow, timeToday, timeTomorrow)
        saveCurrentPrice(curveToday, timeToday)
        publishPrices()
    except:
        raise
        
    exit(0)

if __name__ == '__main__':
    main()