#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import csv
import argparse

def outfiledefyear(jjjjinput):
    if (str(jjjjinput) == str(aktjjjj)):
    # heutiges Jahr nachgerechnet, ramdisk nehmen
        file_stringo =  outputa + 'logaktyearonl.csv'
        file_stringos =  outputa + 'logaktyearonls.csv'
    else:
        file_stringo =  outputp + str(jjjjinput) + 'onl.csv'
        file_stringos =  outputp + str(jjjjinput) + 'onls.csv'
    return (file_stringo,file_stringos)
def outfiledef(jjjjmminput):
    if (str(jjjjmminput) == str(aktjjjjmm)):
    # heutiger Monat nachgerechnet, ramdisk nehmen
        file_stringo =  outputa + 'logaktmonthonl.csv'
        file_stringos =  outputa + 'logaktmonthonls.csv'
    else:
        file_stringo =  outputp + str(jjjjmminput) + 'onl.csv'
        file_stringos =  outputp + str(jjjjmminput) + 'onls.csv'
    return (file_stringo,file_stringos)
def exceldate(datestring):
    datestringexcel =  datestring[-2:]  + '.' + datestring[4:6] + '.' + datestring[:4]
    return datestringexcel
def prep():
    global headerst
    headerst = 'Datum,'
    for i in range (1,SUMCOLUMNSTART*2):
        if (i <= SUMCOLUMNSTART ):
            if i < len(header):
                headerst=str(headerst) + 'Z-' + str(header[i]) + ','
            else:
                headerst=headerst + ' ,'
        else:
            if (i-SUMCOLUMNSTART) < len(header):
                headerst=headerst +  header[i-SUMCOLUMNSTART]
            if (i-SUMCOLUMNSTART) < (len(header)-1):
                headerst=headerst + ','
    headerst=headerst + '\n'
    return

def getTime():
    named_tuple = time.localtime() # getstruct_time
    return time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

