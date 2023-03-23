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

![产品实物图](../../resources/images/DF2301Q.png)


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

1. 下载库至树莓派，要使用这个库，首先要将库下载到Raspberry Pi，命令下载方法如下:<br>
```python
sudo git clone https://github.com/DFRobot/DFRobot_DF2301Q
```
2. 打开并运行例程，要执行一个例程demo_x.py，请在命令行中输入python demo_x.py。例如，要执行 i2c.py例程，你需要输入:<br>

```python
python i2c.py 
或 
python2 i2c.py 
或 
python3 i2c.py
```


## 方法

```python
"""#################################################################
                        使用 I2C 接口通信的子类
#################################################################"""

    '''!
      @brief 获取命令词对应的ID
      @return 返回获取的命令词ID, 返回0表示未获取到有效id
    '''
    def get_CMDID(self):

    '''!
      @brief 根据命令词ID播放对应的答复音
      @param CMDID - 命令词ID
      @note i2c模式下, 可通过ID-1进入唤醒状态
    '''
    def play_by_CMDID(self, CMDID):

    '''!
      @brief 获取唤醒持续时间
      @return 当前设置的唤醒周期
    '''
    def get_wake_time(self):

    '''!
      @brief 设置唤醒持续时间
      @param wakeTime - 唤醒持续时间(0~255)
    '''
    def set_wake_time(self, wake_time):

    '''!
      @brief 设置音量
      @param vol - 音量范围(1~7)
    '''
    def set_volume(self, vol):

    '''!
      @brief 设置静音模式
      @param mode - 静音模式; 设置值 1: mute, 0: unmute
    '''
    def set_mute_mode(self, mode):

"""#################################################################
                        使用 UART 接口通信的子类
#################################################################"""

    '''!
      @brief 获取命令词对应的ID
      @return 返回获取的命令词ID, 返回0表示未获取到有效id
    '''
    def get_CMDID(self):

    '''!
      @brief 根据命令词ID播放对应的答复音
      @param CMDID - 命令词ID
    '''
    def play_by_CMDID(self, play_id):

    '''!
      @brief 复位模块
    '''
    def reset_module(self):

    '''!
      @brief 设置模块的命令
      @param set_type - 设置类型
      @n       DF2301Q_UART_MSG_CMD_SET_VOLUME : 设置音量, 设置值范围1~7
      @n       DF2301Q_UART_MSG_CMD_SET_ENTERWAKEUP : 进入唤醒状态; 设置值 0
      @n       DF2301Q_UART_MSG_CMD_SET_MUTE : 静音模式; 设置值 1: mute, 0: unmute
      @n       DF2301Q_UART_MSG_CMD_SET_WAKE_TIME : 唤醒持续时间; 设置值范围0~255秒
      @param set_value - 设置值, 范围参见上述设置类型
    '''
    def setting_CMD(self, set_type, set_value):

```


## 兼容性

* RaspberryPi 版本

| Board        | Work Well | Work Wrong | Untested | Remarks |
| ------------ | :-------: | :--------: | :------: | ------- |
| RaspberryPi2 |           |            |    √     |         |
| RaspberryPi3 |           |            |    √     |         |
| RaspberryPi4 |     √     |            |          |         |

* Python 版本

| Python  | Work Well | Work Wrong | Untested | Remarks |
| ------- | :-------: | :--------: | :------: | ------- |
| Python2 |     √     |            |          |         |
| Python3 |     √     |            |          |         |


## 历史

- 2022/12/30 - 1.0.0 版本


## 创作者

Written by qsjhyy(yihuan.huang@dfrobot.com), 2022. (Welcome to our [website](https://www.dfrobot.com/))

