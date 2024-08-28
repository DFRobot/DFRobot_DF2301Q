# -*- coding: utf-8 -*
""" 
  @file  DFRobot_DF2301Q.py
  @note  DFRobot_DF2301Q Class infrastructure, implementation of underlying methods
  @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence  The MIT License (MIT)
  @author  [qsjhyy](yihuan.huang@dfrobot.com)
  @version  V1.0
  @date  2022-12-30
  @url  https://github.com/DFRobot/DFRobot_DF2301Q
  @date 20230705
  @此代码在原RaspberryPi的代码上调整了i2c读取方式，仅适配行空板(DFR0706)使用

"""
import sys
import time

import array
#import smbus
from pinpong.board import I2C
import serial
import numpy as np

import logging
from ctypes import *


logger = logging.getLogger()
# logger.setLevel(logging.INFO)   # Display all print information
logger.setLevel(logging.FATAL)   # If you don’t want to display too many prints, only print errors, please use this option
ph = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - [%(filename)s %(funcName)s]:%(lineno)d - %(levelname)s: %(message)s")
ph.setFormatter(formatter) 
logger.addHandler(ph)


## i2c address
DF2301Q_I2C_ADDR                  = 0x64

## Address of the register for requesting command word ID
DF2301Q_I2C_REG_CMDID             = 0x02
## Address of the register for playing audio by command word ID
DF2301Q_I2C_REG_PLAY_CMDID        = 0x03
## Register for setting mute mode
DF2301Q_I2C_REG_SET_MUTE          = 0x04
## Register for setting volume
DF2301Q_I2C_REG_SET_VOLUME        = 0x05
## Address of the register for wake-up time
DF2301Q_I2C_REG_WAKE_TIME         = 0x06

# tail
DF2301Q_I2C_MSG_TAIL              = 0x5A

## UART baud rate
DF2301Q_UART_BAUDRATE             = 9600
## Maximum data length of serial data frame
DF2301Q_UART_MSG_DATA_MAX_SIZE    = 8

# header
DF2301Q_UART_MSG_HEAD_LOW         = 0xF4
DF2301Q_UART_MSG_HEAD_HIGH        = 0xF5
DF2301Q_UART_MSG_HEAD             = 0xF5F4
# tail
DF2301Q_UART_MSG_TAIL             = 0xFB
# msg_type
DF2301Q_UART_MSG_TYPE_CMD_UP      = 0xA0
DF2301Q_UART_MSG_TYPE_CMD_DOWN    = 0xA1
DF2301Q_UART_MSG_TYPE_ACK         = 0xA2
DF2301Q_UART_MSG_TYPE_NOTIFY      = 0xA3
# msg_cmd
## Report voice recognition results
DF2301Q_UART_MSG_CMD_ASR_RESULT        = 0x91
## Play local broadcast audio
DF2301Q_UART_MSG_CMD_PLAY_VOICE        = 0x92
## Read the serial number of FLASH
DF2301Q_UART_MSG_CMD_GET_FLASHUID      = 0x93
## Read version number
DF2301Q_UART_MSG_CMD_GET_VERSION       = 0x94
## Reset the voice module
DF2301Q_UART_MSG_CMD_RESET_MODULE      = 0x95
## Settings
DF2301Q_UART_MSG_CMD_SET_CONFIG        = 0x96
## Enter update mode
DF2301Q_UART_MSG_CMD_ENTER_OTA_MODE    = 0x97
## Event notification
DF2301Q_UART_MSG_CMD_NOTIFY_STATUS     = 0x9A
DF2301Q_UART_MSG_CMD_ACK_COMMON        = 0xAA
# if user want add please add form DF2301Q_UART_MSG_CMD_USER_START
DF2301Q_UART_MSG_CMD_USER_START        = 0xB0
# msg_data  msg_cmd:DF2301Q_UART_MSG_CMD_PLAY_VOICE
DF2301Q_UART_MSG_DATA_PLAY_START            = 0x80
DF2301Q_UART_MSG_DATA_PLAY_PAUSE            = 0x81
DF2301Q_UART_MSG_DATA_PLAY_RESUME           = 0x82
DF2301Q_UART_MSG_DATA_PLAY_STOP             = 0x83
DF2301Q_UART_MSG_DATA_PLAY_BY_VOICEID       = 0x90
DF2301Q_UART_MSG_DATA_PLAY_BY_SEMANTIC_ID   = 0x91
DF2301Q_UART_MSG_DATA_PLAY_BY_CMD_ID        = 0x92
# msg_data  msg_cmd:DF2301Q_UART_MSG_CMD_GET_VERSION
## Serial protocol version number
DF2301Q_UART_MSG_DATA_VER_PROTOCOL          = 0x80
## SDK version number
DF2301Q_UART_MSG_DATA_VER_SDK               = 0x81
## ASR component version number
DF2301Q_UART_MSG_DATA_VER_ASR               = 0x82
## Audio pre-processing algorithm version number
DF2301Q_UART_MSG_DATA_VER_PREPROCESS        = 0x83
## Player version number
DF2301Q_UART_MSG_DATA_VER_PLAYER            = 0x84
## App version number
DF2301Q_UART_MSG_DATA_VER_APP               = 0x8A
# msg_data  msg_cmd:DF2301Q_UART_MSG_CMD_NOTIFY_STATUS
DF2301Q_UART_MSG_DATA_NOTIFY_POWERON        = 0xB0
DF2301Q_UART_MSG_DATA_NOTIFY_WAKEUPENTER    = 0xB1
DF2301Q_UART_MSG_DATA_NOTIFY_WAKEUPEXIT     = 0xB2
DF2301Q_UART_MSG_DATA_NOTIFY_PLAYSTART      = 0xB3
DF2301Q_UART_MSG_DATA_NOTIFY_PLAYEND        = 0xB4
# msg_data msg_cmd:DF2301Q_UART_MSG_CMD_SET_CONFIG
DF2301Q_UART_MSG_CMD_SET_VOLUME             = 0x80
DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP        = 0x81
DF2301Q_UART_MSG_CMD_SET_PRT_MID_RST        = 0x82
DF2301Q_UART_MSG_CMD_SET_MUTE               = 0x83
DF2301Q_UART_MSG_CMD_SET_WAKE_TIME          = 0x84
DF2301Q_UART_MSG_CMD_SET_NEEDACK            = 0x90
DF2301Q_UART_MSG_CMD_SET_NEEDSTRING         = 0x91
# ACK error code
DF2301Q_UART_MSG_ACK_ERR_NONE               = 0x00
DF2301Q_UART_MSG_ACK_ERR_CHECKSUM           = 0xff
DF2301Q_UART_MSG_ACK_ERR_NOSUPPORT          = 0xfe


