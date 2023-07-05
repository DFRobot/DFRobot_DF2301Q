/*!
 * @file DFRobot_DF2301Q.cpp
 * @brief Implementation of DFRobot_DF2301Q class
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence  The MIT License (MIT)
 * @author  [qsjhyy](yihuan.huang@dfrobot.com)
 * @version  V1.0
 * @date  2022-04-02
 * @url  https://github.com/DFRobot/DFRobot_DF2301Q
 */
#include "DFRobot_DF2301Q.h"

DFRobot_DF2301Q::DFRobot_DF2301Q()
{
}

/**************************************************************************
                          Subclass using I2C interface for communication 
 **************************************************************************/

DFRobot_DF2301Q_I2C::DFRobot_DF2301Q_I2C(TwoWire *pWire, uint8_t i2cAddr)
{
  _pWire = pWire;
  _deviceAddr = i2cAddr;
}

bool DFRobot_DF2301Q_I2C::begin()
{
  _pWire->begin();   // Wire.h(I2C)library function initialize wire library
  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(0x00);
  if(0 != _pWire->endTransmission())
    return false;
  return true;
}

uint8_t DFRobot_DF2301Q_I2C::getCMDID(void)
{
  uint8_t CMDID = 0;
  readReg(DF2301Q_I2C_REG_CMDID, &CMDID);
  delay(50);   // Prevent the access rate from interfering with other functions of the voice module
  return CMDID;
}

void DFRobot_DF2301Q_I2C::playByCMDID(uint8_t CMDID)
{
  writeReg(DF2301Q_I2C_REG_PLAY_CMDID, &CMDID);
  delay(1000);
}

uint8_t DFRobot_DF2301Q_I2C::getWakeTime(void)
{
  uint8_t wakeTime = 0;
  readReg(DF2301Q_I2C_REG_WAKE_TIME, &wakeTime);
  return wakeTime;
}

void DFRobot_DF2301Q_I2C::setWakeTime(uint8_t wakeTime)
{
  writeReg(DF2301Q_I2C_REG_WAKE_TIME, &wakeTime);
}

void DFRobot_DF2301Q_I2C::setVolume(uint8_t vol)
{
  // if (vol < 0)
  //   vol = 0;
  // else if (vol > 20)
  //   vol = 20;
  writeReg(DF2301Q_I2C_REG_SET_VOLUME, &vol);
}

void DFRobot_DF2301Q_I2C::setMuteMode(uint8_t mode)
{
  if (0 != mode)
    mode = 1;
  writeReg(DF2301Q_I2C_REG_SET_MUTE, &mode);
}

