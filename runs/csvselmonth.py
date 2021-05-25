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
def itdate(datestring):
    datestringit =  datestring[-4:]   + datestring[3:5]  + datestring[:2]
    nextmonat = int(datestring[3:5] ) + 1
    nextyear = int(datestring[-4:])
    if (nextmonat > 12):
        nextyear = int(nextyear) + 1
        nextmonat = 1
    nextmonats =   '0' + str (nextmonat)
    datestringitnext = str(nextyear) + nextmonats[-2:] + '01'
    return (datestringit,datestringitnext)
def infiledef(jjjjmminput):
    if (str(jjjjmminput) == str(aktjjjjmm)):
    # heutiger Monat nachgerechnet, ramdisk nehmen
        file_cvsfinp =  inputcvsa + 'logaktmonthonl.csv'
        file_cvsfinps =  inputcvsa + 'logaktmonthonls.csv'
    else:
        file_cvsfinp =  inputcvsp + str(jjjjmminput) + 'onl.csv'
        file_cvsfinps =  inputcvsp + str(jjjjmminput) + 'onls.csv'
    return (file_cvsfinp,file_cvsfinps)
def getTime():
    named_tuple = time.localtime() # getstruct_time
    return time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
def seprow(usedspalten,compspalten,irow):
    #print ('usedspalten %s compspalten %s len %s' % (str(usedspalten),str(compspalten),str(len(irow))))
    #usedspalten 75 compspalten 40 len 81
    #datum in it format umwandeln
    datestringitnext = ''
    datestringit = ''
    (datestringit,datestringitnext) = itdate(str(irow [0]))
    sumlinec=datestringit+','
    sumlineb=datestringit+','
    #alles andere
    for i in range(2,usedspalten+1):
        #print ('I %s ' % (str(i)))
        sumlinec=sumlinec+ str(irow [i-1])
        sumlineb=sumlineb+ str(irow [i-1+compspalten])
        if i < (usedspalten):
            sumlinec=sumlinec+ ','
            sumlineb=sumlineb+ ','
    sumlinec=sumlinec+ '\n'
    sumlineb=sumlineb+ '\n'
    return (sumlinec,sumlineb,datestringitnext)
def selmonth(jjjjmm):
    #lesen summenfile
    datestringitnext = ''
    complastdate = ''
    complastzeit = ''
    compspalten = 0
    ifile=0
    (file_cvsfinp,file_cvsfinps) = infiledef(jjjjmm)
    try:
        if os.path.isfile(file_cvsfinps):
            ifile=1
            f = open(file_cvsfinps, 'r')
            csv_os = csv.reader(f)
            sumrow = next(csv_os)
            compspalten = int(int(sumrow[1]) / 2)
            complastdate = sumrow[3]
            complastzeit = sumrow[5]
            headerrow = next(csv_os)
            sumrow = next(csv_os)
            f.close()
        else:
            ifile=0
    except Exception as e:
            print ('%s error %s inhalt %s' % (getTime(),datestring, str(e) ))
    if (ifile == 0):
        print ('%s summenfile nicht gefunden %s' % (getTime(),datestring,file_cvsfinps ))
        return
    # header machen
    headerline = str(headerrow [0]) +','
    for i in range (compspalten+2,(compspalten*2)+2):
        if (i > len(headerrow)):
            break
        headerline=headerline+ str(headerrow [i-1]) +','
    #Headerline für online abschliessen
    # file 1 -> headerst
    headerline=headerline+ str('*ENDE*')+ '\n'
    f1 = open(  outputfile + 'a_onl1', 'w')
    f1.write(str(headerline))
    f1.close()
    #nur bis laenge header  schicken
    # summenzeile in Zaehler und betraege trennen
    (sumlinec,sumlineb,datestringitnext)  = seprow(len(headerrow)-compspalten,compspalten,sumrow)
    # file 2 -> Zaehler summe
    # file 3 -> beträge summe
    f1 = open(  outputfile + 'a_onl2', 'w')
    f1.write(str(sumlinec))
    f1.close()
    f1 = open(  outputfile + 'a_onl3', 'w')
    f1.write(str(sumlineb))
    f1.close()
    os.chmod(outputfile + 'a_onl1', 0o777)
    os.chmod(outputfile + 'a_onl2', 0o777)
    os.chmod(outputfile + 'a_onl3', 0o777)
    #lesen gesamtes monatsfile
    ifile=0
    try:
        if os.path.isfile(file_cvsfinp):
            ifile=1
            f = open(file_cvsfinp, 'r')
            # file 4 -> Zaehler detail
            # file 5 -> beträge detail
            f1 = open(  outputfile + 'a_onl4', 'w')
            f2 = open(  outputfile + 'a_onl5', 'w')
            f3 = open(  outputfile + 'a_onl6', 'w')
            f4 = open(  outputfile + 'a_onl7', 'w')
            csv_o = csv.reader(f)
            i = 0
            for inrow in csv_o:
                if (i == 0):
                    pass
                else:
                    (sumlinec,sumlineb,datestringitnext)  = seprow(len(headerrow)-compspalten,compspalten,inrow)
                    if (i < 15):
                        f1.write(str(sumlinec))
                        f2.write(str(sumlineb))
                    else:
                        f4.write(str(sumlinec))
                        f3.write(str(sumlineb))
                i=i+1
            # folgemonat simulierem
            print ('%s letzer vom Monat %s, Saetze %s' % (getTime(),sumlinec[:8],str(i) ))
            sumlinec=datestringitnext+','+sumlinec[9:]
            f4.write(str(sumlinec))
            sumlineb=datestringitnext+','+sumlineb[9:]
            f3.write(str(sumlineb))
            f.close()
            f1.close()
            f2.close()
            f3.close()
            f4.close()
            os.chmod(outputfile + 'a_onl4', 0o777)
            os.chmod(outputfile + 'a_onl5', 0o777)
            os.chmod(outputfile + 'a_onl6', 0o777)
            os.chmod(outputfile + 'a_onl7', 0o777)
    except Exception as e:
        print ('%s error1 %s inhalt %s' % (getTime(),datestring, str(e) ))
    if (ifile == 0):
        print ('%s datenfile nicht gefunden %s' % (getTime(),datestring,file_cvsfinp ))
    return
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, required=True, help='output folder should be in ramdisk for mqtt files ')
    parser.add_argument('-i', '--input', type=str, required=True, help='folder for complete logfiles as input')
    parser.add_argument('-p', '--partial', type=str, required=True, help='partial logfiles (actual month), should be in ramdisk as input')
    parser.add_argument('-d', '--date', type=int, required=False, default=time.strftime("%Y%m"), help='month to select in format YYYYMM, defaults to current month')
    args = parser.parse_args()
    aktjjjjmm  = time.strftime("%Y%m")
    aktjjjj = int(int(aktjjjjmm) / 100)
    inputcvsp=args.input
    outputfile=args.output
    inputcvsa=args.partial
    jjjjmm=args.date
    jjjj = int(int(jjjjmm) / 100)
    print ('%s csvselmonth.py  select date jjjjmm %6d' % (getTime(),jjjjmm))
    selmonth(jjjjmm)
    print ('%s csvselmonth.py finished' % (getTime()))
