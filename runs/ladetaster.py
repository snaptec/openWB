import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Sofortladen
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Min+PV
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)#NURPV
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)#AUS
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)#STANDBY
try:
    while True:
        button1_state = GPIO.input(12)
        button2_state = GPIO.input(16)
        button3_state = GPIO.input(6)
        button4_state = GPIO.input(13)
        button5_state = GPIO.input(21)
        time.sleep(0.2)
        if button1_state == False:
            file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
            file.write("0")
            file.close()
            file = open("/var/www/html/openWB/ramdisk/ladestatus.log","a") 
            file.write("Lademodus geaendert durch Ladetaster auf SofortLaden")
            file.close()
            time.sleep(0.2)
        if button2_state == False:
            file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
            file.write("1")
            file.close()
            file = open("/var/www/html/openWB/ramdisk/ladestatus.log","a") 
            file.write("Lademodus geaendert durch Ladetaster auf Min und PV")
            file.close()
            time.sleep(0.2)
        if button3_state == False:
            file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
            file.write("2")
            file.close()
            file = open("/var/www/html/openWB/ramdisk/ladestatus.log","a") 
            file.write("Lademodus geaendert durch Ladetaster auf NurPV")
            file.close()
            time.sleep(0.2)
        if button4_state == False:
            file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
            file.write("3")
            file.close()
            file = open("/var/www/html/openWB/ramdisk/ladestatus.log","a") 
            file.write("Lademodus geaendert durch Ladetaster auf Stop")
            file.close()
            time.sleep(0.2)
        if button5_state == False:
            file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
            file.write("4")
            file.close()
            file = open("/var/www/html/openWB/ramdisk/ladestatus.log","a") 
            file.write("Lademodus geaendert durch Ladetaster auf Standby")
            file.close()
            time.sleep(0.2)
except:
     GPIO.cleanup()