class DFRobot_DF2301Q(object):
  '''!
    @brief Define DFRobot_DF2301Q basic class
  '''

  def __init__(self):
    '''!
      @brief Module init
    '''
    pass


class DFRobot_DF2301Q_I2C(DFRobot_DF2301Q):
  '''!
    @brief Define DFRobot_DF2301Q_I2C basic class
  '''

  def __init__(self, i2c_addr=DF2301Q_I2C_ADDR, bus=0):
    '''!
      @brief Module I2C communication init
      @param i2c_addr - I2C communication address
      @param bus - I2C bus
    '''
    print("2301Q init starts...")
    self._addr = i2c_addr
    try:
        self._i2c = I2C(bus)
    except Exception as e:
        print(f"\nError:PinPong未初始化")
        print(f"Error:{e}\n")
        raise

    super(DFRobot_DF2301Q_I2C, self).__init__()
    print("2301Q init end")

  def get_CMDID(self):
    '''!
      @brief Get the ID corresponding to the command word
      @return Return the obtained command word ID, returning 0 means no valid ID is obtained
    '''
    return self._read_reg(DF2301Q_I2C_REG_CMDID)

  def play_by_CMDID(self, CMDID):
    '''!
      @brief Play the corresponding reply audio according to the command word ID
      @param CMDID - Command word ID
      @note Can enter wake-up state through ID-1 in I2C mode
    '''
    self._write_reg(DF2301Q_I2C_REG_PLAY_CMDID, CMDID)
    time.sleep(1)

  def get_wake_time(self):
    '''!
      @brief Get the wake-up duration
      @return The current set wake-up period
    '''
    return self._read_reg(DF2301Q_I2C_REG_WAKE_TIME)

  def set_wake_time(self, wake_time):
    '''!
      @brief Set wake-up duration
      @param wakeTime - Wake-up duration(0-255)
    '''
    wake_time = wake_time & 0xFF
    self._write_reg(DF2301Q_I2C_REG_WAKE_TIME, wake_time)

  def set_volume(self, vol):
    '''!
      @brief Set voice volume
      @param vol - Volume value(1~7)
    '''
    # if (vol < 0):
    #   vol = 0
    # elif (vol > 20):
    #   vol = 20
    self._write_reg(DF2301Q_I2C_REG_SET_VOLUME, vol)

  def set_mute_mode(self, mode):
    '''!
      @brief Set mute mode
      @param mode - Mute mode; set value 1: mute, 0: unmute
    '''
    if (0 != mode):
      mode = 1
    self._write_reg(DF2301Q_I2C_REG_SET_MUTE, mode)

  def _write_reg(self, reg, data):
    '''!
      @brief writes data to a register
      @param reg - register address
      @param data - written data
    '''
    if isinstance(data, int):
      data = [data]
      #logger.info(data)
    #self._i2c.write_i2c_block_data(self._addr, reg, data)
    #print("write reg:",reg)
    #print("write buf:",data)
    self._i2c.writeto_mem(self._addr, reg, data)

  def _read_reg(self, reg):
    '''!
      @brief read the data from the register
      @param reg - register address
      @return read data
    '''
    #data = self._i2c.read_i2c_block_data(self._addr, reg, 1)
    #print("read reg:",reg)
    data = self._i2c.readfrom_mem_restart_transmission(self._addr, reg, 1)
    if data is None:
        print(f"2301Q reg:{reg},data:{data}")
        return 0
    else:
      return data[0]


