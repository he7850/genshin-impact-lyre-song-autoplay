
import time
import win32api
from win32.lib import win32con

# in this example i'm using a dictionary (that i called VK_CODE)
# to map the keys to their respective virtual key codes

# Sending the key a

i = 'a'.upper()
VK_CODE = {
    'A': 0x41
}

time.sleep(3)

# send key down event
win32api.keybd_event(VK_CODE[i], win32api.MapVirtualKey(VK_CODE[i], 0), 0, 0)
print("press key")

# wait for it to get registered.
# You might need to increase this time for some applications
time.sleep(.05)

# send key up event
win32api.keybd_event(VK_CODE[i], win32api.MapVirtualKey(VK_CODE[i], 0), win32con.KEYEVENTF_KEYUP, 0)
print('release key')