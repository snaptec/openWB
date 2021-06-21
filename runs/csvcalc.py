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
aktjjjjmm  = time.strftime("%Y%m")
aktjjjj = int(int(aktjjjjmm) / 100)
header = [
'Datum','Bezug','Einspeisung','Pv',
'Lp1','Lp2','Lp3','Lpalle',
'Verbraucher1imp','Verbraucher1exp','Verbraucher2imp','Verbraucher2exp',
'Lp4','Lp5','Lp6','Lp7','Lp8','Speicherimp','Speicherexpt',
'Device1','Device2','Device3','Device4','Device5','Device6','Device7','Device8','Device9','Device10'
]
SUMCOLUMNSTART = 40
startjjjj= 2018
inputp=str(sys.argv[1])
outputp=str(sys.argv[2])
outputa=str(sys.argv[3])
mode=str(sys.argv[4])
try:
    jjjjmm=int(sys.argv[5])
except:
    jjjjmm=int(aktjjjjmm)
# Parameter
# inputp = Verzeichnis der tagesexcel (input)
#       -> /var/www/html/openWB/web/logging/data/daily/ (sd karte)
# outputp = Verzeichnis der neuen Monatsexcel
#       -> /var/www/html/openWB/web/logging/data/excel/  (sd karte)
# outputa = Verzeichnis von dem aktuellen Monatsexel
#       -> /var/www/html/openWB/ramdisk/ (Dateiname logaktmonthonl(s).csv)
#           Das aktuellen Monatsexel wird den ganzen Monat immer wieder geschrieben,
#           wenn neue tagesexcel kommen oder die mit neuen 5 Minuten Eintraegen erweitert werden
#           (deshalb Ramdisk)
# mode = Verarbeitungsmodus
#       M -> Rechnen und schreiben von einem Monat
#       A -> Ueberpruefen jeden Monat ab Startjjjj (2018) bis heute  ,
#           neuberechnung gesamter Monat wenn
#               ein gueltiges Tagesexcel für einen Monat vorhanden ist
#               und Summenexecl fehlt
#               oder Anzahl Spalten (SUMCOLUMNSTART ) anders
#               oder neuere Daten in Tagesexel vorhanden
#
# JJMM -> nur bei M relevant, Monat zum nachrechnen
#
jjjj = int(int(jjjjmm) / 100)
countercsv = []
sumcsv = []
sumcsvt = []
for i in range (1,SUMCOLUMNSTART+1):
    countercsv.append("0")
    sumcsv.append("0")
    sumcsvt.append(float(0))
def outfiledef(jjjjmminput):
    if (str(jjjjmminput) == str(aktjjjjmm)):
    # heutiger Monat nachgerechnet, ramdisk nehmen
        file_stringo =  outputa + 'logaktmonthonl.csv'
        file_stringos =  outputa + 'logaktmonthonls.csv'
    else:
        file_stringo =  outputp + str(jjjjmminput) + 'onl.csv'
        file_stringos =  outputp + str(jjjjmminput) + 'onls.csv'
    return (file_stringo,file_stringos)
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
def timeup():
    global time_string
    named_tuple = time.localtime() # getstruct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    return
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
#gleiche positionen
#   zeit    0    datum  0
#	Täglich	Index täglich	Monatlich	Seq
#
#	$bezug	1	$bezug	1
#	$einspeisung	2	$einspeisung	2
#	$pv	3	$pv	3
#	$ll1	4	$ll1	4
#	$ll2	5	$ll2	5
#	$ll3	6	$ll3	6
#	$llg	7	$llg	7
#andere postionen
#	$speicheri	8	$verbraucher1iwh	10
    row [8] = inputrow [10]
#	$speichere	9	$verbraucher1ewh	11
    row [9] = inputrow [11]
#	$verbraucher1	10	$verbraucher2iwh	12
    row [10] = inputrow [12]
#	$verbrauchere1	11	$verbraucher2ewh	13
    row [11] = inputrow [13]
#	$verbraucher2	12	$ll4	15
    row [12] = inputrow [15]
#	$verbrauchere2	13	$ll5	16
    row [13] = inputrow [16]
#	$verbraucher3	14	$ll6	17
    row [14] = inputrow [17]
#	$ll4	15	$ll7	18
    row [15] = inputrow [18]
#	$ll5	16	$ll8	19
    row [16] = inputrow [19]
#	$ll6	17	$speicherikwh	8
    row [17] = inputrow [8]
#	$ll7	18	$speicherekwh	9
    row [18] = inputrow [9]
#	$ll8	19	$d1	26
    row [19] = inputrow [26]
#	$speichersoc	20	$d2	27
    row [20] = inputrow [27]
#	$soc	21	$d3	28
    row [21] = inputrow [28]
#	$soc1	22	$d4	29
    row [22] = inputrow [29]
#	$temp1	23	$d5	30
    row [23] = inputrow [30]
#	$temp2	24	$d6	31
    row [24] = inputrow [31]
#	$temp3	25	$d7	32
    row [25] = inputrow [32]
#	$d1	26	$d8	33
    row [26] = inputrow [33]
#	$d2	27	$d9	34
    row [27] = inputrow [34]
#	$d3	28	$d10 	35
    row [28] = inputrow [35]
