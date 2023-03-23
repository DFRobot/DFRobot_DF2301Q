/*!
 * @file  i2c.ino
 * @brief  Control the voice recognition module via I2C
 * @n  Get the recognized command ID and play the corresponding reply audio according to the ID;
 * @n  Get and set the wake-up state duration, set mute mode, set volume, and enter the wake-up state
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @licence  The MIT License (MIT)
 * @author  [qsjhyy](yihuan.huang@dfrobot.com)
 * @version  V1.0
 * @date  2022-12-30
 * @url  https://github.com/DFRobot/DFRobot_DF2301Q
 */
#include "DFRobot_DF2301Q.h"

//I2C communication
DFRobot_DF2301Q_I2C DF2301Q;

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
   * @brief Set voice volume
   * @param voc - Volume value(1~7)
   */
  DF2301Q.setVolume(4);

  /**
   * @brief Set mute mode
   * @param mode - Mute mode; set value 1: mute, 0: unmute
   */
  DF2301Q.setMuteMode(0);

  /**
   * @brief Set wake-up duration
   * @param wakeTime - Wake-up duration (0-255)
   */
  DF2301Q.setWakeTime(15);

  /**
   * @brief Get wake-up duration
   * @return The currently-set wake-up period
   */
  uint8_t wakeTime = 0;
  wakeTime = DF2301Q.getWakeTime();
  Serial.print("wakeTime = ");
  Serial.println(wakeTime);

  /**
   * @brief Play the corresponding reply audio according to the command word ID
   * @param CMDID - Command word ID
   * @note Can enter wake-up state through ID-1 in I2C mode
   */
  // DF2301Q.playByCMDID(1);   // Wake-up command
  DF2301Q.playByCMDID(23);   // Common word ID

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
  delay(3000);
}
