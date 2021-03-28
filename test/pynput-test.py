import time

from pynput.keyboard import Key, Controller

keyboard = Controller()
time.sleep(3)
keyboard.press('c')
print('c pressed')
