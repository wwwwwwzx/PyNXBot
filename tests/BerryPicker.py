#Description
#
#

import signal
import sys
sys.path.append('../')

from nxbot import BerryBot

def signal_handler(signal, frame): #CTRL+C handler
    print("Stop request")
    b.stopBot()
    sys.exit(0)

IP = '192.168.1.6' #write the IP of your Switch here
b = BerryBot(IP)

signal.signal(signal.SIGINT, signal_handler)

cycles = input("Do you want a limited number of picking cycles? (y/n): ")
if cycles == 'y' or cycles == 'Y':
    cycles = int(input("Input the max number of picking cycles: "))
else:
    cycles = sys.maxsize

shakes = int(input("How many shakes per cycle? (input the number): "))

b.pause(0.5)
print()

i = 0
while i < cycles:
    b.click('R') #R on Luxray "+1" button
    b.pause(1.2)
    print("Cycle", i+1)
    b.shakeTree()
    b.continueShaking(shakes - 1)
    b.pickEverything()
    b.pause(0.5)
    print()
    i += 1
print(i+1, "cycles completed!")
print()
b.stopBot()
