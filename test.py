#!/usr/bin/env python3
from ev3dev.ev3 import *

from ev3dev2.motor import *
import time

tank     = MoveTank(OUTPUT_A, OUTPUT_B)
csL      = ColorSensor('in2')
us       = UltrasonicSensor('in3')
csR      = ColorSensor('in1')
push     = "? nom du capteur push"
leve     = "? nom du capteur push"
csR.mode = 'COL-COLOR'
csL.mode = 'COL-COLOR'
isGreen  = 0
us.mode  = 'US-DIST-CM'
triangle=False


def bille():
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(15), 1)  
    tank.on_for_seconds(SpeedPercent(-30), SpeedPercent(10), 1,8)    
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(15), 1) 
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(15), 0.5) 
    tank.on_for_seconds(SpeedPercent(15), SpeedPercent(-5), 1,8) 
    while us.value()/10 > 4:
        tank.on(SpeedPercent(15), SpeedPercent(15))
    tank.on_for_seconds(SpeedPercent(-5), SpeedPercent(15), 1,8)#position collé coté droit après entrée dasn bon sens
    #trouver comment dtecter le triangle 


def dejavu():
        if csL.value() == 5 or csR.value() == 5:
            csR.mode = 'RGB-RAW'
            csL.mode = 'RGB-RAW'
            if csR.value()="rouge" or csL.value()="rouge":
                bille()
            else:
                csR.mode='COL-COLOR'
                csL.mode='COL-COLOR'


            

def evitement():
    
    tank.on_for_seconds(SpeedPercent(5), SpeedPercent(5), 1)
    
    tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(5), 1.8)
  
    tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15), 2)
 
    tank.on_for_seconds(SpeedPercent(5), SpeedPercent(-15), 1.8)

    tank.on_for_seconds(SpeedPercent(-20), SpeedPercent(-20), 3)

    tank.on_for_seconds(SpeedPercent(5), SpeedPercent(-15), 1.8)

    tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15), 1.75)

    tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(5), 1.8)

    tank.on_for_seconds(SpeedPercent(20), SpeedPercent(20), 0.75)

def noirD():
    if csR.value() == 1:
        tank.on(SpeedPercent(-40), SpeedPercent(20))
def noirG():
    if csL.value() == 1:
        tank.on(SpeedPercent(20), SpeedPercent(-40))

def follow():
    if csR.value() == 1 or csL.value() == 1:
        noirG()
        noirD()

    elif csR.value()==3:
        csR.mode = 'RGB-RAW'
        if  13 <= csR.value() <= 16:
            tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15), 0.5)
            tank.on_for_seconds(SpeedPercent(-20), SpeedPercent(0), 1.8)
        csR.mode = 'COL-COLOR'

    elif csL.value()==3:
        csL.mode = 'RGB-RAW'
        if 13 <= csL.value() <=16:
            tank.on_for_seconds(SpeedPercent(-15), SpeedPercent(-15), 0.5)
            tank.on_for_seconds(SpeedPercent(0), SpeedPercent(-20), 1.8) 
        csL.mode = 'COL-COLOR'

    elif csL.value() == 5 or csR.value() == 5:
        dejavu()

    else:
        if us.value()/10 <= 4:
            print("evitement")
            evitement()
        tank.on(SpeedPercent(-7), SpeedPercent(-7))



while 1:
    follow()
