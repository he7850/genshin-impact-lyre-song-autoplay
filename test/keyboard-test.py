import time
import threading

import keyboard


def adjust_speed(args, flag, zero):
    args['speed'] = round(args['speed'] * (1 + 0.05 * flag), 2)
    print('speed: %.2f' % args['speed'])


def wait_for_event(args):
    print(args)
    # listen to the event of pressing f12
    keyboard.add_hotkey('f12', adjust_speed, args=(args, 1, 0))
    # listen to the event of pressing ctrl+alt
    keyboard.add_hotkey('ctrl+alt', adjust_speed, args=(args, -1))
    # listen to the event of pressing shift+f12
    keyboard.add_hotkey('shift+f12', adjust_speed, args=(args, -1))
    # wait block until f11 is pressed
    keyboard.wait('f11')
    # remove all previously defined hotkeys
    keyboard.unhook_all_hotkeys()
    print('exit keyboard event listening.')


my_args = {
    'speed': 1.0
}

if __name__ == '__main__':
    t1 = threading.Thread(name='blocking',
                          target=wait_for_event,
                          args=(my_args,))
    t1.start()
    for i in range(100):
        print('sleep 1')
        time.sleep(1)
