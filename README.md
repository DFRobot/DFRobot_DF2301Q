# DFRobot_DF2301Q
* [中文版](./README_CN.md)

1. Arduino-compatible controllers: Arduino UNO, Arduino Leonardo, Arduino MEGA, FireBeetle series controllers, Raspberry Pi, and ESP32

2. Standard Gravity interface, plug-and-play, and 3.3V & 5V devices compatible

3. Command word self-learning function: learn command words by the voice control module, and any audio can be used as a command

4. Built-in fixed 150 commonly-used command words 

5. The module comes with a speaker and interface for connecting external speaker, which can give voice feedback of recognition results in real time

6. Adopt I2C & UART communication methods, and Gravity interface.

7. On-board power indicator (red) and recognition status indicator (blue)

8. Dual microphone receiver for better anti-noise ability and farther recognition distance

![Product Image](./resources/images/DF2301Q.png)


## Product Link (https://www.dfrobot.com/)
    SKU: SEN0539


## Table of Contents

* [Summary](#summary)
* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)


## Summary

 * This library can be used to get the recognized command ID and play the corresponding reply audio according to the ID;
 * This library can also be used to get and set the wake-up state duration, set the mute mode/volume, enter wake-up state, and reset the module.


## Installation

There two methods:

1. To use this library, first download the library file, paste it into the \Arduino\libraries directory, then open the examples folder and run the demo in the folder.
2. Search the DFRobot_DF2301Q library from the Arduino Software Library Manager and download it.


## Methods

```C++
/**************************************************************************
                          Subclass using I2C interface for communication
 **************************************************************************/

  /**
   * @fn DFRobot_DF2301Q_I2C
   * @brief Constructor
   * @param pWire I2C bus pointer object, construct the device. You can pass a parameter to it or not, default to be Wire
   * @param address 7bits I2C address, the first three bits determine the value of the address, default to 0x50
   * @return None
   */
  DFRobot_DF2301Q_I2C(TwoWire *pWire=&Wire, uint8_t i2cAddr=DF2301Q_I2C_ADDR);

  /**
   * @fn begin
   * @brief Subclass init function
   * @return Bool type, true for success, false for failure
   */
  virtual bool begin(void);

  /**
   * @fn getCMDID
   * @brief Get the ID corresponding to the command word
   * @return Return the obtained command word ID, returning 0 means no valid ID is obtained
   */
  uint8_t getCMDID(void);

  /**
   * @fn playByCMDID
   * @brief Play the corresponding reply audio according to the command word ID
   * @param CMDID - Command word ID
   * @return None
   * @note Can enter wake-up state through ID-1 in I2C mode
   */
  void playByCMDID(uint8_t CMDID);

  /**
   * @fn getWakeTime
   * @brief Get the wake-up duration
   * @return The current set wake-up period
   */
  uint8_t getWakeTime(void);

  /**
   * @fn setWakeTime
   * @brief Set wake-up duration
   * @param wakeTime - Wake-up duration (0-255)
   * @return None
   */
  void setWakeTime(uint8_t wakeTime);

  /**
   * @fn setVolume
   * @brief Set volume
   * @param vol - Volume range(1-7)
   * @return None
   */
  void setVolume(uint8_t vol);

  /**
   * @fn setMuteMode
   * @brief Set mute mode
   * @param mode - Mute mode; set value 1: mute, 0: unmute
   * @return None
   */
  void setMuteMode(uint8_t mode);

/**************************************************************************
                          Subclass using UART interface for communication
 **************************************************************************/

  /**
   * @fn DFRobot_DF2301Q_UART
   * @brief  Constructor
   * @param serial - Serial communication, support hardware and software serial
   * @param rx - UART  The pin for receiving data
   * @param tx - UART  The pin for transmitting data
   * @return None
   */
  DFRobot_DF2301Q_UART(HardwareSerial *hardSerial);
#if defined(ARDUINO_AVR_UNO)||defined(ESP8266)
  DFRobot_DF2301Q_UART(SoftwareSerial *softSerial);
#elif defined(ESP32)
  DFRobot_DF2301Q_UART(HardwareSerial *hardSerial, uint8_t rx, uint8_t tx);
#endif

  /**
   * @fn begin
   * @brief Subclass init function
   * @return Bool type, true for success, false for failure
   */
  virtual bool begin();

  /**
   * @fn getCMDID
   * @brief Get the ID corresponding to the command word
   * @return Return the obtained command word ID, returning 0 means no valid ID is obtained
   */
  uint8_t getCMDID(void);

  /**
   * @fn playByCMDID
   * @brief Play the corresponding reply audio according to the command word ID
   * @param play_id - Command word ID
   * @return None
   */
  void playByCMDID(uint32_t play_id);

  /**
   * @fn resetModule
   * @brief Reset module
   * @return None
   */
  void resetModule(void);

  /**
   * @fn settingCMD
   * @brief Set commands of the module
   * @param setType - Set type
   * @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : Set volume, the set value range 1-7
   * @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : Enter wake-up state; set value 0
   * @n       DF2301Q_UART_MSG_CMD_SET_MUTE : Mute mode; set value 1: mute, 0: unmute
   * @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : Wake-up duration; the set value range 0-255s
   * @param setValue - Set value, refer to the set type above for the range
   * @return None
   */
  void settingCMD(uint8_t setType, uint32_t setValue);

```


## Compatibility

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | :----:
Arduino Uno        |      √       |              |             |
Arduino MEGA2560   |      √       |              |             |
Arduino Leonardo   |      √       |              |             |
FireBeetle-ESP8266 |      √       |              |             |
FireBeetle-ESP32   |      √       |              |             |
FireBeetle-M0      |      √       |              |             |
Micro:bit          |      √       |              |             |


## History

- 2022/12/30 - Version 1.0.0 released.


## Credits

Written by qsjhyy(yihuan.huang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))

