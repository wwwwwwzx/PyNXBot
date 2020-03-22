Filename = "Images/176s.png"

import sys
sys.path.append('../')
from lookups import Util
from nxbot import ACNHBot,ArduinoBot

hsvarray = Util.convertImage(Filename)
colorlist , hsvarray = Util.generatePallete(hsvarray)
a = ArduinoBot()
a.attach()

b = ACNHBot(a)

b.ResetCanvas()
b.SetPalette(colorlist)
b.PrintDesign(hsvarray)

a.detach()