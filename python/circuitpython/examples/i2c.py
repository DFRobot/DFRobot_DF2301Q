# -*- coding: utf-8 -*
"""
  @file  i2c.py
  @brief  Control the voice recognition module via I2C
  @n  Get the recognized command ID and play the corresponding reply audio according to the ID;
  @n  Get and set the wake-up state duration, set mute mode, set volume, and enter the wake-up state
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence  The MIT License (MIT)
  @author  [qsjhyy](yihuan.huang@dfrobot.com)
  @version  V1.0
  @date  2022-12-30
  @url https://github.com/DFRobot/DFRobot_DF2301Q
"""

import time
import board
import busio
from DFRobot_DF2301Q import DFRobot_DF2301Q_I2C, DF2301Q_I2C_ADDR
from DFRobot_DF2301Q_Commands import CommandWord

# Initialize I2C bus
i2c = busio.I2C(board.GP21, board.GP20)

# Create instance of the I2C device
DF2301Q = DFRobot_DF2301Q_I2C(i2c, i2c_addr=DF2301Q_I2C_ADDR)

def setup():
    '''
      @brief Set voice volume
      @param vol - Volume
    '''
    DF2301Q.set_volume(15)

    '''
      @brief Set mute mode
      @param mode - Mute mode; set value 1: mute, 0: unmute
    '''
    DF2301Q.set_mute_mode(0)

    '''
      @brief Set wake-up duration
      @param wakeTime - Wake-up duration(0-255)
    '''
    DF2301Q.set_wake_time(20)

    '''
      @brief Get the wake-up duration
      @return The current set wake-up period
    '''
    print("wake_time = %u\n" % (DF2301Q.get_wake_time()))

    '''
      @brief Play the corresponding reply audio according to the command word ID
      @param CMDID - Command word ID
      @note Can enter wake-up state through ID-1 in I2C mode
    '''
    # DF2301Q.play_by_CMDID(CommandWord.HelloRobot)   # Wake-up command
    DF2301Q.play_by_CMDID(CommandWord.Retreat)   # Common word ID

def loop():
    CMDID = DF2301Q.get_CMDID()
    if CMDID != 0:
        print("CMDID = %u\n" % CMDID)
    time.sleep(3)

if __name__ == "__main__":
    setup()
    while True:
        loop()