def trdaymonth(irow):
    inputrow = []
    # Kopie erzwingen,
    if (len(irow) > SUMCOLUMNSTART):
        inputrow = irow[:]
    else:
        for i in range(1,SUMCOLUMNSTART):
            if (i-1) < len(irow):
                inputrow.append(irow[i-1])
            else:
                inputrow.append( float(0) )
    row = inputrow [:]
    #	Monatlich_________	Seq	PosT	Tag
    #
    #	$bezug___________	1	1	$bezug
    #	$einspeisung_____	2	2	$einspeisung
    #	$pv______________	3	3	$pv
    #	$ll1_____________	4	4	$ll1
    #	$ll2_____________	5	5	$ll2
    #	$ll3_____________	6	6	$ll3
    #	$llg_____________	7	7	$llg
    #   $verbraucher1iwh_	8	10	$speicheri
    #	$verbraucher1ewh_	9	11	$speichere
    #	$verbraucher2iwh_	10	12	$verbraucher1
    #	$verbraucher2ewh_	11	13	$verbrauchere1
    #	$ll4_____________	12	15	$verbraucher2
    #	$ll5_____________	13	16	$verbrauchere2
    #	$ll6_____________	14	17	$verbraucher3
    #	$ll7_____________	15	18	$ll4
    #	$ll8_____________	16	19	$ll5
    #	$speicherikwh____	17	8	$ll6
    #	$speicherekwh____	18	9	$ll7
    #	$d1______________	19	26	$ll8
    #	$d2______________	20	27	$speichersoc
    #	$d3______________	21	28	$soc
    #	$d4______________	22	29	$soc1
    #	$d5______________	23	30	$temp1
    #	$d6______________	24	31	$temp2
    #	$d7______________	25	32	$temp3
    #	$d8______________	26	33	$d1
    #	$d9______________	27	34	$d2
    #	$d10 ____________	28	35	$d3
    #	Lpalle PV________	29	7	$d4
    #	Lpall Speicher___	30	7	$d5
    #	Lpalle EVU_______	31  7	$d6
    #	Device 1 PV______	32	26  $d7
    #	Device 1 Speicher	33	26	$d8
    #	Device 1 EVU____ 	34	26	$d9
    #	Device 2 pv________	35	27 $d10
    #	Device 2 Speicher_	36	27 $temp4
    #	device 2_EVU_______	37	27 $temp5
    #	Device 3 PV______	38	28 $temp6
    #	Device 3 Speicher	39	28
    #	Device 3 EVU____ 	40	28
    #	Device 4 PV______	41	29
    #	Device 4 Speicher	42	29
    #	Device 4 EVU____ 	43	29
    #	Device 5 PV______	44	30
    #	Device 5 Speicher	45	30
    #	Device 5 EVU____ 	46	30
    #	Device 6 PV______	47	31
    #	Device 6 Speicher	48	31
    #	Device 6 EVU____ 	49	31
    #	Device 7 PV______	50	32
    #	Device 7 Speicher	51	32
    #	Device 7 EVU____ 	52	32
    #	Device 8 PV______	53	33
    #	Device 8 Speicher	54	33
    #	Device 8 EVU____ 	55	33
    #	Device 9 PV______	56	34
    #	Device 9 Speicher	57	34
    #	Device 9 EVU____ 	58	34
    row [8] = inputrow [10]
    row [9] = inputrow [11]
    row [10] = inputrow [12]
    row [11] = inputrow [13]
    row [12] = inputrow [15]
    row [13] = inputrow [16]
    row [14] = inputrow [17]
    row [15] = inputrow [18]
    row [16] = inputrow [19]
    row [17] = inputrow [8]
    row [18] = inputrow [9]
    row [19] = inputrow [26]
    row [20] = inputrow [27]
    row [21] = inputrow [28]
    row [22] = inputrow [29]
    row [23] = inputrow [30]
    row [24] = inputrow [31]
    row [25] = inputrow [32]
    row [26] = inputrow [33]
    row [27] = inputrow [34]
    row [28] = inputrow [35]
    row [29] = inputrow [7]
    row [30] = inputrow [7]
    row [31] = inputrow [7]
    row [32] = inputrow [26]
    row [33] = inputrow [26]
    row [34] = inputrow [26]
    row [35] = inputrow [27]
    row [36] = inputrow [27]
    row [37] = inputrow [27]
    row [38] = inputrow [28]
    row [39] = inputrow [28]
    row [40] = inputrow [28]
    row [41] = inputrow [29]
    row [42] = inputrow [29]
    row [43] = inputrow [29]
    row [44] = inputrow [30]
    row [45] = inputrow [30]
    row [46] = inputrow [30]
    row [47] = inputrow [31]
    row [48] = inputrow [31]
    row [49] = inputrow [31]
    row [50] = inputrow [32]
    row [51] = inputrow [32]
    row [52] = inputrow [32]
    row [53] = inputrow [33]
    row [54] = inputrow [33]
    row [55] = inputrow [33]
    row [56] = inputrow [34]
    row [57] = inputrow [34]
    row [58] = inputrow [34]

    try:
        totalc = float(row [1]) + float(row [2]) + float(row [3]) + float(row [4]) + float(row [5])
    except:
        totalc = 0
    return (row,totalc)

