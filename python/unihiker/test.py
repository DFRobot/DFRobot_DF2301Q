#  -*- coding: UTF-8 -*-
# Python
# UNIHIKER & Gravity Voice Recognition Module
from pinpong.board import Board,Pin
import time
from DFRobot_DF2301Q import *

Board().begin()
led = Pin(Pin.P24, Pin.OUT)  # Pin initialization to level output

DF2301Q = DFRobot_DF2301Q_I2C()  # Initialize
DF2301Q.set_volume(5)  # Volume
DF2301Q.set_mute_mode(0)  # Set mute
DF2301Q.set_wake_time(20)  # Set wake time
print(DF2301Q.get_wake_time())
DF2301Q.play_by_CMDID(2)
print("----------------------")

while True:
    DF2301Q_CMDID = DF2301Q.get_CMDID()
    time.sleep(0.05)
    if (not DF2301Q_CMDID==0):
        if ((DF2301Q_CMDID) == 5): #The first custom command
            led.value(1)  # Output High Level
            print("1")  # Terminal printing information
        if ((DF2301Q_CMDID) == 6): #The second custom command
            led.value(0)  # Output low level
            print("0")  # Terminal printing information