# class DFRobot_DF2301Q_UART(DFRobot_DF2301Q):
#   '''!
#     @brief Define DFRobot_DF2301Q_UART basic class
#   '''

#   REV_STATE_HEAD0   = 0x00
#   REV_STATE_HEAD1   = 0x01
#   REV_STATE_LENGTH0 = 0x02
#   REV_STATE_LENGTH1 = 0x03
#   REV_STATE_TYPE    = 0x04
#   REV_STATE_CMD     = 0x05
#   REV_STATE_SEQ     = 0x06
#   REV_STATE_DATA    = 0x07
#   REV_STATE_CKSUM0  = 0x08
#   REV_STATE_CKSUM1  = 0x09
#   REV_STATE_TAIL    = 0x0a

#   class uart_msg():
#     '''!
#       @brief Class for serial data frame struct
#     '''
#     def __init__(self):
#       '''!
#         @brief sensor_status structure init
#       '''
#       self.header = 0
#       self.data_length = 0
#       self.msg_type = 0
#       self.msg_cmd = 0
#       self.msg_seq = 0
#       self.msg_data = [0] * 8

#   def __init__(self):
#     '''!
#       @brief Module UART communication init
#     '''
#     self.uart_cmd_ID = 0
#     self._send_sequence = 0
#     self._ser = serial.Serial("/dev/ttyAMA0", baudrate=DF2301Q_UART_BAUDRATE, bytesize=8, parity='N', stopbits=1, timeout=0.5)
#     if self._ser.isOpen == False:
#       self._ser.open()
#     super(DFRobot_DF2301Q_UART, self).__init__()

#   def get_CMDID(self):
#     '''!
#       @brief Get the ID corresponding to the command word 
#       @return Return the obtained command word ID, returning 0 means no valid ID is obtained
#     '''
#     self._recv_packet()
#     temp = self.uart_cmd_ID
#     self.uart_cmd_ID = 0
#     return temp

#   def play_by_CMDID(self, play_id):
#     '''!
#       @brief Play the corresponding reply audio according to the command word ID
#       @param CMDID - Command word ID
#     '''
#     msg = self.uart_msg()
#     msg.header = DF2301Q_UART_MSG_HEAD
#     msg.data_length = 6
#     msg.msg_type = DF2301Q_UART_MSG_TYPE_CMD_DOWN
#     msg.msg_cmd = DF2301Q_UART_MSG_CMD_PLAY_VOICE
#     msg.msg_seq = self._send_sequence
#     self._send_sequence += 1
#     msg.msg_data[0] = DF2301Q_UART_MSG_DATA_PLAY_START
#     msg.msg_data[1] = DF2301Q_UART_MSG_DATA_PLAY_BY_CMD_ID
#     msg.msg_data[2] = play_id

#     self._send_packet(msg)
#     time.sleep(1)

#   def reset_module(self):
#     '''!
#       @brief Reset the module
#     '''
#     msg = self.uart_msg()
#     msg.header = DF2301Q_UART_MSG_HEAD
#     msg.data_length = 5
#     msg.msg_type = DF2301Q_UART_MSG_TYPE_CMD_DOWN
#     msg.msg_cmd = DF2301Q_UART_MSG_CMD_RESET_MODULE
#     msg.msg_seq = self._send_sequence
#     self._send_sequence += 1
#     msg.msg_data[0] = 'r'
#     msg.msg_data[1] = 'e'
#     msg.msg_data[2] = 's'
#     msg.msg_data[3] = 'e'
#     msg.msg_data[4] = 't'

#     self._send_packet(msg)
#     time.sleep(3)

