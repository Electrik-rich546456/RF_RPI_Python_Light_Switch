#!/usr/bin/env python3
import signal
import sys
import time
import my_roomctl
from rpi_rf import RFDevice
dimm = 0
rfdevice = None
debounce = 10
short = 3.4
long = 1.2
count_s = 0
count_l = 0

count1 = 0
count2 = 0
count3 = 0
starttime = 0
endtime = 0
#
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
lasttime  = oldtime
print(short)
print(long)
#Received code 835186. is L Switch near entrance
#Received code 818562. is L Switch in hall way
#Received code 3764961. is big button on car remote <---- Living Room
#Received code 3764962. is next button on car remote <----Leo
#Received code 3764964. is next button on car remote <----My room
#Received code 3764968. is small button on car remote <--- all off
entrance = '835186'
hall_way = '818562'
bigg = '3764961'
leo_room = '3764962'
my_room = '3764964'
all_off = '3764968'
def rfff():
    dt = (time.strftime("%I:%M:%S %p"))
    
    global bigg,  dimm
    global count_s,  count_l,  count1,  count2,  count3,  count4
    global oldtime, oldtime1,  oldtime2,  oldtime3,  oldtime4
    global long
    global short
    global timestamp,  starttime,  endtime ,  lasttime
    switch = str(rfdevice.rx_code)
    if switch == bigg or  switch == hall_way or switch == entrance:
        now = time.perf_counter()       
        if endtime == 0 and now != 0:
                endtime = time.perf_counter()
                #print("endtime", endtime)
                #el = endtime-now
                laptime=round((time.perf_counter() - lasttime), 2)
                el2 = endtime-oldtime
                #print("endtime {:.6f}" .format(el))
                print("el2 {:.2f}" .format(el2))
                print("Lap Time: "+str(laptime))
                now = 0
                endtime = 0
                oldtime = time.perf_counter()
                #count = -99
        print("count short", count_s)
        print("count long", count_l)
        #elapsed = now - oldtime
        if el2 > long and el2 <= short:  #Greater than 2 mins and  less than count 2 <
            #count = 0
            print("Front Room Short Pressssssss" ,  dt)
            if dimm == 0:
                pass
            count_s += 1
            print("count short", count_s ,  dt)
            if count_s == 2:
                print("Front Room Short Pressssssss" ,  dt)
                #my_roomctl.living()
                count_s = 0
                count_l = 0
        if el2 <= long and dimm == 1:  # less than 2.6 sec  and Greater than count 4
            #count = 0
            count_l += 1
            if count_l > 5:
                print("Front Room Long Pressssssssss" ,  dt)
                #my_roomctl.living_br()
                count_l = 0
                count_s = 0
        lasttime=time.perf_counter()

##--------------------------------------leo-------------------------------------------------------------------------
    elif switch == leo_room:
        now1 = time.perf_counter()
        count1 += 1
        print("it worked")
        elapsed1 = now1 - oldtime1
        oldtime1 = now1
        if elapsed1 > short and count1 < 4: #Greater than 4 sec and  less than count 4 <
            print("Leo's Room Short Pressssssss" ,  dt)
            my_roomctl.leo()
            count1 = 0
        if elapsed1 < long and count1 > 6: # less than 0.5  and Greater than count 6
            print("Leo's Room Long Pressssssssss" ,  dt)
            my_roomctl.lights("Leo's Light", 4)
            oldtime1 = now1
            count1 = 0
##--------------------------------My Room-------------------------------------------------------------------------------
    elif switch == my_room:
        now2 = time.perf_counter()
        count2 += 1
        print("it worked")
        elapsed2 = now2 - oldtime2
        oldtime2 = now2
        if elapsed2 > short and count2 < 4: #Greater than 4 sec and  less than count 4 <
            print("My Room Short Pressssssss" ,  dt)
            my_roomctl.bed_lights('Bedroom Light', 1)
            count2 = 0
        if elapsed2 < long and count2 > 6: # less than 0.5  and Greater than count 6
            print("My Room Long Pressssssssss" ,  dt)
            my_roomctl.bed_lights('Bedroom Light', 4)
            oldtime2 = now2
            count2 = 0
##---------------------------------All off-----------------------------------------------------------------------
    elif switch == all_off: #need to rename var
        print("activating dimmer")
        dimm = 1
        #how do i make it wait till i press same button again 
        if switch == all_off:
            print("deactivating dimmer")
            dimm = 0
#        def dim(): #<-this was in the hopes to temp. block the other  if
#            global oldtime3 # conditions futher up the page 
#            now3 = time.perf_counter()
#            print("activating dimmer")
#            el3 = now3 - oldtime3
#            while el3 < 10:
#                #choose what to dim with bloking function like 
#                #input(bigg or leo_room) to triger my_roomctl.bed_lights('Bedroom Light', 4)
#                pass
#            oldtime3 = now3
#            if switch == bigg and el3 < long:
#                print("dimming")
#        dim()        
#            
##        now3 = time.perf_counter()
##        count3 += 1
##        print("it worked")
##        elapsed3 = now3 - oldtime3
##        oldtime3 = now3
##        if elapsed3 > short and count3 < 4: #Greater than 4 sec and  less than count 2 <
##            print("All Room off Short Pressssssss" ,  dt)
##            my_roomctl.all_pof()
##            count3 = 0
##        if elapsed3 < long and count3 > 8: # less than 0.5  and Greater than count 4
##            print("All Room off Long Pressssssssss" ,  dt)
##            my_roomctl.all_pof()
##            oldtime3 = now3
##            count3 = 0
            
x = 0
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        rfff()
#        while x < 5:
#            time.sleep(0.50)
#            count_s = 0
#            x += 1
#            print("x count" ,  x)
    time.sleep(0.50)



rfdevice.cleanup()
