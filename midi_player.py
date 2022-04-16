from time import sleep
from pynput.keyboard import Controller
import keyboard
import mido

keys = [
    ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u'],
]
# lowest_do_note(z) = 48, medium_do_note(a) = 60, highest_do_note(z) = 72
note_offsets = [0, 2, 4, 5, 7, 9, 11]  # do ~ xi
key_of_note = [0, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 6]


def note2key(note, base=48) -> int:
    index0 = (note - base) // 12
    if index0 < 0:
        index0 += 1
    if index0 < 0:
        return ' '
    if index0 > 2:
        return ' '
    note_offset = note % 12
    return keys[index0][key_of_note[note_offset]]


class MidiPlayer:

    speed = 100
    sleep_scale = 1.0
    debug = False
    pause = False
    base = 48
    keyboard = Controller()

    notes = []

    def set_speed(self, speed):
        self.speed = speed
        self.sleep_scale = round(100 / self.speed, 3)

    def set_debug(self, debug):
        self.debug = debug

    def set_base(self, base):
        self.base = base

    def toggle_pause(self):
        self.pause = not self.pause

    def play(self, filename):
        midi = mido.MidiFile(filename, clip=True)
        messages = []
        for msg in midi:
            if msg.is_meta:
                continue
            # print(msg)
            if msg.type == "note_on":
                key = note2key(msg.note)
                if key == ' ' or msg.velocity <= 0:
                    message = {'type': 1, 'time': msg.time}
                else:
                    message = {
                        'type': 0,
                        # 'note': msg.note,
                        'time': msg.time,
                        'key': key,
                    }
                messages.append(message)
            if msg.type == "control_change" and msg.time > 0:
                message = {'type': 1, 'time': msg.time}
                messages.append(message)
        # return
        print('play in 2 seconds:', filename)
        sleep(2)

        for message in messages:
            while self.pause:
                sleep(1)
            sleep(message['time'] * self.sleep_scale)
            if message['type'] == 1:
                continue
            keyboard.press_and_release(message['key'])
            # self.keyboard.press(message['key'])
            # self.keyboard.release(message['key'])
        print('end.')