def calcdelta(row,rowold,i,zeile,datestring):
    # Stunden differieren pro tag
    try:
        newvalue = float(row[i])
    except:
        newvalue = float(0)
    try:
        oldvalue = float(rowold[i])
    except:
        oldvalue = float(0)
    #	Monatlich_________	Seq	PosT	Tag
    #
    #	$bezug___________	1	1	$bezug
    #	$einspeisung_____	2	2	$einspeisung
    #	$pv______________	3	3	$pv
    #	$llg_____________	7	7	$llg
    #	$speicherikwh____	17	8	$ll6
    #	$speicherekwh____	18	9	$ll7
    #	Lpalle PV________	29	7	$d4
    #	Lpall Speicher___	30	7	$d5
    #	Lpalle EVU_______	31  7	$d6
    #	Device 1 PV______	32		$d7
    #	Device 1 Speicher	33		$d8
    #	Device 1 EVU____ 	34		$d9
    if (i >= 29) and (i<=58):
        try:
            gesamtv = float(0)
            deltabezug =  float (row[1]) - float(rowold[1])
            deltaeinspeisung = float (row[2]) - float(rowold[2])
            deltapv = float (row[3]) - float(rowold[3])
            deltaspeicherladung = float (row[17]) - float(rowold[17])
            deltaspeicherentladung = float (row[18]) - float(rowold[18])
            # gesamtv = Bezug    + PV        + Speicherentladung - Speicherladung - Einspeisung
            gesamtv = deltabezug  + deltapv + deltaspeicherentladung - deltaspeicherladung - deltaeinspeisung
            #einzelwerte validieren
            if (deltabezug >= 0) and (deltabezug < 12500) and (deltaeinspeisung >= 0) and (deltaeinspeisung < 12500) and (deltapv >= 0) and (deltapv < 12500) and (deltaspeicherladung >= 0) and (deltaspeicherladung < 12500) and (deltaspeicherentladung >= 0) and (deltaspeicherentladung < 12500):
                pass
            else:
                raise Exception("error ratio calc")
            if (i == 29) or (i == 32) or (i == 35) or (i==38) or (i==41)  or (i==44) or (i==47)  or (i==50)  or (i==53) or (i==56):
                # (PV - Einspeisung - Speicherladung) / Gesamtverbrauch)
                delta = ((deltapv - deltaeinspeisung - deltaspeicherladung)  / gesamtv) * (newvalue -  oldvalue)
            if (i == 30) or (i == 33) or (i == 36) or (i==39) or (i==42)  or (i==45) or (i==48)  or (i==51)  or (i==54) or (i==57):
                # Speicherentladung / Gesamtverbrauch
                delta = (deltaspeicherentladung  / gesamtv) * (newvalue -  oldvalue)
            if (i == 31) or (i == 34) or (i == 37) or (i==40) or (i==43)  or (i==46) or (i==49)  or (i==52)  or (i==55) or (i==58):
                #Bezug EVU / Gesamtverbrauch
                delta = (deltabezug  / gesamtv) * (newvalue -  oldvalue)
        except:
            delta = 0
            # nur fehler wenn gesamtverbrauch > 0
            if (gesamtv > 0):
                try:
                    textcol=header[i]
                except:
                    textcol= ''
                print ('%s i-err(R) %s:%s c %2d(%s) sum %.3f act %.3f prev %.3f gesamtv %.3f' % (getTime(),datestring,str(row[0]),i,textcol,sumcsv [i] ,newvalue, oldvalue,gesamtv ))
    else:
        delta = newvalue -  oldvalue
    deltarund = float(str("%.6f" % delta))
    if (deltarund < 0):
        deltarund = 0
    if (newvalue > oldvalue) and (deltarund < 12500) and (oldvalue > 0):
        sumcsv [i] = float(sumcsv [i])  + deltarund
        sumcsvt [i] = float(sumcsvt [i])  + deltarund
    else:
        if (deltarund > 0):
            try:
                textcol=header[i]
            except:
                textcol= ''
            print ('%s i-err %s:%s c %2d(%s) sum %.3f act %.3f prev %.3f' % (getTime(),datestring,str(row[0]),i,textcol,sumcsv [i] ,newvalue, oldvalue ))
def fillcount(row,  datestring  ,file_stringo,firstfile):
    # letzen tag abschliesen, neuen vorbereiten
    if (firstfile == 1):
        f1 = open(  file_stringo, 'w')
        f1.write(str(headerst))
        f1.close()
        os.chmod(file_stringo, 0o777)
    else:
        f1 = open(  file_stringo, 'a')
        excelstring=exceldate(countercsv [0])
        line = excelstring + ','
        for i in range (1,SUMCOLUMNSTART):
            line=line+ str(countercsv [i]) +','
        line=line+ str(-1) +','
        #print ('%s start write %s  ' % (getTime(), str(sumcsv [1])   ))
        for i in range (1,SUMCOLUMNSTART):
            sumt=float(sumcsv [i]/1000)
            line=line+ str(float("%.3f" % sumt)) +','
        line=line+ str(0) + '\n'
        f1.write(str(line))
        f1.close()
    countercsv [0] = datestring
    for i in range(1,SUMCOLUMNSTART):
        if (i < len(row)):
            countercsv [i] = row [i]
        else:
            countercsv [i] = float(0)
        sumcsv [i] = float(0)
    return

