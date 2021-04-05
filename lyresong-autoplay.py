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
    return note, None


def play_music(filename, base=48, debug=False):
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
            if debug:
                if key:
                    print('on\t%d\t%d\t%s' % (note, base_note, key))
                else:
                    print('error: note=', base_note)
            if key:
                keyboard.press(key)
                keyboard.release(key)
    print('end.')
    pass


if __name__ == '__main__':
    import argparse

    playlist = [
        ('Mondstadt_dawn_winery.mid', 48),
        ('Chararctor_theme_Ganyu_Radiant_Dreams.mid', 48),
        ('Chararctor_theme_Klee_Crimson_Knight.mid', 60),
        ('Chararctor_theme_Zhongli_the_Listener.mid', 48),
        ('Dragonspine_Moonlike_Smile.mid', 48),
        ('Dragonspine_Ice_Ballad.mid', 60),
        ('Dragonspine_Fragile_Fantasy.mid', 48),
        ('Liyue_Luhua_Pool.mid', 48),
        ('Liyue_Another_Hopeful_Tomorrow.mid', 48),
        ('Liyue_Medley_Calm_tracks.mid', 48),
        ('Liyue_Moon_in_One\'s_Cup.mid', 48),
        ('Liyue_Rays_of_Sunlight.mid', 48),
        ('Liyue_Qingce_Village_simple.mid', 60),
        ('Liyue_The_Fading_Stories(Qingce_Village_Night).mid', 60),
        ('Mondstadt_Bustling_Afternoon_of_Mondstadt.mid', 48),
        ('Mondstadt_Tender_Strength.mid', 48),
        ('Mondstadt_A_New_Day_with_Hope.mid', 48),
        ('Genshin_Impact_Main_Theme.mid', 48),
        ('Genshin_Impact_main_theme_simple.mid', 48),
        ('Piano_骑士王の夸り.mid', 48),
        ('Piano_COFFIN_DANCE_master.mid', 48),
        ('Piano_千本樱_piano.mid', 48),
        ('Piano_梦中的婚礼_Mariage_d\'Amour.mid', 48),
        ('Piano_天空之城.mid', 48),
        ('Piano_Canon_C.mid', 48)
    ]
    help_str = 'usage: --num [1-%d]\n' % (len(playlist))
    help_str += '\n'.join([("%d: " % (i+1)) + playlist[i][0]
                           for i in range(len(playlist))])

    parser = argparse.ArgumentParser(
        description='play a song in genshin impact.')
    parser.add_argument('--num', metavar='N', type=int, required=False,
                        help='the choice of music:[1-%d]' % (len(playlist)))
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    args = {}
    print(len(args.keys()))

    if len(args.keys()) == 0:
        while True:
            print(help_str)
            choice = input('input your music choice:')
            try:
                choice = int(choice)
                if 0 < choice <= len(playlist):
                    mid, base = playlist[choice - 1]
                    play_music(mid, base)
                else:
                    raise Exception()
            except:
                print(help_str)

    elif args.list:
        print(help_str)
    elif args.num and 0 < args.num <= len(playlist):
        print("choice: ", args.num)
        mid, base = playlist[args.num - 1]
        play_music(mid, base)
    else:
        pass
    pass
