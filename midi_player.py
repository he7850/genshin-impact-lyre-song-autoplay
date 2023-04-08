from time import sleep
from pynput.keyboard import Controller
import keyboard
import mido
import random

random_change = [1 + random.randint(-4, 16) / 100 for i in range(1000)]

keys = (
    ('z', 'x', 'c', 'v', 'b', 'n', 'm'),
    ('a', 's', 'd', 'f', 'g', 'h', 'j'),
    ('q', 'w', 'e', 'r', 't', 'y', 'u'),
)
# lowest_do_note(z) = 48, medium_do_note(a) = 60, highest_do_note(z) = 72
# do_2_xi_notes = [0, 2, 4, 5, 7, 9, 11]
note_to_key_idx = [0, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 6]  # b note -> upper note


def note2key(note, base=48) -> int:
    index0 = (note - base) // 12
    if index0 < 0 or index0 > 2:
        return ' '
    return keys[index0][note_to_key_idx[note % 12]]


class MidiPlayer:

    speed = 100
    sleep_scale = 1.0
    debug = False
    pause = False
    random_mode = False
    random_index = 0
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

    def toggle_random(self):
        self.random_mode = not self.random_mode

    def play(self, filename):
        midi = mido.MidiFile(filename, clip=True)
        messages = []
        count = 0
        out = open('msg.txt', 'w+')
        for msg in midi:
            count += 1
            if msg.is_meta:
                continue
            # print(count, msg)
            print(count, msg, file=out)
            if msg.type == "note_on":
                key = note2key(msg.note)
                if key == ' ' or msg.velocity == 0: # empty note
                    if msg.time > 0:
                        message = {
                            'type': 1,  # empty note
                            'time': msg.time
                        }
                        if len(messages) > 0 and messages[-1]['type'] == 1:
                            message['time'] += messages.pop(-1)['time']
                        messages.append(message)
                else:   # note to play
                    if msg.time > 0:   # the start note
                        message = {
                            'type': 0,  # note to play
                            'time': msg.time,
                            'key': key,
                        }
                        if len(messages) > 0 and messages[-1]['type'] == 1:
                            message['time'] += messages.pop(-1)['time']
                        messages.append(message)
                    else:   # composition note
                        if len(messages) > 0 and messages[-1]['type'] == 0:  # combine last notes
                            message = messages.pop(-1)
                            message['key'] = message['key'] + '+' + key
                            messages.append(message)
                        else:    # combine empty note
                            message = {
                                'type': 0,  # note to play
                                'time': msg.time,
                                'key': key,
                            }
                            if len(messages) > 0 and messages[-1]['type'] == 1:  # combine empty notes
                                message['time'] += messages.pop(-1)['time']
                            messages.append(message)
            elif msg.type == "control_change":  # empty note
                if msg.time > 0:
                    message = {
                        'type': 1,  # empty note
                        'time': msg.time
                    }
                    if len(messages) > 0 and messages[-1]['type'] == 1:
                        message['time'] += messages.pop(-1)['time']
                    messages.append(message)
        # return
        out.close()
        print('play in 2 seconds:', filename)
        # exit(0)
        sleep(2)

        out = open('notes.txt', 'w+')
        count = 0
        for message in messages:
            count += 1
            print(count, message, file=out)
        out.close()
        
        for message in messages:
            while self.pause:
                sleep(1)
            if message['time'] > 0:
                if self.random_mode:
                    # print('random change:', random_change[self.random_index // 3 % 1000])
                    sleep(message['time'] * self.sleep_scale * random_change[self.random_index // 3 % 1000])
                    self.random_index = self.random_index + 1
                else:
                    sleep(message['time'] * self.sleep_scale)
            if message['type'] == 1:
                continue
            # print(message['key'])
            keyboard.press_and_release(message['key'])
            # self.keyboard.press(message['key'])
            # self.keyboard.release(message['key'])
        print('end.')
