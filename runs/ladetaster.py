import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Sofortladen
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Min+PV
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)#NURPV
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)#AUS
try:
    while True:
         button1_state = GPIO.input(12)
         button2_state = GPIO.input(16)
         button3_state = GPIO.input(6)
         button4_state = GPIO.input(13)
         time.sleep(1)
    if button1_state == False:
         file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
         file.write("0")
         file.close()
         time.sleep(0.2)
    if button2_state == False:
         file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
         file.write("1")
         file.close()
         time.sleep(0.2)
    if button3_state == False:
        file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
        file.write("2")
        file.close()
        time.sleep(0.2)
    if button4_state == False:
        file = open("/var/www/html/openWB/ramdisk/lademodus","w") 
        file.write("3")
        file.close()
        time.sleep(0.2)
except:
     GPIO.cleanup()
