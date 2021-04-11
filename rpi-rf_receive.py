#!/usr/bin/env python3
import signal
import sys
import time
import my_room
from rpi_rf import RFDevice
rfdevice = None
debounce = 10
short = 2
long = 20
# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)

rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()
timestamp = None
oldtime = time.perf_counter()
oldtime1 = time.perf_counter()
oldtime2 = time.perf_counter()
oldtime3 = time.perf_counter()

#Received code 835186. is L Switch near entrance
#Received code 818562. is L Switch in hall way
#-------
#Received code 3764961. is big button on car remote <---- Living Room
#Received code 3764962. is next button on car remote <----Leo
#Received code 3764964. is next button on car remote <----My room
#Received code 3764968. is small button on car remote <--- all off
while True:
    dt = (time.strftime("%I:%M:%S %p"))
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        now = time.perf_counter()
        if ((str(rfdevice.rx_code) == '3764961')) or  ((str(rfdevice.rx_code) == '818562')) or ((str(rfdevice.rx_code) == '835186')) :
            elapsed = now - oldtime
            if elapsed < debounce: # Less than 10                
                pass
            else:
                oldtime = now
                print("Front Room Lights Pressed" ,  dt)
                my_room.living()
            if elapsed <= long: # Less than or equal to 20
                oldtime = now
                my_room.lights("Light_3", 4)
            
##--------------------------------------leo-------------------------------------------------------------------------
        elif ((str(rfdevice.rx_code) == '3764962')):
            now1 = time.perf_counter()
            elapsed1 = now1 - oldtime1
            if elapsed1 < debounce:
                my_room.leo_br()
                print("Duplicate Button Press - Dimming")
                #pass
            else:
                oldtime1 = now1
                print("Leo's Room Lights Pressed" ,  dt)
                my_room.leo()
##--------------------------------My Room-------------------------------------------------------------------------------
        elif ((str(rfdevice.rx_code) == '3764964')):
            now2 = time.perf_counter()
            elapsed2 = now2 - oldtime2
            if elapsed2 < debounce:
                my_room.lights('Bedroom Light' ,  4)
                print("Duplicate Button Press - Dimming")
                #pass
            else:
                oldtime2 = now2
                print("My Room Lights Pressed" ,  dt)
                my_room.bed()
##--------------------------------------------------------------------------------------------------------
        elif ((str(rfdevice.rx_code) == '3764968')):
            now3 = time.perf_counter()
            elapsed3 = now3 - oldtime3
            if elapsed3 < debounce:
                #print("Ignoring Duplicate Button Press")
                pass
            else:
                oldtime3 = now3
                print("All Room's Lights Off" ,  dt)
                my_room.all_pof()
#-----------------------------------------------------------------------------------------------------------
    time.sleep(0.01)
rfdevice.cleanup()
#my_room.living_br()    
#print("Duplicate Button Press - Dimming")
#