#	$d4	29
#	$d5	30
#	$d6	31
#	$d7	32
#	$d8	33
#	$d9	34
#	$d10	35
#	$temp4	36
#	$temp5	37
#	$temp6 	38
    row [29] = float(0)
    row [30] = float(0)
    row [31] = float(0)
    row [32] = float(0)
    row [33] = float(0)
    row [34] = float(0)
    row [35] = float(0)
    row [36] = float(0)
    row [37] = float(0)
    row [38] = float(0)
    try:
        totalc = float(row [1]) + float(row [2]) + float(row [3]) + float(row [4]) + float(row [5])
    except:
        totalc = 0
    return (row,totalc)
def calcdelta(row,rowold,i,zeile,datestring):
#Stunden differieren pro tag
    try:
        newvalue = float(row[i])
    except:
        newvalue = float(0)
    try:
        oldvalue = float(rowold[i])
    except:
        oldvalue = float(0)
    delta = newvalue -  oldvalue
    if (newvalue > oldvalue) and (delta < 12500) and (oldvalue > 0):
        sumcsv [i] = float(sumcsv [i])  + delta
        sumcsvt [i] = float(sumcsvt [i])  + delta
    else:
        if (delta > 0):
            try:
                textcol=header[i]
            except:
                textcol= ''
            print ('%s i-err %s:%s c %2d(%s) sum %.3f act %.3f prev %.3f' % (time_string,datestring,str(row[0]),i,textcol,sumcsv [i] ,newvalue, oldvalue ))
def fillcount(row,  datestring  ,file_stringo,firstfile):
#letzen tag abschliesen, neuen vorbereiten
    if (firstfile == 1):
        f1 = open(  file_stringo, 'w')
        f1.write(str(headerst))
        f1.close()
        os.chmod(file_stringo, 0o777)
    else:
        f1 = open(  file_stringo, 'a')
        line = str(countercsv [0]) + ','
        for i in range (1,SUMCOLUMNSTART):
            line=line+ str(countercsv [i]) +','
        line=line+ str(-1) +','
        #print ('%s start write %s  ' % (time_string, str(sumcsv [1])   ))
        for i in range (1,SUMCOLUMNSTART):
            sumt=float(sumcsv [i]/1000)
            line=line+ str(float("%.6f" % sumt)) +','
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
    line = str(monhtrow [0]) + ','
    for i in range (1,SUMCOLUMNSTART):
        if (i < len(monhtrow)):
            line=line+ str(monhtrow [i]) +','
        else:
            line=line+ str("0") +','
    line=line+ str(-1) +','
    #print ('%s start write %.6f  ' % (time_string,  sumcsv [1]   ))
    for i in range (1,SUMCOLUMNSTART):
        sumt=float(sumcsvt [i]/1000)
        line=line+ str(float("%.6f" % sumt)) +','
    line=line+ str(0) + '\n'
    f1.write(str(line))
    f1.close()
    os.chmod(file_stringos, 0o777)
    print ('%s %s written' % (time_string,file_stringos))
    for i in range(1,SUMCOLUMNSTART):
        if (i < len(monhtrow)):
            monhtrow [i] = float(0)
        sumcsvt [i] = float(0)
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
    #print ('%s act %s next' % (jjjjmm,jjjjmmnext))
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
                    print ('%s output %s' % (time_string,file_stringo))
                print ('%s input  %s' % (time_string,file_stringi))
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
                        print ('%s skip %s:%s first 5 data columns zero' % (time_string,datestring,row[0]))
                f.close()
            except Exception as e:
                print ('%s error %s inhalt %s' % (time_string,datestring, str(e) ))
    # nichts gelesen ?
    if (firstfile == 1):
        return
    if (str(jjjjmm) == str(aktjjjjmm)):
    # heutiger Monat nachgerechnet, abschliessen
        fillcount(row,  datestring  ,file_stringo,firstfile)
    else:
    # vergangenr Monat nachgerechnet, mit ersten Record vom folgemonat abschliessen
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
                    print ('%s error1 %s inhalt %s' % (time_string,datestring, str(e) ))
    #summenfile schreiben
    fillcounts(monhtrow,file_stringos,lastdate,lastzeit)
    return
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
            print ('%s error3 %s inhalt %s' % (time_string,datestring, str(e) ))
    if (dfile==1) and (validdata==1) and (ifile == 0):
        print ('%s checkmm jjjjmm %s Summenfile fehlt' % (time_string,jjjjmm))
        return 0
    if ((complastdate !=lastdate) or (complastzeit != lastzeit))  and (ifile == 1) :
        print ('%s checkmm jjjjmm %s neue Daten alt %s:%s neu %s:%s' % (time_string,jjjjmm,complastdate,complastzeit,lastdate,lastzeit))
        return 0
    if (compspalten  != int(SUMCOLUMNSTART*2)) and (ifile == 1) :
        print ('%s checkmm jjjjmm %s Spalten geaendert' % (time_string,jjjjmm))
        return 0
    return 1
def reyear():
    for ji in range (startjjjj, aktjjjj+1):
        for mi in range (1, 13):
            mis =   '0' + str (mi)
            jis = str(ji) + mis[-2:]
#nur bis heute rechnen
            if (int(jis)<=int(aktjjjjmm)):
                checkflag=checkmonth(jis)
                if (checkflag == 0):
                    remonth(jis)
    return
timeup()
prep()
print ('%s csvcal.py processing mode %s date jjjjmm %6d' % (time_string,mode,jjjjmm))
if (mode == 'M'):
    remonth(jjjjmm)
else:
    reyear()
timeup()
print ('%s csvcal.py finished' % (time_string))
