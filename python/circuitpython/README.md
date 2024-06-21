# DFRobot_DF2301Q

1. Arduino-compatible controllers: Arduino UNO, Arduino Leonardo, Arduino MEGA, FireBeetle series controllers, Raspberry Pi, and ESP32

2. Standard Gravity interface, plug-and-play, and 3.3V & 5V devices compatible

3. Command word self-learning function: learn command words by the voice control module, and any audio can be used as a command

4. Built-in fixed 150 commonly-used command words 

5. The module comes with a speaker and the interface for connecting external speaker, which can give voice feedback of recognition results in real time

6. Adopt I2C & UART (not implemented) communication methods, and Gravity interface.

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

1. Clone the repository<br>

```python
sudo git clone https://github.com/DFRobot/DFRobot_DF2301Q
```

2. Move the associated DFRobot_DF2301Q to the root of your connected CircuitPython device.<br>

3. Copy the code from the associated example to the main.py file for testing to see the device working.

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
```

## History

- 2024/06/19 - Version 1.0.0 released.


## Credits

Original python code written by qsjhyy(yihuan.huang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))