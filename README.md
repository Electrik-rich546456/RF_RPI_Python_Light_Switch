# RF_RPI_Python_Light_Switch
RF control code to switch Tinytuya smart lights.

This is my first published project smashed together.
You can recycle a bunch of old RF 433/315MHz (ref1) to use with my RPI to control smart lights (lg1) with (rfmod1).

I created a few diffrent versions it the attempt to do what i wanted but could not figur out how to make it work.

I wanted to make it reduce the brightness of the bulbs from a long press but I couldnt get It to work as I wanted. It would dim the lights and then turn them off.

so insted I made it turn the lights on and off. 
It also listen for a specific button press that selects the dimmer function then waits for one of the buttons defined to lights to be pressed then dims that light.

Apologies if this is a little hard to read I dont know how to embed links on here.

Things needed:-

(rfmod1) https://pypi.org/project/rpi-rf/

(lg1) https://www.amazon.co.uk/gp/product/B08BRCMXRN/ref=ox_sc_act_title_3?smid=A2PBGKQKFNUGZL&psc=1

https://pypi.org/project/tinytuya/


ref
(ref1) (https://www.amazon.co.uk/gp/product/B08WWRX871/ref=ox_sc_act_title_2?smid=A3Q9UOBR54VJ36&psc=1)
