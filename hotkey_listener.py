import threading
import keyboard


class HotkeyListener:
    stop_hotkey = 'f10'

    def set_stop_hotkey(self, hotkey):
        self.stop_hotkey = hotkey

    def stop_listener(self):
        keyboard.unhook_all_hotkeys()

    def wait_for_event(self):
        keyboard.wait(self.stop_hotkey)
        # remove all previously defined hotkeys
        keyboard.unhook_all_hotkeys()
        print('all hotkey listening have been canceled.')

    def register_hotkey(self, hotkey, fn, args):
        if not isinstance(hotkey, str):
            print('invalid hotkey!')
            return
        keyboard.add_hotkey(hotkey, fn, args)

    def start_listener(self):
        t1 = threading.Thread(name='hotkey listener',
                              target=self.wait_for_event)
        t1.start()