def fillcounts(monhtrow,file_stringos,lastdate,lastzeit):
    f1 = open(  file_stringos, 'w')
    line='Anzahl Spalten,' + str(SUMCOLUMNSTART*2) + ',Letzes Datum,' + lastdate + ',Letzte Zeit,' + lastzeit + ',  \n'
    f1.write(str(line))
    f1.write(str(headerst))
    excelstring=exceldate(monhtrow [0])
    line = excelstring + ','
    for i in range (1,SUMCOLUMNSTART):
        if (i < len(monhtrow)):
            line=line+ str(monhtrow [i]) +','
        else:
            line=line+ str("0") +','
    line=line+ str(-1) +','
    #print ('%s start write %.6f  ' % (getTime(),  sumcsv [1]   ))
    for i in range (1,SUMCOLUMNSTART):
        sumt=float(sumcsvt [i]/1000)
        line=line+ str(float("%.3f" % sumt)) +','
    line=line+ str(0) + '\n'
    f1.write(str(line))
    f1.close()
    os.chmod(file_stringos, 0o777)
    print ('%s %s written' % (getTime(),file_stringos))
    for i in range(1,SUMCOLUMNSTART):
        if (i < len(monhtrow)):
            monhtrow [i] = float(0)
        sumcsvt [i] = float(0)
    return
def reyeardet(calcyear):
    firstfile=1
    validdata=0
    #print ('%s actyear ' % (calcyear))
    lastdate = ''
    lastzeit = ''
    compspalten = 0
    startspalten = 0
    for dd in range(1, 13):
        dds = '0' + str (dd)
        datestring = int(str(calcyear) + dds[-2:])
        #summenfile montssuchen
        (file_stringi,file_stringis) = outfiledef(datestring)
        #outputfile year
        (file_stringo,file_stringos) = outfiledefyear(calcyear)
        if os.path.isfile(file_stringis):
            ifile=1
        else:
            ifile=0
        if (ifile == 1):
            try:
                f = open(  file_stringis, 'r')
                if firstfile==1:
                    print ('%s year output %s' % (getTime(),file_stringo))
                print ('%s year input  %s' % (getTime(),file_stringis))
                csv_os = csv.reader(f)
                firstrow = next(csv_os)
                if firstfile == 1:
                    startspalten = int(firstrow[1])
                compspalten = int(firstrow[1])
                headerrow = next(csv_os)
                sumrow = next(csv_os)
                f.close()
                if (startspalten == compspalten):
                    complastdate = firstrow[3]
                    complastzeit = firstrow[5]
                    if (firstfile == 1):
                        firstfile = 0
                        validdata=1
                        headerline = str(headerrow [0])
                        for i in range (2,startspalten+1):
                            if (i > len(headerrow)):
                                break
                            headerline=headerline+ ','
                            headerline=headerline+ str(headerrow [i-1])
                        headerline=headerline+  '\n'
                        f1 = open(  file_stringo, 'w')
                        f1.write(str(headerline))
                    sumline=''
                    for i in range(1,startspalten+2):
                        #print ('I %s ' % (str(i-1)))
                        sumline=sumline+ str(sumrow [i-1])
                        if i < (startspalten+1):
                            sumline=sumline+ ','
                    sumline=sumline+ '\n'
                    f1.write(str(sumline))
            except Exception as e:
                print ('%s Yearerror %s inhalt %s' % (getTime(),file_stringis, str(e) ))
    if (validdata == 1):
        f1.close()
        os.chmod(file_stringo, 0o777)
        f1 = open(  file_stringos, 'w')
        line='Anzahl Spalten,' + str(startspalten) + ',Letzes Datum,' + complastdate + ',Letzte Zeit,' + complastzeit + ',  \n'
        f1.write(str(line))
        f1.write(str(headerline))
        f1.close()
        os.chmod(file_stringos, 0o777)
        print ('%s %s written' % (getTime(),file_stringos))
    return
