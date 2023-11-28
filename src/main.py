from asyncio import run
from dfplayer import DFPlayer
from machine import Pin, ADC
from time import sleep
import random

############ Parameters ############
# The number of files on the SD card
files = 2

# The amount of seconds you want to wait after a sound was made
timer = 5

# The moisture threshold (you may need to play around with this a little)
threshold = 2300

############ Start ############

# Initialize PIR sensor with Pin 5
pir = Pin(5, Pin.IN, Pin.PULL_UP)

# Initialize moisture sensor with Pin 12
moisture_pin = Pin(12, Pin.IN)
adc = ADC(moisture_pin, atten=ADC.ATTN_11DB)

# Initialize DFPlayer with UART2
df = DFPlayer(2)
df.init()

############ Functions ############
    
async def playSound(folder, file):
    await df.wait_available() # Optional, make sure DFPlayer is booted.

    # setting volume to 15 of 30
    await df.volume(15)

    await df.play(folder, file)

def main():
    while True:
        try:
            pirVal = pir.value()
            mv = adc.read_uv() // 1000
            
            if pirVal == 1 and mv > threshold:
                rnd = random.randint(1, files)
                run(playSound(1, rnd))
                sleep(timer)
            sleep(1)
        except:
            print("Error")

############ Execution ############
            
# Play Sound after init is complete
run(playSound(2, 1))
sleep(3)
run(main())