#   def setting_CMD(self, set_type, set_value):
#     '''!
#       @brief Set commands of the module
#       @param set_type - Set type
#       @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : Set volume, the set value range 1-7
#       @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : Enter wake-up state; set value 0
#       @n       DF2301Q_UART_MSG_CMD_SET_MUTE : Mute mode; set value 1: mute, 0: unmute
#       @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : Wake-up duration; the set value range 0-255s
#       @param set_value - Set value, refer to the set type above for the range
#     '''
#     msg = self.uart_msg()
#     msg.header = DF2301Q_UART_MSG_HEAD
#     msg.data_length = 5
#     msg.msg_type = DF2301Q_UART_MSG_TYPE_CMD_DOWN
#     msg.msg_cmd = DF2301Q_UART_MSG_CMD_SET_CONFIG
#     msg.msg_seq = self._send_sequence
#     self._send_sequence += 1
#     msg.msg_data[0] = set_type
#     msg.msg_data[1] = set_value

#     self._send_packet(msg)

#   def _send_packet(self, msg):
#     '''
#       @brief Write data through UART
#       @param msg - Data packet to be sent
#     '''
#     chk_sum = 0x0000
#     data = []
#     data.append(msg.header & 0xFF)
#     data.append((msg.header >> 8) & 0xFF)
#     data.append(msg.data_length & 0xFF)
#     data.append((msg.data_length >> 8) & 0xFF)
#     data.append(msg.msg_type & 0xFF)
#     chk_sum += msg.msg_type
#     data.append(msg.msg_cmd & 0xFF)
#     chk_sum += msg.msg_cmd
#     data.append(msg.msg_seq & 0xFF)
#     chk_sum += msg.msg_seq
#     for i in range(0, msg.data_length):
#       data.append(msg.msg_data[i] & 0xFF)
#       chk_sum += msg.msg_data[i]
#     data.append(chk_sum & 0xFF)
#     data.append((chk_sum >> 8) & 0xFF)
#     data.append(DF2301Q_UART_MSG_TAIL & 0xFF)
#     logger.info(data)
#     self._ser.write(data)
#     time.sleep(0.1)

#   def _recv_packet(self):
#     '''
#       @brief Read data through UART
#       @param msg - Buffer for receiving data packet
#     '''
#     msg = self.uart_msg()
#     rev_state = self.REV_STATE_HEAD0
#     receive_char = 0
#     chk_sum = 0
#     data_rev_count = 0
#     while self._ser.in_waiting:
#       receive_char = ord(self._ser.read(1))
#       if(self.REV_STATE_HEAD0 == rev_state):
#         if(DF2301Q_UART_MSG_HEAD_LOW == receive_char):
#           rev_state = self.REV_STATE_HEAD1
#       elif(self.REV_STATE_HEAD1 == rev_state):
#         if(DF2301Q_UART_MSG_HEAD_HIGH == receive_char):
#           rev_state = self.REV_STATE_LENGTH0
#           msg.header = DF2301Q_UART_MSG_HEAD
#         else:
#           rev_state = self.REV_STATE_HEAD0
#       elif(self.REV_STATE_LENGTH0 == rev_state):
#         msg.data_length = receive_char
#         rev_state = self.REV_STATE_LENGTH1
#       elif(self.REV_STATE_LENGTH1 == rev_state):
#         msg.data_length += receive_char << 8
#         rev_state = self.REV_STATE_TYPE
#       elif(self.REV_STATE_TYPE == rev_state):
#         msg.msg_type = receive_char
#         rev_state = self.REV_STATE_CMD
#       elif(self.REV_STATE_CMD == rev_state):
#         msg.msg_cmd = receive_char
#         rev_state = self.REV_STATE_SEQ
#       elif(self.REV_STATE_SEQ == rev_state):
#         msg.msg_seq = receive_char
#         rev_state = rev_state
#         if(msg.data_length > 0):
#           rev_state = self.REV_STATE_DATA
#           data_rev_count = 0
#         else:
#           rev_state = self.REV_STATE_CKSUM0
#       elif(self.REV_STATE_DATA == rev_state):
#         msg.msg_data[data_rev_count] = receive_char
#         data_rev_count += 1
#         if(msg.data_length == data_rev_count):
#           rev_state = self.REV_STATE_CKSUM0
#       elif(self.REV_STATE_CKSUM0 == rev_state):
#         chk_sum = receive_char
#         rev_state = self.REV_STATE_CKSUM1
#       elif(self.REV_STATE_CKSUM1 == rev_state):
#         chk_sum += receive_char << 8

#         rev_state = self.REV_STATE_TAIL
#       elif(self.REV_STATE_TAIL == rev_state):
#         if(DF2301Q_UART_MSG_TAIL == receive_char):
#           if(DF2301Q_UART_MSG_TYPE_CMD_UP == msg.msg_type):
#             self.uart_cmd_ID = msg.msg_data[0]
#         else:
#           data_rev_count = 0
#         rev_state = self.REV_STATE_HEAD0
#       else:
#         rev_state = self.REV_STATE_HEAD0

#     return data_rev_count
