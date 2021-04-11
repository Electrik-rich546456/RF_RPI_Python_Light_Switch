#!/usr/bin/env python3
import threading
import signal
import sys
import time
#from datetime import timedelta
#from threading import Timer
from rpi_rf import RFDevice

rfdevice = None
debounce = 10
entrance = '835186'
hall_way = '818562'
bigg = '3764961'
leo_room = '3764962'
my_room = '3764964'
all_off = '3764968'

#global switch

def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()
timestamp = None
timestamp2 = time.perf_counter()
timestamp3 = None
lastClick = 0
lastcode = 0
switch = None
count = 0
count_long = 0
count_long2 = 0
def button_pressed(switch):
    global lastClick,  count,  timestamp2,  count_long,  lastcode
    lastClick = time.perf_counter()
    count += 1
    print("button pressed", switch ,  "button count", count, "long",count_long )
    lastcode = switch
    print("a's", switch)
    print("last code", lastcode)
    elapsed = lastClick - timestamp2
    print("elapsed", round(elapsed, 2))
    timestamp2 = time.perf_counter()
    
    if elapsed <= 1:
        count_long += 1
        print("long", count_long)
#        for n in args:
#            if n == bigg:
#                print ("big button repeat code", count_long )
#        if count_long == 5:
#            count_long = 0
#            return
#    print("button press", count)
    return switch

def state_machine(*switch):
    #    print("State Machine Go..." , switch)
    STATE1 = 1 # ON
    STATE2 = 2 # OFF
    STATE3 = 3 # LONG PRESS
    INITIAL_STATE = STATE1
#    DEBOUNCE_SECONDS = 10
    state = INITIAL_STATE
    global lastClick,  count,  count_long,  count_long2, all_off,  bigg,  lastcode
    global leo_room,  my_room,  entrance,  hall_way
#    STATE4 = all_off
    lastClick = 0 # wait for next button click
    lastcode = 0
    button_state = lastcode
#    print("Last click set")
    while True:
        
#        print("While true loop...")
#        elapsed = time.time() - lastClick
        ###### state definitions and transitions
        if state == STATE1:  # STATE1 actions and transitions
            if lastClick != 0:
                print("On!")
                print("last code", lastcode)
                print("button state", button_state)
                lastClick = 0  # we handled click
                count = 0
                #state = STATE2
                #if count_long == 5:
                    #print("long press detected")
                    #state = STATE2
                state = STATE2  # goto STATE2
#            count_long =0
        if state == STATE2:
            if button_state == all_off:  # STATE2 actions and transitions
                print("select")
                if button_state == bigg:
                    print("Cool")
                #if count_long >=5:
                    print("dimming...")
                    count_long2 += 1
                    if count_long2 == 5:
                        count_long = 0
                        count_long2 = 0
                        state = STATE1
                    count = 0
                    lastClick = 0  # we handled click
    #            else:
    #                state = STATE3
                    #state = INITIAL_STATE
        #                state = STATE1
            if time.perf_counter() - timestamp2 > 240:
                print(time.perf_counter() - timestamp2 > 240)
                state = STATE3
                print("reset")
        if state == STATE3:
            #if state == STATE4:
                #print("done")
            if lastClick != 0:
                print("off was pressed.......")
                count_long = 0
                lastClick = 0
                state = STATE1
        #if state == STATE4:
            
            #if time.perf_counter() ==10:
                
            
        # transitions common to all states
        if time.perf_counter() - lastClick > 60:
#            print("Check time")
            lastClick = 0  # timeout
            count = 0
            count_long = 0
            #state = STATE1
#            print("State = "+str(state))
#            print("Last Click = "+str(lastClick))
        time.sleep(1)
        lastcode = 0
        

# create separate thread for state machine
stateMachineThread = threading.Timer(0.5, state_machine, args=(switch))
stateMachineThread.daemon = True
stateMachineThread.start()
args = str(rfdevice.rx_code)
while True:
    #global switch
    switch = str(rfdevice.rx_code)
    
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if switch == bigg or  switch == hall_way or switch == entrance or switch == leo_room or switch == my_room or switch == all_off:
            button_pressed(switch)
        
#        if rfdevice._rx_last_timestamp != timestamp3:
#            timestamp3 = rfdevice._rx_last_timestamp
#        print("time in loop", timestamp)        
#            print(type(timestamp))
##            print("yay",  timestamp)
#            totaltime=round((timestamp), 2) 
#            print("time     stamp " +str(timestamp))
##            print("last timestamp", str(timestamp+timedelta(hours=-1))).split(' ')[1][:12]
#            
            #print(rfdevice._rx_repeat_count)
            #print (timestamp3 ,  timestamp)
            #elapsed9 = timestamp3  - timestamp
            #print(elapsed9)
            #if timestamp != timestamp:
                #print("echo")
            #if elapsed9 < 6000:
                #print("dup")
#                timestamp = 0
#                timestamp3 = 0

#        logging.info(str(rfdevice.rx_code) +
#                     " [pulselength " + str(rfdevice.rx_pulselength) +
#                     ", protocol " + str(rfdevice.rx_proto) + "]")
    time.sleep(0.01)
rfdevice.cleanup()
