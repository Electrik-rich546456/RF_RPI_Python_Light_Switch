#!/usr/bin/env python3
import time
from rpi_rf import RFDevice
rfdevice = None
rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()
timestamp = None
i = 0
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if str(rfdevice.rx_code) == '3764961':
            start = time.perf_counter()
            i = i+1
            print("Detect code " + str(rfdevice.rx_code) + " i=" + str(i))
            end = time.perf_counter()
            elapsed = int(end-start)
            print("Elapsed time in seconds:", elapsed) 
            if elapsed < 0.005 and i == 10:
               print("long press")
#               i = 0
#            else:
#                print("short")
        if i == 10:
            r =1
            while r:
                print("something")
                time.sleep(30)
                i = 0
                r = 0
                
#            start2 = time.perf_counter()
#            print("publish.single /home/hass/.homeassistant/sensor/pir_entrance_one ON ,hostname=localhost auth=auth)")
#            i = 0
#            end2 = time.perf_counter()
#            print("Elapsed time in seconds:", end2-start2)
#            time.sleep(2)
    time.sleep(0.01)
rfdevice.cleanup()
