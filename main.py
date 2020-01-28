import time
from LCD import LCD

try:
    lcd = LCD()
    while True:
        lcd.lcd_display_string("Test", 1)
        lcd.lcd_display_string("Line 2", 2)
        time.sleep(2)
        lcd.lcd_clear()
        time.sleep(1)
except KeyboardInterrupt:
    lcd.lcd_clear()
