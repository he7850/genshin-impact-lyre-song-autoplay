import sys
import random
from time import sleep
import glob, os
from midi_player import MidiPlayer
from hotkey_listener import HotkeyListener

playlist_dirs = ['other', 'genshin']
playlist = []
player_speed = 100
auto_play = False

def switch_to_midi_dir():
    # change dir to midi_files
    curr_dir = os.getcwd()
    if "midi_files" in curr_dir:
        midi_dir = curr_dir.split("midi_files")[0] + "/midi_files"
        os.chdir(midi_dir)
    else:
        os.chdir("midi_files")
    curr_dir = os.getcwd()

def update_playlist():
    playlist.clear()
    for dir_name in playlist_dirs:
        for file in glob.glob(dir_name + "/*.mid"):
            playlist.append(file)

def get_help():
    help_str = 'usage: --num [1-%d] (0 to exit)\n' % (len(playlist))
    for index, name in enumerate(playlist, start=1):
        help_str += "%d: %s\n" % (index, name)
    return help_str

def adjust_speed(player: MidiPlayer, value):
    global player_speed
    player_speed += value
    if player_speed < 20:
        player_speed = 20
    player.set_speed(player_speed)
    print('adjust speed to: %d%%' % player_speed)

def toggle_pause(player: MidiPlayer):
    global auto_play
    player.toggle_pause()
    auto_play = not auto_play

if __name__ == '__main__':
    switch_to_midi_dir()
    update_playlist()
    midi_player = MidiPlayer()
    midi_player.set_debug(False)
    hotkey_listener = HotkeyListener()
    hotkey_listener.register_hotkey("-", adjust_speed, args=(midi_player, -4))
    hotkey_listener.register_hotkey("+", adjust_speed, args=(midi_player, 4))
    hotkey_listener.register_hotkey("/", toggle_pause, args=(midi_player,))
    hotkey_listener.start_listener()
    print('start listening hotkeys: use -/+ to adjust speed...')

    line = ''
    while True:
        update_playlist()
        print(get_help())
        print('input your music choice:(0 to randomly autoplay)')
        try:
            line = input()
        except KeyboardInterrupt:
            print('exit lyresong autoplay.')
            hotkey_listener.stop_listener()
            sys.exit(0)

        try:
            choice = int(line)
            if choice == 0:
                current = next = -1
                auto_play = True
                while auto_play:
                    if next != -1:
                        current = next
                    else:
                        current = random.randint(0,len(playlist)-1)
                    next = random.randint(0,len(playlist)-1)
                    mid = playlist[current]
                    # classic\雪掩的往事.mid
                    # classic\龙脊雪山-雪掩的往事-Dragonspine_Snow_Buried_Tales.mid
                    song_name = mid.split("\\")[1].replace(".mid","").replace("Piano_","")
                    song_name_parts = song_name.split("-")
                    if len(song_name_parts) > 1:
                        song_name = "-".join(song_name_parts[:-1])
                    next_song_name = playlist[next].split("\\")[1].replace(".mid","")
                    song_name_parts = next_song_name.split("-")
                    if len(song_name_parts) > 1:
                        next_song_name = "-".join(song_name_parts[:-1])
                    print(f"当前演奏：{song_name}")
                    print(f"下一曲：{next_song_name}")
                    with open("playinfo.txt","wt") as f:
                        f.write(f"当前演奏：{song_name}")
                    sleep(4)
                    midi_player.play(mid)
            elif 0 < choice <= len(playlist):
                mid = playlist[choice - 1]
                midi_player.play(mid)
            else:
                continue
        except FileNotFoundError:
            print("The midi file has been deleted, now refresh dir...")
            update_playlist()
        except (NameError, ValueError, KeyboardInterrupt):
            continue
