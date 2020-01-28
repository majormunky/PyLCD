import time
import socket
from LCD import LCD


def get_local_ip_address():
    address = None

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    address = s.getsockname()[0]
    s.close()

    return address


local_address = get_local_ip_address()

try:
    lcd = LCD()
    while True:
        lcd.lcd_display_string("IP: {}".format(local_address), 1)
        lcd.lcd_display_string("Line 2", 2)
        time.sleep(10)
        lcd.lcd_clear()
        time.sleep(0.1)
except KeyboardInterrupt:
    lcd.lcd_clear()
