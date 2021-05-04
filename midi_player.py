from time import sleep
from pynput.keyboard import Controller
import mido


class MidiPlayer:
    speed = 1.0
    sleep_scale = 1.0
    debug = False
    base = 48
    keyboard = Controller()

    def set_speed(self, speed):
        self.speed = speed
        self.sleep_scale = round(1 / self.speed, 2)

    def set_debug(self, debug):
        self.debug = debug

    def set_base(self, base):
        self.base = base

    @staticmethod
    def note2key(note, base=48):
        # do = 48
        notes = [0, 2, 4, 5, 7, 9, 11]  # do ~ xi
        cycle = 12
        keys = [
            ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u'],
        ]
        index0 = (note - base) // cycle
        if index0 < 0 or index0 > 2:
            return None
        note0 = note % cycle
        index1 = 0
        for i in range(len(notes)):
            if notes[i] >= note0:
                index1 = i
                break
        return keys[index0][index1]

    def play(self, filename):
        midi = mido.MidiFile(filename, clip=True)
        print('play in 2 seconds:', filename)
        sleep(2)

        # for msg in midi.play():
        for msg in midi:
            if self.debug:
                print(msg)
            sleep(msg.time * self.sleep_scale)
            if msg.is_meta:
                continue
            if msg.type == "note_on" and msg.velocity > 0:
                note = msg.note
                key = self.note2key(note, base=self.base)
                if self.debug:
                    if key:
                        print('on\t%d\t%s' % (note, key))
                    else:
                        print('error: note=', note)
                if key:
                    self.keyboard.press(key)
                    self.keyboard.release(key)
        print('end.')
