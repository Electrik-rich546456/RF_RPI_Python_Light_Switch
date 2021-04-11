#!/usr/bin/env python3
import signal
import sys
import time
#import my_room
from rpi_rf import RFDevice
rfdevice = None
debounce = 10
short = 4
long = 0.5
global count
count = 0

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
print(short)
print(long)
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
        print("up")
        if ((str(rfdevice.rx_code) == '3764961')) or  ((str(rfdevice.rx_code) == '818562')) or ((str(rfdevice.rx_code) == '835186')) :
            print(str(rfdevice.rx_code))
            count += 1
            print(count)
            elapsed = now - oldtime
            print("elapsed" ,  elapsed)
            oldtime = now
#            if elapsed < debounce: # Less than 10                
#                pass
#            else:
##                oldtime = now
#                print("Front Room after debounce Press" ,  dt)
#                oldtime = now
##                my_room.living()
#            elapsed = now - oldtime
            if elapsed > short and count < 2: #Greater than 4 sec and  less than count 2 <
                print("Front Room Short Pressssssss" ,  dt)
            if elapsed < long and count > 4: # less than 0.5  and Greater than count 4
                print("Front Room Long Pressssssssss" ,  dt)
            oldtime = now
#            count = 0

rfdevice.cleanup()
