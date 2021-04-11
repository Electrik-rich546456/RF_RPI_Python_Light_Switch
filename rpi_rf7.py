#!/usr/bin/env python3
import signal
import sys
import time
import threading

from rpi_rf import RFDevice
#global bigg, timestamp, rfdevice,  lastClick

rfdevice = None
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exithandler)

rfdevice = RFDevice(gpio=27)
rfdevice.enable_rx()
print(rfdevice)
timestamp = None

bigg = '3764961'

#
#def button_pressed_dash():
#    global lastClick
#    lastClick = time.time()
#    print("button pressed")
#    return 
#
###When the button is clicked, do this and ONLY this:
##
##global lastClick
##lastClick = time.time()
##
#
#
#lastClick = 0
#
#
#
#def state_machine():
#    STATE1 = 1
#    STATE2 = 2
#    INITIAL_STATE = STATE1
#    DEBOUNCE_SECONDS = 1
#
#    state = INITIAL_STATE 
#    global lastClick
#    lastClick = 0 # wait for next button click
#    while True:
#        elapsed = time.time() - lastClick
#        ###### state definitions and transitions
#        if state == STATE1:  # STATE1 actions and transitions
#            if lastClick != 0 and elapsed > DEBOUNCE_SECONDS:
#                print("on")
#                lastClick = 0  # we handled click
#                state = STATE2  # goto STATE2
#        elif state == STATE2:  # STATE2 actions and transitions
#            if lastClick != 0 and elapsed > DEBOUNCE_SECONDS:
#                print("off")
#                lastClick = 0  # we handled click
#                state = INITIAL_STATE  
#        ##### transitions common to all states
#        time.sleep(0.1)  # let the processor do other stuff


switch = str(rfdevice.rx_code)
sig = rfdevice.rx_code_timestamp
print(sig)
print("time before", timestamp)
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        print("time in loop", timestamp)
        if switch == bigg:
            print(switch)
#            stateMachineThread = threading.Timer(0.1, state_machine)
#            stateMachineThread.daemon = True
#            stateMachineThread.start()
#    
#            button_pressed_dash()
rfdevice.cleanup()
