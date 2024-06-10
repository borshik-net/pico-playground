#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import Pin, I2C
from struct import pack
import time

class SCRI2C:
    
    def __init__(self, scl=Pin(21), sda=Pin(20), freq=100_000, address=0x47, debug=False):
        self.i2c = I2C(0, scl=scl, sda=sda, freq=freq, timeout=50_000)
        self.address = address
        self.debug = debug
    
    def I2C_SendWord(self, reg, value):
        data = pack(">BH", reg, value)
        if(self.debug):
            print("i2c.writeto(" + hex(self.address) + ", " + hex(data[0]) + ", " + hex(data[1]) + ", " + hex(data[2]) + ")")
        self.i2c.writeto(self.address, data)
        time.sleep(0.001)
    
    def SetMode(self, Mode):
        self.I2C_SendWord(0x01, Mode)

    def ChannelEnable(self, Channel):
        self.I2C_SendWord(0x02, Channel)
            
    def VoltageRegulation(self, Channel,  Angle):
        if(Channel == 1):
            self.I2C_SendWord(0x03, Angle)
        elif(Channel == 2):
            self.I2C_SendWord(0x04, Angle)
        
    def GridFrequency(self, Hz):
        if(Hz == 50 or Hz ==60):
            self.I2C_SendWord(0x05, Hz)
        
    def Reset(self, Delay):
        self.I2C_SendWord(0x06, Delay);
    
       
def cycle(scr, cycles=360, step=5, delay=0.01):       
    scr.SetMode(0x01)
    scr.GridFrequency(50)
    scr.VoltageRegulation(1,0)
    scr.VoltageRegulation(2,0)
    scr.ChannelEnable(0x03)
  
    angle = 0;
    i = cycles
    while(i > 0):
        i = i-1
        time.sleep(delay)
        if(angle<180):
            if(scr.debug):
                print("angle="+str(angle%180))
            scr.VoltageRegulation(1,angle%180)
            scr.VoltageRegulation(2,angle%180)
        else :
            if(scr.debug):
                print("angle="+str(180 - angle%180))
            scr.VoltageRegulation(1,180 - angle%180)
            scr.VoltageRegulation(2,180 - angle%180)
        angle = angle+step
        if(angle>360):
            angle = 0
    
def cleanup(scr):
    scr.VoltageRegulation(1,0)
    scr.VoltageRegulation(2,0)
    scr.ChannelEnable(0x00)
    
    
scr = SCRI2C(debug=True)
cycle(scr, cycles=360, step=1, delay=0.01)
cleanup(scr)
    
    
     



