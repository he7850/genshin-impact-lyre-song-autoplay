from time import sleep
from pynput.keyboard import Controller
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
    midi = MidiFile(filename, clip=True)
    keyboard = Controller()
    print('start to play in 2 seconds:', filename)
    sleep(1)
    sleep(1)
    for msg in midi.play():
        if msg.type == "note_on" and msg.velocity > 0:
            # print(msg)
            note = msg.note
            base_note, key = note2key(note, base)
            if key:
                print('on\t%d\t%d\t%s' % (note, base_note, key))
                keyboard.press(key)
                keyboard.release(key)
    pass


if __name__ == '__main__':
    import argparse
    import sys

    playlist = [
        ('Mondstadt_dawn_winery.mid', 48),
        ('Chararctor_theme_Ganyu_Radiant_Dreams.mid', 48),
        ('Chararctor_theme_Klee_Crimson_Knight.mid', 60),
        ('Chararctor_theme_Zhongli_the_Listener.mid', 48),
        ('Dragonspine_Song_no_tune_change.mid', 48),
        ('Dragonspine_Ice_Ballad.mid', 60),
        ('Liyue_Luhua_Pool.mid', 48),
        ('Liyue_Another_Hopeful_Tomorrow.mid', 48),
        ('Liyue_Medley_Calm_tracks.mid', 48),
        ('Liyue_Moon_in_ones_cup.mid', 48),
        ('Liyue_Rays_of_Sunlight.mid', 48),
        ('Liyue_The_Fading_Stories(Qingce_Village_Night).mid', 60),
        ('Liyue_Qingce_Village_simple.mid', 60),
        ('Mondstadt_Bustling_Afternoon_of_Mondstadt.mid', 48),
        ('Mondstadt_Tender_Strength.mid', 48),
        ('Mondstadt_A_New_Day_with_Hope.mid', 48),
        ('Genshin_Impact_Main_Theme__.mid', 48),
        ('Genshin_Impact_main_theme_simple.mid', 48),
    ]
    help_str = 'usage: --num [0-%d]\n' % (len(playlist) - 1)
    help_str += '\n'.join([("%d: " % i) + playlist[i][0] for i in range(len(playlist))])

    parser = argparse.ArgumentParser(description='play a song in genshin impact.')
    parser.add_argument('--num', metavar='N', type=int, required=False,
                        help='the choice of music:[0-%d]' % (len(playlist) - 1))
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    if args.list:
        print(help_str)
    elif args.num is not None and 0 <= args.num < len(playlist):
        print("choice: ", args.num)
        mid, base = playlist[args.num]
        play_music(mid, base)
    else:
        play_music('COFFIN_DANCE_master.mid')
        pass
    pass
