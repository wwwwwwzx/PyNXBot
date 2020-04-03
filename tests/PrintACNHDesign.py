Filename = "Images/129s.png"
import sys
sys.path.append('../')
from lookups import Util
from nxbot import ACNHBot,ArduinoBot

hsvarray = Util.convertImage(Filename)
colorlist , hsvarray = Util.generatePallete(hsvarray,size = 32)
a = ArduinoBot()
a.attach()

b = ACNHBot(a)

b.ResetCanvas(Pro = True)
b.SetPalette(colorlist)
b.PrintDesign(hsvarray)

a.detach()