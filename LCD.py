import I2CDevice
import time
import enum


class LCDCommands(enum.Enum):
    CLEARDISPLAY = 0x01
    RETURNHOME = 0x02
    ENTRYMODESET = 0x04
    DISPLAYCONTROL = 0x08
    CURSORSHIFT = 0x10
    FUNCTIONSET = 0x20
    SETCGRAMADDR = 0x40
    SETDDRAMADDR = 0x80


class LCDDisplayEntryMode(enum.Enum):
    ENTRYRIGHT = 0x00
    ENTRYLEFT = 0x02
    ENTRYSHIFTUP = 0x01
    ENTRYSHIFTDOWN = 0x00


class LCDOnOff(enum.Enum):
    DISPLAYON = 0x04
    DISPLAYOFF = 0x00
    CURSORON = 0x02
    CURSOROFF = 0x00
    BLINKON = 0x01
    BLINKOFF = 0x00


class LCDCursor(enum.Enum):
    DISPLAYMOVE = 0x08
    CURSORMOVE = 0x00
    MOVERIGHT = 0x04
    MOVELEFT = 0x00


class LCDMode(enum.Enum):
    BITMODE_8 = 0x10
    BITMODE_4 = 0x00
    LINE_2 = 0x08
    LINE_1 = 0x00
    DOTS_5x10 = 0x04
    DOTS_5x8 = 0x00


class LCDBacklight(enum.Enum):
    ON = 0x08
    OFF = 0x00


class Bits(enum.Enum):
    ENABLE = 0b00000100
    READ_WRITE = 0b00000010
    SELECT = 0b00000001


class LCD:
    def __init__(self, addr=0x27):
        self.device = I2CDevice(addr)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(
            LCDCommands.FUNCTIONSET
            | LCDMode.LINE_2
            | LCDMode.DOTS_5x8
            | LCDMode.BITMODE_4
        )
        self.lcd_write(LCDCommands.DISPLAYCONTROL | LCDCommands.DISPLAYON)
        self.lcd_write(LCDCommands.CLEARDISPLAY)
        self.lcd_write(LCDCommands.ENTRYMODESET | LCDCommands.ENTRYLEFT)
        time.sleep(0.2)

    def lcd_strobe(self, data):
        self.device.write_cmd(data | Bits.ENABLE | LCDBacklight.ON)
        time.sleep(0.0005)
        self.device.write_cmd(((data & Bits.ENABLE) | LCDBacklight.ON))
        time.sleep(0.0001)

    def lcd_write_four_bits(self, data):
        self.device.write_cmd(data | LCDBacklight.ON)
        self.lcd_strobe(data)

    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_display_string(self, string, line):
        if line == 1:
            self.lcd_write(0x80)
        elif line == 2:
            self.lcd_write(0xC0)
        elif line == 3:
            self.lcd_write(0x94)
        elif line == 4:
            self.lcd_write(0xD4)

        for char in string:
            self.lcd_write(ord(char), Bits.SELECT)

    def lcd_clear(self):
        self.lcd_write(LCDCommands.CLEARDISPLAY)
        self.lcd_write(LCDCommands.RETURNHOME)
