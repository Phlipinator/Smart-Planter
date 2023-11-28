from asyncio import run
from dfplayer import DFPlayer
from machine import Pin, ADC
from time import sleep
import random

############ Variables ############
# the number of files on the SD card
files = 2

# time amount of seconds you want to wait after a sound was made
timer = 5

############ Start ############

# Initialize PIR sensor with Pin 5
pir = Pin(5, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor

# Initialize moisture sensor with Pin 12
moisture_pin = Pin(12, Pin.IN)
adc = ADC(moisture_pin, atten=ADC.ATTN_11DB)

# Initialize DFPlayer with UART2
df = DFPlayer(2)
df.init()

############ Functions ############
    
async def playSound():
    await df.wait_available() # Optional, make sure DFPlayer is booted.

    # setting volume to 15 of 30
    await df.volume(15)
    #print("DFPlayer reports volume:", await df.volume())

    rnd = random.randint(1, files)
    await df.play(1, rnd)
    print("playing file " + str(rnd))


while True:
    pirVal = pir.value()
    mv = adc.read_uv() // 1000
    print("current moisture lvl: " + str(mv))
    
    if pirVal == 1 and mv > 2300:
        run(playSound())
        sleep(timer)
    sleep(1)