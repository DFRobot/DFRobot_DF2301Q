/*!
 * @file uart.ino
 * @brief  Control the voice recognition module via UART
 * @n  Get the recognized command ID and play the corresponding reply audio according to the ID;
 * @n  Set the wake-up state duration, set mute mode, set volume, enter the wake-up state, and reset the module
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence  The MIT License (MIT)
 * @author  [qsjhyy](yihuan.huang@dfrobot.com)
 * @version  V1.0
 * @date  2022-12-30
 * @url  https://github.com/DFRobot/DFRobot_DF2301Q
 */
#include "DFRobot_DF2301Q.h"

/**
 * @brief DFRobot_URM13_RTU constructor
 * @param serial - serial ports for communication, supporting hard and soft serial ports
 * @param rx - UART The pin for receiving data
 * @param tx - UART The pin for transmitting data
 */
#if (defined(ARDUINO_AVR_UNO) || defined(ESP8266))   // Use software serial
  SoftwareSerial softSerial(/*rx =*/4, /*tx =*/5);
  DFRobot_DF2301Q_UART DF2301Q(/*softSerial =*/&softSerial);
#elif defined(ESP32)   // Use the hardware serial with remappable pin: Serial1
  DFRobot_DF2301Q_UART DF2301Q(/*hardSerial =*/&Serial1, /*rx =*/D3, /*tx =*/D2);
#else   // Use hardware serial: Serial1
  DFRobot_DF2301Q_UART DF2301Q(/*hardSerial =*/&Serial1);
#endif

void setup()
{
  Serial.begin(115200);

  // Init the sensor
  while( !( DF2301Q.begin() ) ) {
    Serial.println("Communication with device failed, please check connection");
    delay(3000);
  }
  Serial.println("Begin ok!");

  /**
   * @brief Reset the module
   */
  // DF2301Q.resetModule();

  /**
   * @brief Set commands of the module
   * @param setType - Set type
   * @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : Set volume, the set value range 1-7 
   * @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : Enter wake-up state; set value 0
   * @n       DF2301Q_UART_MSG_CMD_SET_MUTE : Mute mode; set value 1: mute, 0: unmute
   * @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : Wake-up duration; the set value range 0-255s
   * @param setValue - Set value, refer to the set type above for the range
   */
//  DF2301Q.settingCMD(DF2301Q_UART_MSG_CMD_SET_MUTE, 0);
//  DF2301Q.settingCMD(DF2301Q_UART_MSG_CMD_SET_VOLUME, 5);
//  DF2301Q.settingCMD(DF2301Q_UART_MSG_CMD_SET_WAKE_TIME, 20);
  // DF2301Q.settingCMD(DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP, 0);

  /**
   * @brief Play the corresponding reply audio according to the command word ID
   * @param CMDID - Command word ID
   */
  DF2301Q.playByCMDID(23);

}

void loop()
{
  /**
   * @brief Get the ID corresponding to the command word 
   * @return Return the obtained command word ID, returning 0 means no valid ID is obtained
   */
  uint8_t CMDID = 0;
  CMDID = DF2301Q.getCMDID();
  if(0 != CMDID) {
    Serial.print("CMDID = ");
    Serial.println(CMDID);
  }
  delay(2000);
}
