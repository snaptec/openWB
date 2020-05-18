import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
state=0
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    while True:
        button1_state = GPIO.input(10)
        time.sleep(0.2)

        if button1_state == False:
            if state == 0:
                file = open("/var/www/html/openWB/ramdisk/buchsestatus","w") 
                file.write("1")
                file.close()
                time.sleep(0.2)
                state=1
        if button1_state == True:
            if state == 1:
                file = open("/var/www/html/openWB/ramdisk/buchsestatus","w") 
                file.write("0")
                file.close()
                time.sleep(0.2)
                state=0
except:
    GPIO.cleanup()
