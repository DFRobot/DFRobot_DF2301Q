# -*- coding: utf-8 -*
""" 
  @file  uart.py
  @brief  Control the voice recognition module via UART
  @n  Get the recognized command ID and play the corresponding reply audio according to the ID;
  @n  Set the wake-up state duration, set mute mode, set volume, enter the wake-up state, and reset the module
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence  The MIT License (MIT)
  @author  [qsjhyy](yihuan.huang@dfrobot.com)
  @version  V1.0
  @date  2022-12-30
  @url https://github.com/DFRobot/DFRobot_DF2301Q
"""
from __future__ import print_function
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from DFRobot_DF2301Q import *

'''
  @brief Module UART communication init
'''
DF2301Q = DFRobot_DF2301Q_UART()

def setup():
  '''
    @brief Reset the module
  '''
  # DF2301Q.reset_module(20)

  '''
    @brief Set commands of the module
    @param set_type - Set type 
    @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : Set volume, the set value range 1-7
    @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : Enter wake-up state; set value 0
    @n       DF2301Q_UART_MSG_CMD_SET_MUTE : Mute mode; set value 1: mute, 0: unmute
    @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : Wake-up duration; the set value range 0-255s
    @param set_value - Set value, refer to the set type above for the range
  '''
  DF2301Q.setting_CMD(DF2301Q_UART_MSG_CMD_SET_MUTE, 0)
  DF2301Q.setting_CMD(DF2301Q_UART_MSG_CMD_SET_VOLUME, 4)
  DF2301Q.setting_CMD(DF2301Q_UART_MSG_CMD_SET_WAKE_TIME, 20)
  # DF2301Q.setting_CMD(DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP, 0)

  '''
    @brief Play the corresponding reply audio according to the command word ID
    @param CMDID - Command word ID
  '''
  DF2301Q.play_by_CMDID(23)


def loop():
  CMDID = DF2301Q.get_CMDID()
  if(0 != CMDID):
    print("CMDID = %u\n" % CMDID)
  time.sleep(2)


if __name__ == "__main__":
  setup()
  while True:
    loop()