def remonth(jjjjmm):
    firstfile=1
    nextmonat = str(jjjjmm)[-2:]
    nextmonat = int(nextmonat) + 1
    nextyear = str(jjjjmm)[0:4]
    if (nextmonat > 12):
        nextyear = int(nextyear) + 1
        nextmonat = 1
    nextmonats =   '0' + str (nextmonat)
    jjjjmmnext = str(nextyear) + nextmonats[-2:]
    # print ('%s act %s next' % (jjjjmm,jjjjmmnext))
    lastdate = ''
    lastzeit = ''
    for dd in range(1, 32):
        dds = '0' + str (dd)
        datestring = str(jjjjmm) + dds[-2:]
        file_stringi =  inputp + datestring + '.csv'
        (file_stringo,file_stringos) = outfiledef(jjjjmm)
        if os.path.isfile(file_stringi):
            ifile=1
        else:
            ifile=0
        if (ifile == 1):
            try:
                f = open(  file_stringi, 'r')
                if firstfile==1:
                    print ('%s output %s' % (getTime(),file_stringo))
                print ('%s input  %s' % (getTime(),file_stringi))
                csv_o = csv.reader(f)
                zeile=0
                for inrow in csv_o:
                    (row,totalc)  = trdaymonth(inrow)
                    if (totalc != int(0)):
                        if (zeile == 0):
                            if (firstfile ==0):
                                for i in range(1,len(row)):
                                    calcdelta(row,rowold,i,zeile,datestring)
                            else:
                                monhtrow=row[:]
                                monhtrow[0] = datestring
                            fillcount(row,  datestring  ,file_stringo,firstfile)
                            firstfile=0
                        else:
                            lastdate = datestring
                            lastzeit = row[0]
                            for i in range(1,len(row)):
                                calcdelta(row,rowold,i,zeile,datestring)
                        rowold=row[:]
                        zeile = zeile + 1
                    else:
                        print ('%s skip %s:%s first 5 data columns zero' % (getTime(),datestring,row[0]))
                f.close()
            except Exception as e:
                print ('%s error %s inhalt %s' % (getTime(),datestring, str(e) ))
    # nichts gelesen ?
    if (firstfile == 1):
        return
    if (str(jjjjmm) == str(aktjjjjmm)):
        # heutiger Monat nachgerechnet, abschliessen
        fillcount(row,  datestring  ,file_stringo,firstfile)
    else:
        # vergangener Monat nachgerechnet, mit ersten Record vom folgemonat abschliessen
        for dd in range(1, 32):
            dds = '0' + str (dd)
            datestring = str(jjjjmmnext) + dds[-2:]
            file_stringi =  inputp + datestring + '.csv'
            if os.path.isfile(file_stringi):
                ifile=1
            else:
                ifile=0
            if (ifile == 1):
                try:
                    f = open(  file_stringi, 'r')
                    csv_o = csv.reader(f)
                    inrow = next(csv_o)
                    (row,totoalc) = trdaymonth(inrow)
                    for i in range(1,len(row)):
                        calcdelta(row,rowold,i,0,datestring)
                    f.close()
                    fillcount(row,  datestring  ,file_stringo,firstfile)
                    break
                except Exception as e:
                    print ('%s error1 %s inhalt %s' % (getTime(),datestring, str(e) ))
    #summenfile schreiben
    fillcounts(monhtrow,file_stringos,lastdate,lastzeit)
    return
