# Go to root/test of PyNXBot
import signal
import sys
import json
sys.path.append('../')

from nxbot import BDSPIDsBot

config = json.load(open("../config.json"))
b = BDSPIDsBot(config["IP"])

def signal_handler(signal, advances): #CTRL+C handler
    print("Stop request")
    b.moveStick("RIGHT",x=0,y=0)
    b.close()

signal.signal(signal.SIGINT, signal_handler)

def openSecondMenu():
    print(f"Cycle: {n}")
    print("Opening second menu...")
    b.click("A")
    b.pause(1)
    b.moveStick("RIGHT",x=0,y=-32767)
    b.pause(0.3)
    b.moveStick("RIGHT",x=0,y=0)
    b.pause(0.2)
    b.click("X")
    b.pause(1.5)

    b.click("A")
    b.pause(2)
    b.click("R")
    b.pause(2.5)
    b.click("X")
    b.pause(1)

def getHeldItem():
    slot = j + 1 if i % 2 == 0 else 7 - (j + 1)
    print(f"Getting item in Line {i + 1} Slot {slot}")
    b.click("A")
    b.pause(0.6)
    b.moveStick("RIGHT",x=0,y=-32767)
    b.pause(0.3)
    b.moveStick("RIGHT",x=0,y=0)
    b.pause(0.2)
    b.click("A")
    b.pause(0.6)
    b.click("A")
    b.pause(0.8)
    b.click("A")
    b.pause(0.5)

def moveToNextSlot(line):
    rightStickValue = 32767 if line % 2 == 0 else -32767
    b.moveStick("RIGHT",x=rightStickValue,y=0)
    b.pause(0.3)
    b.moveStick("RIGHT",x=0,y=0)
    b.pause(0.2)

def moveToNextLine():
    b.moveStick("RIGHT",x=0,y=-32767)
    b.pause(0.5)
    b.moveStick("RIGHT",x=0,y=0)

def goBackToFirstMenu():
    print("Going back to first menu...\n")
    for i in range(3):
        b.click("B")
        b.pause(2)
    b.click("A")
    b.pause(2)
    b.click("B")
    b.pause(2.3)

cycles = input("Do you want a limited number of cloning cycles? (y/n): ")
if cycles == 'y' or cycles == 'Y':
    cycles = int(input("Input the max number of cloning cycles: "))
else:
    cycles = sys.maxsize

print()
b.pause(0.5)

n = 1
while n <= cycles:
    openSecondMenu()
    for i in range(5):
        for j in range(6):
            getHeldItem()
            if j != 5:
                moveToNextSlot(i)
        if i != 4:
            moveToNextLine()

    goBackToFirstMenu()
    n += 1

print(f"{n} Cycles completed!")
print()
b.close()
