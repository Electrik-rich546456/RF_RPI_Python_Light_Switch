#!/usr/bin/env python3
import threading
import signal
import sys
import time
#from datetime import timedelta
#from threading import Timer
from rpi_rf import RFDevice
import my_roomctl

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
    #print("button pressed", switch ,  "button count", count, "long",count_long )
    lastcode = switch
    #print("a's", switch)
    #print("last code", lastcode)
    elapsed = lastClick - timestamp2
    print("elapsed", round(elapsed, 2))
    timestamp2 = time.perf_counter()
    if elapsed <= debounce:
        count_long += 1
        #print("long", count_long)
        if count_long == 5:
            count_long = 0
    return "switch"

def state_machine():
    global lastClick, count, count_long, count_long2, lastcode, button_state
    global leo_room, my_room, entrance, hall_way, bigg, sure,  switch
    lastClick = 0 # wait for next button click
    lastcode = 0
    while True:
        dt = (time.strftime("%I:%M:%S %p"))
        sure = str(rfdevice.rx_code)
        #if sure != switch:
            #print("changed")
        if (sure == bigg and count_long == 0 or sure == hall_way and   
            count_long == 0 or sure == entrance and count_long == 0):
            if lastClick != 0:
                print("living room pressed",  dt)
                my_roomctl.living()
                lastClick = 0  # handled click
                count = 0
                count_long = 0
        elif sure == leo_room:
            if lastClick != 0:
                print("leo_room pressed",  dt)
                my_roomctl.leo()
                lastClick = 0  # handled click
                count = 0
                count_long = 0
        elif sure == my_room:
            if lastClick != 0:
                print("my_room pressed",  dt)
                my_roomctl.bed()
                lastClick = 0  # handled click
                count = 0
                count_long = 0
        time.sleep(1)
        count_long = 0

# create separate thread for state machine
stateMachineThread = threading.Timer(0.5, state_machine )
stateMachineThread.daemon = True
stateMachineThread.start()

def dimm(switch): #state machine 2
    S1 = 1
    S2 = 2
    S3 = 3
    #S4 = 4
    #S5 = 5
    INITIAL_STATE = S1
    state = INITIAL_STATE
    global tag
    tag = 0
#    global safty
    global leo_room,  my_room,  entrance,  hall_way,  bigg,  all_off
    while True:
        dt = (time.strftime("%I:%M:%S %p"))
        time.sleep(0.01)
        global sure
        sure = str(rfdevice.rx_code)
        if state == S1:
            if tag != 0:
                if sure == all_off:
                    print("dimmer func select" , sure)
                    #if sure != switch:
                        #print("code", sure)
                    state = S2
#        print("sure code ", sure)
        if state == S2:
            if tag != 0:
                if sure == bigg:
                    for count_long2 in range(1, 2):
                        print("front room dimmmmmmm",  dt)
                        my_roomctl.living_br2()
                    state = S3
                    #tag = 0
        if state == S2:
            if tag != 0:
                if sure == leo_room:
                    for count_long2 in range(1, 2):
                        print("leo_room dimmming",  dt)
                        my_roomctl.leo_br()
                    state = S3
                    #tag = 0
        if state == S2:
            if tag != 0:
                if sure == my_room:
                    for count_long2 in range(1, 2):
                        print("my_room dimmming",  dt)
                        my_roomctl.bed_br()
                    #tag = 0
                    state = S3
        if state == S3:
            if tag != 0:
                state = S1
                time.sleep(5)
                tag = 0

    return
dimmButtonThread = threading.Timer(0.5, dimm, args=(switch,) )
dimmButtonThread.daemon = True
dimmButtonThread.start()

tag = 0 
sure = 0

def button_pressed_dash(switch):
    global tag
    tag = 1
    #print("button pressed", switch)

safty = 0
while True:
#    global tag
    switch = str(rfdevice.rx_code)
    args = str(rfdevice.rx_code)
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        sure = switch
        if (switch == bigg or  switch == hall_way or switch == entrance 
        or switch == leo_room or switch == my_room):
            if tag == 0:
                button_pressed(switch)
        if switch == all_off:
            button_pressed_dash(switch)


    time.sleep(0.01)
rfdevice.cleanup()
