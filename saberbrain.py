import rp2
import uarray as array
import time
from machine import Pin

global bladeState
global bladeColor

NUM_LEDS = 144 #actually not, 288 in the saber but pixels_set fixes that.
SABERPIN_NUM = 15
BUTTON_NUM = 18

# LED Strip Brightness.  1.0 = 100%   0.0 = 0%  Doesn't seem linear.
brightness = 1.0

button = Pin(BUTTON_NUM, Pin.IN, Pin.PULL_UP)

#Color Definitions
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = ( 255, 127, 0 )
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 0, 255)
BLUE = (0, 0, 128)
#Didn't use this. Indigo looks white-purple.  Pride rainbow flag doesn't have indigo.
#INDIGO = ( 76, 43,195)
PURPLE = (200, 0, 200)
#This will REALLY draw the battery down... try not to use it...
WHITE = (255, 255, 255)

#Trans flag has special Pink color only used there.
TRANSPINK = (247, 58, 54)

## I copied this code from literally any RPiPico WS2812 demo program.
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(SABERPIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
##End Stuff I Copied.

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(288)])
##########################################################################

#Probably some of these functions are borrowed too. I don't recall. 
def pixels_show():
    sm.put(ar, 8)

def pixels_set(i, color):
# here is how we treat the blade as if it has 144 pixels, instead of the 288 it realy has.
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
    ar[287-i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
# Flood Fill, we don't care about up and back, this just sets all values to the same.
    for i in range(288):
        ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def BladeOut(BLADE):
    #I do this in sets of 6 because timing wise it gave the best "out" sense.  No delay needed here due to RPiPico's clocks.
    for i in range(24):
        pixels_set(i*6,BLADE)
        pixels_set(i*6+1,BLADE)
        pixels_set(i*6+2,BLADE)
        pixels_set(i*6+3,BLADE)
        pixels_set(i*6+4,BLADE)
        pixels_set(i*6+5,BLADE)
        pixels_show()

def BladeIn():
    # like above, but backwards, and "black" which is just turning the LED off.
    BLADE=BLACK
    for i in reversed(range(24)):
        pixels_set(i*6,BLADE)
        pixels_set(i*6+1,BLADE)
        pixels_set(i*6+2,BLADE)
        pixels_set(i*6+3,BLADE)
        pixels_set(i*6+4,BLADE)
        pixels_set(i*6+5,BLADE)
        pixels_show()


def ShowTrans():
# Trans Pride Flag pattern
    for i in range(0,28):
        pixels_set(i,BLUE)
    pixels_show()
    for i in range(29,56):
        pixels_set(i,TRANSPINK)
    pixels_show()
    for i in range(57,84):
        pixels_set(i,WHITE)
    pixels_show()
    for i in range(85,112):
        pixels_set(i,TRANSPINK)
    pixels_show()
    for i in range(113,144):
        pixels_set(i,BLUE)
    pixels_show()
    time.sleep(0.2)

def ShowRainbow():
#Rainbow flag, purple at handle, red at tip.
    for i in range(0,24):
        pixels_set(i,PURPLE)
    pixels_show()
    for i in range(25,48):
        pixels_set(i,BLUE)
    pixels_show()
    for i in range(49,72):
        pixels_set(i,GREEN)
    pixels_show()
    for i in range(73,96):
        pixels_set(i,YELLOW)
    pixels_show()
    for i in range(97,120):
        pixels_set(i,ORANGE)
    pixels_show()
    for i in range(121,144):
        pixels_set(i,RED)
    pixels_show()
    time.sleep(0.2)

def toggleBlade():
    # For scope reasons.
    global bladeState
    global bladeColor
# bladeState==1 means the blade is "OUT"  What 0 means, you can work out.
    if bladeState==1:
        BladeIn()
        bladeState=0
    else:
#When 'Extending" the blade, curse micropython for not having switch/case or useful if elseif
        if bladeColor==0:
            BladeOut(BLUE)
            bladeState=1
        if bladeColor==1:
            BladeOut(GREEN)
            bladeState=1
        if bladeColor==2:
            BladeOut(RED)
            bladeState=1
        if bladeColor==3:
            BladeOut(PURPLE)
            bladeState=1
        if bladeColor==4:
            BladeOut(YELLOW)
            bladeState=1
        if bladeColor==5:
            pixels_fill(BLACK)
            pixels_show()
            ShowTrans()
            bladeState=1
        if bladeColor==6:
            pixels_fill(BLACK)
            pixels_show()
            ShowRainbow()
            bladeState=1

maxBlades=6 # If I add more colors/patterns, I have to change this.

## Okay, the "MAIN" starts here.  

# Reset the blade to black
pixels_fill(BLACK)
pixels_show()

#and then go bue to start
bladeState=1
bladeColor=0
BladeOut(BLUE)

changeSkip=1
while True:
    if button.value()== 0: #value is 0 when button is pressed because I used Pin.PULL_UP
        changeSkip=1  # I use ChangeSkip so I know if I am retracting/extending, or just rotating colors.
        start = time.time()
        time.sleep(0.2) # Button Debounce Time.
        while button.value()==0:  #While it is held down...
            time.sleep(0.01) # if this was ASM, this would be a few NOPs to delay a teeny bit.
            templength = time.time() - start
            if templength>=1:  #If button has been held for more than a second
                start=time.time() #Reset timer so it triggers again if held for an additional second, otherwise blades won't "cycle" and you'll have to keep press/hold
                bladeColor=bladeColor+1
                if bladeColor>maxBlades:
                    bladeColor=0
                bladeState=0 # Fake the blade being "in" so that the toggleBlade is reused.
                toggleBlade()
                changeSkip=0 # Blade will be "out" so if you don't do this, once the loop ends the blade will retract
        if changeSkip==1:
            toggleBlade()
        else:  # Reset changeSkip, but I honestly might not need this... I'll test later.
            changeskip=1