def checkyear(calcyear):
    #lesen summenfile year
    lastdate = ''
    lastzeit = ''
    complastdate = ''
    complastzeit = ''
    compspalten = 0
    lastspalten = 0
    dfile=0
    ifile=0
    (file_stringo,file_stringos) = outfiledefyear(calcyear)
    try:
        if os.path.isfile(file_stringos):
            ifile=1
            f = open(file_stringos, 'r')
            csv_os = csv.reader(f)
            sumrow = next(csv_os)
            compspalten = int(sumrow[1])
            complastdate = sumrow[3]
            complastzeit = sumrow[5]
            f.close()
        else:
            ifile=0
        for dd in range(12, 0,-1):
            dds = '0' + str (dd)
            datestring = int(str(calcyear) + dds[-2:])
            #letzses summenfile montssuchen
            (file_stringi,file_stringis) = outfiledef(datestring)
            if os.path.isfile(file_stringis):
                dfile=1
                f = open(  file_stringis, 'r')
                csv_os = csv.reader(f)
                sumrow = next(csv_os)
                lastspalten = int(sumrow[1])
                lastdate = sumrow[3]
                lastzeit = sumrow[5]
                f.close()
                break
            else:
                dfile=0
    except Exception as e:
            print ('%s yearerror3 %s inhalt %s' % (getTime(),datestring, str(e) ))
    if (dfile==1) and (ifile == 0):
        print ('%s checkyear jjjj %s Summenfile fehlt' % (getTime(),calcyear))
        return 0
    if ((complastdate !=lastdate) or (complastzeit != lastzeit))  and (ifile == 1) :
        print ('%s checkyear jjjj %s neue Daten alt %s:%s neu %s:%s' % (getTime(),calcyear,complastdate,complastzeit,lastdate,lastzeit))
        return 0
    if (compspalten  != lastspalten) and (ifile == 1) :
        print ('%s checkyear jjjj %s Spalten geaendert' % (getTime(),calcyear))
        return 0
    return 1
def checkmonth(jjjjmm):
    #lesen summenfile
    lastdate = ''
    lastzeit = ''
    complastdate = ''
    complastzeit = ''
    compspalten = 0
    dfile=0
    ifile=0
    (file_stringo,file_stringos) = outfiledef(jjjjmm)
    try:
        if os.path.isfile(file_stringos):
            ifile=1
            f = open(file_stringos, 'r')
            csv_os = csv.reader(f)
            sumrow = next(csv_os)
            compspalten = int(sumrow[1])
            complastdate = sumrow[3]
            complastzeit = sumrow[5]
            f.close()
        else:
            ifile=0
        for dd in range(31, 0,-1):
            dds = '0' + str (dd)
            datestring = str(jjjjmm) + dds[-2:]
            file_stringi =  inputp + datestring + '.csv'
            if os.path.isfile(file_stringi):
                dfile=1
                validdata=0
                f = open(  file_stringi, 'r')
                csv_o = csv.reader(f)
                for inrow in csv_o:
                    lastzeit = inrow[0]
                    lastdate = datestring
                    try:
                        totalc = float(inrow [1]) + float(inrow [2]) + float(inrow [3]) + float(inrow [4]) + float(inrow [5])
                    except:
                        totalc = 0
                    if (totalc != 0):
                        validdata=1
                f.close()
                break
            else:
                dfile=0
    except Exception as e:
            print ('%s error3 %s inhalt %s' % (getTime(),datestring, str(e) ))
    if (dfile==1) and (validdata==1) and (ifile == 0):
        print ('%s checkmm jjjjmm %s Summenfile fehlt' % (getTime(),jjjjmm))
        return 0
    if ((complastdate !=lastdate) or (complastzeit != lastzeit))  and (ifile == 1) :
        print ('%s checkmm jjjjmm %s neue Daten alt %s:%s neu %s:%s' % (getTime(),jjjjmm,complastdate,complastzeit,lastdate,lastzeit))
        return 0
    if (compspalten  != int(SUMCOLUMNSTART*2)) and (ifile == 1) :
        print ('%s checkmm jjjjmm %s Spalten geaendert' % (getTime(),jjjjmm))
        return 0
    return 1

