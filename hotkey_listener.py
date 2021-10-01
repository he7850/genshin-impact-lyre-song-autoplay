import threading
import keyboard


class HotkeyListener:
    stop_hotkey = 'f10'
    listener_thread = None

    def stop_listener(self):
        keyboard.unhook_all_hotkeys()
        print('all hotkey listening have been canceled.')

    def wait_for_stop(self):
        keyboard.wait(self.stop_hotkey)
        # remove all previously defined hotkeys
        keyboard.unhook_all_hotkeys()
        print('all hotkey listening have been canceled.')

    def register_hotkey(self, hotkey: str, fn, args):
        keyboard.add_hotkey(hotkey, fn, args)

    def start_listener(self):
        self.listener_thread = threading.Thread(name='stop hotkey listener',
                                                target=self.wait_for_stop,
                                                daemon=True)
        self.listener_thread.start()
