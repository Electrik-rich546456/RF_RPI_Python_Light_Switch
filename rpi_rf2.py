#!/usr/bin/env python3
import time
from rpi_rf import RFDevice
rfdevice = None
rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()
big_button = 3764961
rfdevice.rx_callback(gpio=27)
timestamp = None
last_timestamp = None
# timestamp2 = time.perf_counter()
#key = (str(rfdevice.rx_code))
count = 0

    
def rfff():
    command = (str(rfdevice.rx_code))
    if command == '3764961':
        print("yay")
        global count
        count += 1
        print(count)
        if count == 10:
            print("long press")
            count = 0
        if count == 4:
            print("short press")
            count = 5
#            return True
#            timestamp2 = time.perf_counter()
#            elapsed =  timestamp - t
#            time_taken = timestamp - round(time.time() , 2) #rounding the long decimal float
#            print(time_taken,'seconds')
#            print("elapsed" ,  elapsed)
 
#    if key:
#        print(key)
#    #with rfff as press_listener: #setting code for listening key-press
#    #    press_listener.join()
#    global t
#    t = time.time() #reading time in sec
#    if key == False:
#        print(key)
#    #with rfff(on_release = on_key_release) as release_listener: #setting code for listening key-release
#    #    release_listener.join()
    

while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
#        count = 0
        rfff()
    time.sleep(0.50)
    

#            print("elapsed" ,  elapsed)

    #    print("time" ,  timestamp)
    #    if ((str(rfdevice.rx_code) == '3764961')):
#            timestamp2 = rfdevice.rx_code_timestamp
    #        print("time 2" ,  timestamp2)
    #        elapsed =  timestamp - timestamp2
    #        print("elapsed" ,  elapsed)
    #        print(str(rfdevice.rx_code))


