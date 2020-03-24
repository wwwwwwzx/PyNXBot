from time import sleep
from abc import ABC, abstractmethod 

class Bot(ABC):
    # Botton
    def A(self,duration = 0.1):
        pass
    def B(self,duration = 0.1):
        pass
    def X(self,duration = 0.1):
        pass
    def Y(self,duration = 0.1):
        pass
    def L(self,duration = 0.1):
        pass
    def R(self,duration = 0.1):
        pass
    def ZL(self,duration = 0.1):
        pass
    def ZR(self,duration = 0.1):
        pass
    # Press down left stick
    def LS(self,duration = 0.1):
        pass
    # Press down right stick
    def RS(self,duration = 0.1):
        pass
    # Plus
    def p(self,duration = 0.1):
        pass
    # Minus
    def m(self,duration = 0.1):
        pass
    # Home
    def h(self,duration = 0.1):
        pass
    # Capture
    def c(self,duration = 0.1):
        pass
    # DPAD
    def l(self,duration = 0.1):
        pass
    def u(self,duration = 0.1):
        pass
    def r(self,duration = 0.1):
        pass
    def d(self,duration = 0.1):
        pass

    # LEFT STICK
    def ls_l(self,duration = 0.1):
        pass
    def ls_r(self,duration = 0.1):
        pass
    def ls_d(self,duration = 0.1):
        pass
    def ls_u(self,duration = 0.1):
        pass

    # RIGHT STICK
    def rs_l(self,duration = 0.1):
        pass
    def rs_r(self,duration = 0.1):
        pass
    def rs_d(self,duration = 0.1):
        pass
    def rs_u(self,duration = 0.1):
        pass

    def pause(self,duration):
        sleep(duration)

    def quit_app(self):
        self.h()
        sleep(0.5)
        self.X()
        self.A()

    def enter_app(self):
        self.A()
        sleep(1)
        self.A()

    def unlock(self):
        self.A()
        sleep(2)
        self.A()
        self.A()
        self.A()

    def sleepmode(self):
        self.h()
        sleep(0.5)
        self.d()
        self.r(0.7)
        self.A()
        sleep(0.5)
        self.A()
        print('Switch entering sleep mode')

    def attach(self):
        self.LS()
        self.A()
        self.h()
        sleep(1)
        self.A()
        sleep(2)

    def detach(self):
        self.h()
        self.pause(1)
        self.d()
        for jj in range(3):
            self.r()
        self.A()
        self.pause(1)
        self.A()

class ACNHBot():
    def __init__(self, bot = None):
        if isinstance(bot , Bot):
            self.bot = bot

    def ResetCanvas(self, Pro = False):
        b = self.bot
        if Pro:
            b.L() 
            b.L()
            b.L() # White
        else:
            b.L() # Transparent

        b.X() # Tool
        b.d()
        b.d()
        b.d()
        b.d()
        b.A()
        b.A() # Clear Canvas

        b.X()
        b.u()
        b.u()
        b.u()
        b.u()
        b.A() # Choose pen

        b.l(3) # Move cursor to top-left
        b.u(3)

        if Pro:
            b.L() # Black

    def SetPalette(self, colorlist):
        b = self.bot
        if len(colorlist) > 15:
            print("Too many colors")
        b.X()
        b.u()
        b.r()
        b.A()
        b.pause(0.5)
        for ii in range(len(colorlist)):
            if ii > 0:
                b.L()
            b.l(2)
            b.d()
            b.l(2)
            b.d()
            b.l(2)
            b.d()
            C = colorlist[ii]
            for V in C:
                for jj in range(V):
                    b.r()
                b.d()
        b.A()
        b.pause(0.5)
        b.B()
        for ii in range(1,len(colorlist)):
            b.R()

    def MoveToNextPixel(self, direction):
        if direction > 0:
            self.bot.r()
        else:
            self.bot.l()

    def Move2NextRow(self):
        self.bot.d()

    def PrintPIX(self):
        self.bot.A()

    def ChooseColor(self, last_hsv, hsv):
        Diff = int(last_hsv[4] - hsv[4])
        if Diff > 0:
            for jj in range(Diff):
                self.bot.R()
        else:
            for jj in range(-Diff):
                self.bot.L()

    def PrintDesign(self, hsv_array):
        h , w , d = hsv_array.shape
        direction = +1
        last_hsv = [0,0,0,255,0]
        for r in range(h):
            if not hsv_array[r,:,3].any(): # Skip transparent row
                self.Move2NextRow()
                continue
            for ii in range(w):
                if direction < 0:
                    c = w - ii - 1
                else:
                    c = ii
                hsv = hsv_array[r,c]
                if hsv[3] == 0: # Skip transparent pixel
                    if ii < w - 1:
                        self.MoveToNextPixel(direction)
                    continue
                self.ChooseColor(last_hsv,hsv)
                last_hsv = hsv
                self.PrintPIX()
                if ii < w - 1:
                    self.MoveToNextPixel(direction)
            self.Move2NextRow()
            direction = - direction