def reyear():
    for ji in range (startjjjj, aktjjjj+1):
        for mi in range (1, 13):
            mis =   '0' + str (mi)
            jis = str(ji) + mis[-2:]
            # nur bis heute rechnen
            if (int(jis)<=int(aktjjjjmm)):
                checkflag=checkmonth(jis)
                if (checkflag == 0):
                    remonth(jis)
        checkflag=checkyear(ji)
        if (checkflag == 0):
            reyeardet(ji)
    return
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True, help='folder containing daily logfiles')
    parser.add_argument('-o', '--output', type=str, required=True, help='destination folder for complete logfiles')
    parser.add_argument('-p', '--partial', type=str, required=True, help='destination folder for partial logfiles (actual month), should be in ramdisk')
    parser.add_argument('-m', '--mode', type=str, required=True, choices=["M", "A"], help='mode for calculation, M = month, A = all starting 2018/01')
    parser.add_argument('-d', '--date', type=int, required=False, default=time.strftime("%Y%m"), help='in mode M: month to calculate in format YYYYMM, defaults to current month')
    args = parser.parse_args()

    '''
    Parameter
    inputp = Verzeichnis der Tageslogs, csv Format (input)
        -> /var/www/html/openWB/web/logging/data/daily/ (sd karte)
    outputp = Verzeichnis der neuen Monatslogs, csv Format
        -> /var/www/html/openWB/web/logging/data/v001/  (sd karte)
    outputa = Verzeichnis von den aktuellen Monatlogs, csv Format
        -> /var/www/html/openWB/ramdisk/ (Dateiname logaktmonthonl(s).csv)
        Das aktuellen Monatslog wird den ganzen Monat immer wieder geschrieben,
        wenn neue Tageslogs kommen oder bestehende mit neuen 5 Minuten Einträgen erweitert werden
        (deshalb Ramdisk)
    mode = Verarbeitungsmodus
        M -> Rechnen und schreiben von einem Monat
        A -> Ueberpruefen jeden Monat ab Startjjjj (2018) bis heute,
        Neuberechnung gesamter Monat wenn ein gueltiges Tageslog für einen Monat vorhanden ist
        und Summenlog fehlt oder Anzahl Spalten (SUMCOLUMNSTART ) anders oder neuere Daten in Tageslog vorhanden
    JJMM -> nur bei M relevant, Monat zum nachrechnen
    '''

    aktjjjjmm  = time.strftime("%Y%m")
    aktjjjj = int(int(aktjjjjmm) / 100)
    header = [
            'Datum','Bezug','Einspeisung','Pv',
            'Lp1','Lp2','Lp3','Lpalle',
            'Verbraucher1imp','Verbraucher1exp','Verbraucher2imp','Verbraucher2exp',
            'Lp4','Lp5','Lp6','Lp7','Lp8','Speicherimp','Speicherexpt',
            'Device1','Device2','Device3','Device4','Device5','Device6','Device7','Device8','Device9','Device10',
            'Lpalle Pv','Lpalle Speicher','Lpalle EVU',
            'Device1 Pv','Device1 Speicher','Device1 EVU',
            'Device2 Pv','Device2 Speicher','Device2 EVU',
            'Device3 Pv','Device3 Speicher','Device3 EVU',
            'Device4 Pv','Device4 Speicher','Device4 EVU',
            'Device5 Pv','Device5 Speicher','Device5 EVU',
            'Device6 Pv','Device6 Speicher','Device6 EVU',
            'Device7 Pv','Device7 Speicher','Device7 EVU',
            'Device8 Pv','Device8 Speicher','Device8 EVU',
            'Device9 Pv','Device9 Speicher','Device9 EVU'
        ]
    # not smaller than 40
    SUMCOLUMNSTART = 60
    startjjjj= 2018
    inputp=args.input
    outputp=args.output
    outputa=args.partial
    mode=args.mode
    jjjjmm=args.date
    jjjj = int(int(jjjjmm) / 100)
    countercsv = []
    sumcsv = []
    sumcsvt = []
    for i in range (1,SUMCOLUMNSTART+1):
        countercsv.append("0")
        sumcsv.append("0")
        sumcsvt.append(float(0))

    prep()
    print ('%s csvcalc.py processing mode %s date jjjjmm %6d' % (getTime(),mode,jjjjmm))
    if (mode == 'M'):
        remonth(jjjjmm)
    else:
        reyear()
    print ('%s csvcalc.py finished' % (getTime()))
