import time
from pinpong.board import gboard, I2C

# I2C constants
DF2301Q_I2C_ADDR = 0x64
DF2301Q_I2C_REG_CMDID = 0x02
DF2301Q_I2C_REG_PLAY_CMDID = 0x03
DF2301Q_I2C_REG_SET_MUTE = 0x04
DF2301Q_I2C_REG_SET_VOLUME = 0x05
DF2301Q_I2C_REG_WAKE_TIME = 0x06

class DFRobot_DF2301Q:
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
    def __init__(self):
        board = gboard
        self.i2c_addr = DF2301Q_I2C_ADDR
        self._i2c = I2C(0)
        super().__init__()

    def _read_reg(self, reg, length=1):
        '''!
          @brief read the data from the register
          @param reg - register address
          @param length - number of bytes to read
          @return read data
        '''
        result = self._i2c.readfrom_mem_restart_transmission(self.i2c_addr, reg, length)
        return result

    def _write_reg(self, reg, data):
        '''!
          @brief writes data to a register
          @param reg - register address
          @param data - written data
        '''
        self._i2c.writeto_mem(self.i2c_addr, reg, bytes(data))

    def get_CMDID(self):
        '''!
          @brief Get the ID corresponding to the command word
          @return Return the obtained command word ID, returning 0 means no valid ID is obtained
        '''
        time.sleep(0.05)
        return self._read_reg(DF2301Q_I2C_REG_CMDID)[0]

    def play_by_CMDID(self, CMDID):
        '''!
          @brief Play the corresponding reply audio according to the command word ID
          @param CMDID - Command word ID
          @note Can enter wake-up state through ID-1 in I2C mode
        '''
        self._write_reg(DF2301Q_I2C_REG_PLAY_CMDID, [CMDID])
        time.sleep(1)

    def get_wake_time(self):
        '''!
          @brief Get the wake-up duration
          @return The current set wake-up period
        '''
        return self._read_reg(DF2301Q_I2C_REG_WAKE_TIME)[0]

    def set_wake_time(self, wake_time):
        '''!
          @brief Set wake-up duration
          @param wake_time - Wake-up duration(0-255)
        '''
        self._write_reg(DF2301Q_I2C_REG_WAKE_TIME, [wake_time & 0xFF])

    def set_volume(self, vol):
        '''!
          @brief Set voice volume
          @param vol - Volume value(1~7)
        '''
        self._write_reg(DF2301Q_I2C_REG_SET_VOLUME, [vol])

    def set_mute_mode(self, mode):
        '''!
          @brief Set mute mode
          @param mode - Mute mode; set value 1: mute, 0: unmute
        '''
        self._write_reg(DF2301Q_I2C_REG_SET_MUTE, [1 if mode else 0])

