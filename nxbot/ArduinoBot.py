#!/usr/bin/env python3
import serial
import serial.tools.list_ports
from time import sleep
from nxbot import Bot

class ArduinoBot(Bot):
    def __init__(self,serial_port = None,printout = False):
        if serial_port is None:
            serial_port = ArduinoBot.find_port()
            print(f'Using port: {serial_port[0]}')
        self.ser = serial.Serial(serial_port[0], 9600)
        self.buttondelay = 0.1
        self.printout = printout

    @staticmethod
    def find_port():
        ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if p.vid is not None and p.pid is not None
        ]
        if not ports:
            raise IOError('No device found')
        if len(ports) > 1:
            print('Found multiple devices:')
            for p in ports:
                print(p)
        return ports

    def write(self,msg):
        self.ser.write(f'{msg}\r\n'.encode('utf-8'));

    def release(self):
        self.ser.write(b'RELEASE\r\n');

    # Negative or zero duration to hold the button
    def send(self, msg, duration = 0.1):
        if self.printout:
            print(msg)
        self.write(msg);
        if duration > 0:
            sleep(duration)
            self.release();
            sleep(self.buttondelay)

    def close(self):
        self.release();
        sleep(0.5)
        self.ser.close()
        print('Connection closed!')

    # Botton
    def A(self,duration = 0.1):
        self.send('Button A',duration)

    def B(self,duration = 0.1):
        self.send('Button B',duration)

    def X(self,duration = 0.1):
        self.send('Button X',duration)

    def Y(self,duration = 0.1):
        self.send('Button Y',duration)

    def L(self,duration = 0.1):
        self.send('Button L',duration)

    def R(self,duration = 0.1):
        self.send('Button R',duration)

    def ZL(self,duration = 0.1):
        self.send('Button ZL',duration)

    def ZR(self,duration = 0.1):
        self.send('Button ZR',duration)

    # Press down left stick
    def LS(self,duration = 0.1):
        self.send('Button LCLICK',duration)

    # Press down right stick
    def RS(self,duration = 0.1):
        self.send('Button RCLICK',duration)

    # Plus
    def p(self,duration = 0.1):
        self.send('Button PLUS',duration)

    # Minus
    def m(self,duration = 0.1):
        self.send('Button MINUS',duration)

    # Home
    def h(self,duration = 0.1):
        self.send('Button HOME',duration)

    # Capture
    def c(self,duration = 0.1):
        self.send('Button CAPTURE',duration)

    # DPAD
    def l(self,duration = 0.1):
        self.send('HAT LEFT',duration)

    def u(self,duration = 0.1):
        self.send('HAT TOP',duration)

    def r(self,duration = 0.1):
        self.send('HAT RIGHT',duration)

    def d(self,duration = 0.1):
        self.send('HAT BOTTOM',duration)

    # LEFT STICK
    def ls_l(self,duration = 0.1):
        self.send('LX MIN',duration)

    def ls_r(self,duration = 0.1):
        self.send('LX MAX',duration)

    def ls_d(self,duration = 0.1):
        self.send('LY MAX',duration)

    def ls_u(self,duration = 0.1):
        self.send('LY MIN',duration)

    # RIGHT STICK
    def rs_l(self,duration = 0.1):
        self.send('RX MIN',duration)

    def rs_r(self,duration = 0.1):
        self.send('RX MAX',duration)

    def rs_d(self,duration = 0.1):
        self.send('RY MAX',duration)

    def rs_u(self,duration = 0.1):
        self.send('RY MIN',duration)