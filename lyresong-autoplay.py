from time import sleep

from pynput.keyboard import Key, Controller
from mido import MidiFile


def note2key(note, base=48):
    # do = 60
    # ri = 62
    # mi = 64
    # fa = 65
    # so = 67
    # la = 69
    # xi = 71
    # do = 72
    notes = [0, 2, 4, 5, 7, 9, 11]
    keys = [
        ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j'],
        ['q', 'w', 'e', 'r', 't', 'y', 'u'],
    ]
    index0 = (note - base) // 12
    note0 = note % 12
    index1 = 0
    for i in range(7):
        if notes[i] == note0:
            index1 = i
            break
        if notes[i] > note0:
            index1 = i
            break
    if 0 <= index0 <= 2 and 0 <= index1 <= 6:
        return note0, keys[index0][index1]
    print('error: note=', note)
    return None, None


def play_music(filename, base=48):
    mid = MidiFile(filename, clip=True)
    keyboard = Controller()
    print('start to play in 2 seconds:', filename)
    sleep(1)
    sleep(1)
    for msg in mid.play():
        # print(msg.type)
        # continue
        if msg.type == "note_on":
            note = msg.note
            # print(note)
            base_note, key = note2key(note, base=base)
            if key:
                print('on\t%d\t%d\t%s' % (note, base_note, key))
                keyboard.press(key)
        elif msg.type == "note_off":
            note = msg.note
            # print(note)
            base_note, key = note2key(note, base=base)
            if key:
                print('**off\t%d\t%d\t%s' % (note, base_note, key))
                keyboard.release(key)
                # sleep(0.02)

    # keyboard = Controller()
    # for i in range(10):
    #     keyboard.press('a')
    #     keyboard.release('a')
    #     sleep(1)
    pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('num', metavar='N', type=int, help='the choice of music')
    args = parser.parse_args()

    playlist = [
        ('Genshin_Impact_main_theme_simple.mid', 48),
        ('dawn_winery_piano.mid', 48),
        ('Dragonspine_Song.mid', 48),
        ('Dragonspine_Song_no_tune_change.mid', 48),
        ('Qingce_Village_clip.mid', 60),
        ('Moon_in_ones_cpu.mid', 48),
        ('liyue_sunset.mid', 48),
        ('Genshin_Impact_Luhua_Pool.mid', 60),
    ]
    print("choice: ", args.num)
    if 0 <= args.num < len(playlist):
        mid, base = playlist[args.num]
        play_music(mid, base)
    else:
        play_music('Genshin_Impact_Liyue_Medley_Calm.mid', base=60)
        pass
    pass
