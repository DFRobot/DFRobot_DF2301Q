# DFRobot_DF2301Q
* [中文版](./README_CN.md)

1. Arduino-compatible controllers: Arduino UNO, Arduino Leonardo, Arduino MEGA, FireBeetle series controllers, Raspberry Pi, and ESP32

2. Standard Gravity interface, plug-and-play, and 3.3V & 5V devices compatible

3. Command word self-learning function: learn command words by the voice control module, and any audio can be used as a command

4. Built-in fixed 150 commonly-used command words 

5. The module comes with a speaker and the interface for connecting external speaker, which can give voice feedback of recognition results in real time

6. Adopt I2C & UART communication methods, and Gravity interface.

7. On-board power indicator (red) and recognition status indicator (blue)

8. Dual microphone receiver for better anti-noise ability and farther recognition distance

![Product Photo Show](../../resources/images/DF2301Q.png)


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

 * This library can be used to get the recognized command ID, and play the corresponding reply audio according to the ID;
 * This library can also be used to get and set the wake-up state duration, set mute mode, set volume, enter wake-up state, and reset the module


## Installation

1. Download the library to Raspberry Pi first before use.<br>

```python
sudo git clone https://github.com/DFRobot/DFRobot_DF2301Q
```

2. Open and run the routine. To execute a routine demo_x.py, enter python demo_x.py in the command line. For example, to execute the routine i2c.py, you need to enter:<br>

```python
python i2c.py
or 
python2 i2c.py
or 
python3 i2c.py
```


## Methods

```python
"""#################################################################
                        Subclass using I2C interface for communication
#################################################################"""

    '''!
      @brief Get the ID corresponding to the command word
      @return Return the obtained command word ID, returning 0 means no valid ID is obtained
    '''
    def get_CMDID(self):

    '''!
      @brief Play the corresponding reply audio according to the command word ID
      @param CMDID - Command word ID
      @note Can enter wake-up state through ID-1 in I2C mode
    '''
    def play_by_CMDID(self, CMDID):

    '''!
      @brief Get the wake-up duration
      @return The current set wake-up period
    '''
    def get_wake_time(self):

    '''!
      @brief Set wake-up duration
      @param wakeTime - Wake-up duration(0-255)
    '''
    def set_wake_time(self, wake_time):

    '''!
      @brief Set volume
      @param vol - Volume range(1-7)
    '''
    def set_volume(self, vol):

    '''!
      @brief Set mute mode
      @param mode - Mute mode; set value 1: mute, 0: unmute
    '''
    def set_mute_mode(self, mode):

"""#################################################################
                        Subclass using UART interface for communication
#################################################################"""

    '''!
      @brief Get the ID corresponding to the command word
      @return Return the obtained command word ID, returning 0 means no valid ID is obtained
    '''
    def get_CMDID(self):

    '''!
      @brief Play the corresponding reply audio according to the command word ID
      @param CMDID - Command word ID
    '''
    def play_by_CMDID(self, play_id):

    '''!
      @brief Reset the module
    '''
    def reset_module(self):

    '''!
      @brief Set commands of the module
      @param set_type - Set type
      @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : Set volume, the set value range 1-7
      @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : Enter wake-up state; set value 0 
      @n       DF2301Q_UART_MSG_CMD_SET_MUTE : Mute mode; set value 1: mute, 0: unmute
      @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : Wake-up duration; the set value range 0-255s
      @param set_value - Set value, refer to the set type above for the range
    '''
    def setting_CMD(self, set_type, set_value):

```


## Compatibility

* RaspberryPi Version

| Board        | Work Well | Work Wrong | Untested | Remarks |
| ------------ | :-------: | :--------: | :------: | ------- |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |

* Python Version

| Python  | Work Well | Work Wrong | Untested | Remarks |
| ------- | :-------: | :--------: | :------: | ------- |
| Python2 |     √     |            |          |         |
| Python3 |     √     |            |          |         |


## History

- 2022/12/30 - Version 1.0.0 released.


## Credits

Written by qsjhyy(yihuan.huang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))