void DFRobot_DF2301Q_I2C::writeReg(uint8_t reg, const void* pBuf)
{
  if(pBuf == NULL) {
    DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;

  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(reg);
  _pWire->write(*_pBuf);
  _pWire->endTransmission();
}

size_t DFRobot_DF2301Q_I2C::readReg(uint8_t reg, void* pBuf)
{
  if(NULL == pBuf) {
    DBG("pBuf ERROR!! : null pointer");
  }
  uint8_t * _pBuf = (uint8_t*)pBuf;

  size_t count = 0;

  _pWire->beginTransmission(_deviceAddr);
  _pWire->write(reg);
  if(0 != _pWire->endTransmission(false)) {   // Used Wire.endTransmission() to end a slave transmission started by beginTransmission() and arranged by write().
    DBG("endTransmission ERROR!!");

  } else {
    _pWire->requestFrom(_deviceAddr, (uint8_t)1);   // Master device requests size bytes from slave device, which can be accepted by master device with read() or available()

    while (_pWire->available()) {
      _pBuf[count++] = _pWire->read();   // Use read() to receive and put into buf
      // DBG(_pBuf[count-1], HEX);
    }
    // _pWire->endTransmission();
  }

  return count;
}

/**************************************************************************
                          Subclass using UART interface for communication
 **************************************************************************/

DFRobot_DF2301Q_UART::DFRobot_DF2301Q_UART(HardwareSerial *hardSerial)
{
  
#if !(defined(ARDUINO_SAM_ZERO))   // Initializing the M0 board now will lead to maincontroller program crash
  hardSerial->begin(DF2301Q_UART_BAUDRATE);
#endif
  _ser = hardSerial;
}

#if defined(ARDUINO_AVR_UNO)||defined(ESP8266)
DFRobot_DF2301Q_UART::DFRobot_DF2301Q_UART(SoftwareSerial *softSerial)
{
  softSerial->begin(DF2301Q_UART_BAUDRATE);
  _ser = softSerial;
}
#elif defined(ESP32)
DFRobot_DF2301Q_UART::DFRobot_DF2301Q_UART(HardwareSerial *hardSerial, uint8_t rx, uint8_t tx)
{
  hardSerial->begin(DF2301Q_UART_BAUDRATE, SERIAL_8N1, rx, tx);
  _ser = hardSerial;
}
#endif

bool DFRobot_DF2301Q_UART::begin()
{
#if defined(ARDUINO_SAM_ZERO)   // The M0 board needs to be initialized at this time
  ((HardwareSerial *)_ser)->begin(DF2301Q_UART_BAUDRATE);
#endif

  _sendSequence = 0;

  if(NULL == _ser){
    return false;
  }
  return true;
}

uint8_t DFRobot_DF2301Q_UART::getCMDID(void)
{
  sUartMsg_t msg;
  _uartCmdId = 0;
  recvPacket(&msg);
  return _uartCmdId;
}

void DFRobot_DF2301Q_UART::playByCMDID(uint32_t play_id)
{
    sUartMsg_t msg;

    msg.header = DF2301Q_UART_MSG_HEAD;
    msg.dataLength = 6;
    msg.msgType = DF2301Q_UART_MSG_TYPE_CMD_DOWN;
    msg.msgCmd = DF2301Q_UART_MSG_CMD_PLAY_VOICE;
    msg.msgSeq = _sendSequence++;
    msg.msgData[0] = DF2301Q_UART_MSG_DATA_PLAY_START;
    msg.msgData[1] = DF2301Q_UART_MSG_DATA_PLAY_BY_CMD_ID;
    memcpy(&msg.msgData[2], &play_id, sizeof(uint32_t));

    sendPacket(&msg);
    delay(1000);
}

void DFRobot_DF2301Q_UART::resetModule(void)
{
    sUartMsg_t msg;

    msg.header = DF2301Q_UART_MSG_HEAD;
    msg.dataLength = 5;
    msg.msgType = DF2301Q_UART_MSG_TYPE_CMD_DOWN;
    msg.msgCmd = DF2301Q_UART_MSG_CMD_RESET_MODULE;
    msg.msgSeq = _sendSequence++;
    msg.msgData[0] = 'r';
    msg.msgData[1] = 'e';
    msg.msgData[2] = 's';
    msg.msgData[3] = 'e';
    msg.msgData[4] = 't';

    sendPacket(&msg);
    delay(3000);
}

void DFRobot_DF2301Q_UART::settingCMD(uint8_t setType, uint32_t setValue)
{
    sUartMsg_t msg;

    msg.header = DF2301Q_UART_MSG_HEAD;
    msg.dataLength = 5;
    msg.msgType = DF2301Q_UART_MSG_TYPE_CMD_DOWN;
    msg.msgCmd = DF2301Q_UART_MSG_CMD_SET_CONFIG;
    msg.msgSeq = _sendSequence++;
    msg.msgData[0] = setType;
    memcpy(&msg.msgData[1], &setValue, sizeof(setValue));

    sendPacket(&msg);
}

void DFRobot_DF2301Q_UART::sendPacket(const sUartMsg_t * msg)
{
  if(NULL == msg) {
    DBG("msg ERROR!! : null pointer");
  }
  uint8_t *_pBuf = (uint8_t *)msg;

  while (_ser->available()) {
    _ser->read();
  }

  uint16_t i = 0;
  /*header and data*/
  for(; i<4; i++) {
    _ser->write( _pBuf[i] );
  }

  uint16_t chkSum = 0;
  for(; i<(msg->dataLength + 7); i++) {
    chkSum += _pBuf[i];
    _ser->write( _pBuf[i] );
  }

  /*check sum*/
  _ser->write( chkSum & 0xff );
  _ser->write( (chkSum >> 8) & 0xff );

  /*tail*/
  _ser->write( DF2301Q_UART_MSG_TAIL );

  delay(100);
}

uint8_t DFRobot_DF2301Q_UART::recvPacket(sUartMsg_t * msg)
{
  if(NULL == msg) {
    DBG("msg ERROR!! : null pointer");
  }

  uint8_t revState = REV_STATE_HEAD0, receiveChar;
  uint16_t length0 = 0, length1 = 0;
  uint16_t chkSum0 = 0, chkSum1 = 0;
  uint16_t dataRevCount = 0;

  while(_ser->available()) {
    receiveChar = _ser->read();
    switch(revState) {
      case REV_STATE_HEAD0:
        if(DF2301Q_UART_MSG_HEAD_LOW == receiveChar) {
          revState = REV_STATE_HEAD1;
        }
        break;
      case REV_STATE_HEAD1:
        if(DF2301Q_UART_MSG_HEAD_HIGH == receiveChar) {
          revState = REV_STATE_LENGTH0;
          msg->header = DF2301Q_UART_MSG_HEAD;
        } else {
          if(DF2301Q_UART_MSG_HEAD_LOW != receiveChar) {
            revState = REV_STATE_HEAD0;
          }
        }
        break;
      case REV_STATE_LENGTH0:
        length0 = receiveChar;
        revState = REV_STATE_LENGTH1;
        break;
      case REV_STATE_LENGTH1:
        length1 = receiveChar;
        length1 <<= 8;
        length1 += length0;
        if(length1 <= DF2301Q_UART_MSG_DATA_MAX_SIZE) {
            msg->dataLength = length1;
            revState = REV_STATE_TYPE;
        } else {
            revState = REV_STATE_HEAD0;
        }
        break;
      case REV_STATE_TYPE:
        msg->msgType = receiveChar;
        revState = REV_STATE_CMD;
        break;
      case REV_STATE_CMD:
        msg->msgCmd = receiveChar;
        revState = REV_STATE_SEQ;
        break;
      case REV_STATE_SEQ:
        msg->msgSeq = receiveChar;
        if(length1 > 0) {
            revState = REV_STATE_DATA;
            dataRevCount = 0;
        } else {
            revState = REV_STATE_CKSUM0;
        }
        break;
      case REV_STATE_DATA:
        msg->msgData[dataRevCount] = receiveChar;
        dataRevCount += 1;
        if(dataRevCount == length1) {
            revState = REV_STATE_CKSUM0;
        }
        break;
      case REV_STATE_CKSUM0:
        chkSum0 = receiveChar;
        revState = REV_STATE_CKSUM1;
        break;
      case REV_STATE_CKSUM1:
      {
        uint16_t packetChkSum = 0;
        uint8_t *data = (uint8_t *)msg;
        for(uint16_t i=4; i<(msg->dataLength + 7); i++) {
          packetChkSum += data[i];
        }

        chkSum1 = receiveChar;
        chkSum1 <<= 8;
        chkSum1 += chkSum0;

        /*msg->chksum = chkSum1; just used as judgement*/
        if(chkSum1 == packetChkSum) {
          revState = REV_STATE_TAIL;
        } else {
          revState = REV_STATE_HEAD0;
        }
        break;
      }
      case REV_STATE_TAIL:
        if(receiveChar == DF2301Q_UART_MSG_TAIL) {   /*receive ok*/
          /*msg->tail = receiveChar; just used as judgement*/
          if(DF2301Q_UART_MSG_TYPE_CMD_UP == msg->msgType) {
            _uartCmdId = msg->msgData[0];
            DBG(_uartCmdId, HEX);
          }

        } else {
          dataRevCount = 0;
        }
        revState = REV_STATE_HEAD0;
        break;
      default:
        revState = REV_STATE_HEAD0;
        break;
    }
  }

  return dataRevCount;
}
