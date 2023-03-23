# DFRobot_DF2301Q
* [English Version](./README.md)

1、 Arduino兼容控制器：Arduino Uno、Arduino leonardo、Arduino MEGA、FireBeetle 系列控制器，树莓派，ESP32

2、 通过 Gravity 连接，简化方便，且兼容 3.3V 与 5V

3、 命令词自学习功能：通过语音控制模块学习命令词，可以使用任何音频作为命令

4、 内置150条常用的固定命令词条

5、 模块自带一个喇叭和外接喇叭的接口，能实时语音反馈识别结果

6、 采用I2C和UART两种通讯方式，Gravity接口。

7、 板载电源指示灯（红）和识别状态指示灯（蓝）

8、 双麦克风收音更好的抗噪音能力和更远的识别距离

![产品实物图](./resources/images/DF2301Q.png)


## 产品链接 (https://www.dfrobot.com.cn/)
    SKU: SEN0539


## 目录

* [概述](#概述)
* [库安装](#库安装)
* [方法](#方法)
* [兼容性](#兼容性)
* [历史](#历史)
* [创作者](#创作者)


## 概述

 * 该库可以获取识别的命令ID, 通过命令ID播放其对应的答复音频;
 * 该库也可以获取和设置唤醒状态的持续周期, 设置静音模式, 设置音量, 进入唤醒状态, 复位模块


## 库安装

这里有2种安装方法：

1. 使用此库前，请首先下载库文件，将其粘贴到\Arduino\libraries目录中，然后打开examples文件夹并在该文件夹中运行演示。
2. 直接在Arduino软件库管理中搜索下载 DFRobot_DF2301Q 库。


## 方法

```C++
/**************************************************************************
                          使用 I2C 接口通信的子类
 **************************************************************************/

  /**
   * @fn DFRobot_DF2301Q_I2C
   * @brief 构造器
   * @param pWire I2C总线指针对象，构造设备，可传递参数或不传递参数，默认为Wire
   * @param address 7bits I2C address, the first three bits determine the value of the address, default to 0x50
   * @return None
   */
  DFRobot_DF2301Q_I2C(TwoWire *pWire=&Wire, uint8_t i2cAddr=DF2301Q_I2C_ADDR);

  /**
   * @fn begin
   * @brief 子类init函数
   * @return Bool类型，成功为true，错误为false
   */
  virtual bool begin(void);

  /**
   * @fn getCMDID
   * @brief 获取命令词对应的ID
   * @return 返回获取的命令词ID, 返回0表示未获取到有效id
   */
  uint8_t getCMDID(void);

  /**
   * @fn playByCMDID
   * @brief 根据命令词ID播放对应的答复音
   * @param CMDID - 命令词ID
   * @return None
   * @note i2c模式下, 可通过ID-1进入唤醒状态
   */
  void playByCMDID(uint8_t CMDID);

  /**
   * @fn getWakeTime
   * @brief 获取唤醒持续时间
   * @return 当前设置的唤醒周期
   */
  uint8_t getWakeTime(void);

  /**
   * @fn setWakeTime
   * @brief 设置唤醒持续时间
   * @param wakeTime - 唤醒持续时间(0~255)
   * @return None
   */
  void setWakeTime(uint8_t wakeTime);

  /**
   * @fn setVolume
   * @brief 设置音量
   * @param vol - 音量范围(1~7)
   * @return None
   */
  void setVolume(uint8_t vol);

  /**
   * @fn setMuteMode
   * @brief 设置静音模式
   * @param mode - 静音模式; 设置值 1: mute, 0: unmute
   * @return None
   */
  void setMuteMode(uint8_t mode);

/**************************************************************************
                          使用 UART 接口通信的子类
 **************************************************************************/

  /**
   * @fn DFRobot_DF2301Q_UART
   * @brief  构造器
   * @param serial - 串口通讯, 支持硬串口和软串口
   * @param rx - UART 接收数据的引脚
   * @param tx - UART 发送数据的引脚
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
   * @brief 子类init函数
   * @return Bool类型, 成功为true, 错误为false
   */
  virtual bool begin();

  /**
   * @fn getCMDID
   * @brief 获取命令词对应的ID
   * @return 返回获取的命令词ID, 返回0表示未获取到有效id
   */
  uint8_t getCMDID(void);

  /**
   * @fn playByCMDID
   * @brief 根据命令词id播放答复音频
   * @param play_id - 命令词id
   * @return None
   */
  void playByCMDID(uint32_t play_id);

  /**
   * @fn resetModule
   * @brief 复位模块
   * @return None
   */
  void resetModule(void);

  /**
   * @fn settingCMD
   * @brief 设置模块的命令
   * @param setType - 设置类型
   * @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : 设置音量, 设置值范围1~7
   * @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : 进入唤醒状态; 设置值 0
   * @n       DF2301Q_UART_MSG_CMD_SET_MUTE : 静音模式; 设置值 1: mute, 0: unmute
   * @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : 唤醒持续时间; 设置值范围0~255秒
   * @param setValue - 设置值, 范围参见上述设置类型
   * @return None
   */
  void settingCMD(uint8_t setType, uint32_t setValue);

```


## 兼容性

MCU                | Work Well    | Work Wrong   | Untested    | Remarks
------------------ | :----------: | :----------: | :---------: | :----:
Arduino Uno        |      √       |              |             |
Arduino MEGA2560   |      √       |              |             |
Arduino Leonardo   |      √       |              |             |
FireBeetle-ESP8266 |      √       |              |             |
FireBeetle-ESP32   |      √       |              |             |
FireBeetle-M0      |      √       |              |             |
Micro:bit          |      √       |              |             |


## 历史

- 2022/12/30 - 1.0.0 版本


## 创作者

Written by qsjhyy(yihuan.huang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))

