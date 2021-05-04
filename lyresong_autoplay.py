from midi_player import MidiPlayer
from hotkey_listener import HotkeyListener

playlist = [
    'Charactor_theme_Ganyu_Radiant_Dreams.mid',
    'Charactor_theme_Klee_Crimson_Knight.mid',
    'Charactor_theme_Zhongli_the_Listener.mid',
    'Charactor_theme_Amber_A_Sweet_Smile.mid',
    'Dragonspine_Moonlike_Smile.mid',
    'Dragonspine_Ice_Ballad.mid',
    'Dragonspine_Fragile_Fantasy.mid',
    'Dragonspine_Snow_Buried_Tales.mid',
    'Dragonspine_Spin_Of_Ice_Crystals.mid',
    'Dragonspine_Unfinished_Frescoes.mid',
    'Dragonspine_ad_oblivione_遗忘的流风.mid',
    'Liyue_Luhua_Pool.mid',
    'Liyue_Another_Hopeful_Tomorrow.mid',
    'Liyue_Medley_Calm_tracks.mid',
    'Liyue_Moon_in_One\'s_Cup.mid',
    'Liyue_Rays_of_Sunlight.mid',
    'Liyue_Slumbering_Lore.mid',
    'Liyue_Adeptus_Solace.mid',
    'Liyue_maidens_longing.mid',
    'Liyue_Good_Night_Liyue.mid',
    'Liyue_The_Fading_Stories(Qingce_Village_Night).mid',
    'Liyue_Battle_Rapid_as_Wildfires.mid',
    'Liyue_Battle_Gallant_Challenge.mid',
    'Mondstadt_dawn_winery.mid',
    'Mondstadt_dawn_winery2.mid',
    'Mondstadt_dawn_winery_OST.mid',
    'Mondstadt_Bustling_Afternoon_of_Mondstadt.mid',
    'Mondstadt_Tender_Strength.mid',
    'Mondstadt_Night.mid',
    'Mondstadt_Let_the_Wind_Tell_You.mid',
    'Genshin_Impact_Main_Theme.mid',
    'Genshin_impact_Caelestinum_Finale_Termini.mid',
    'Piano_骑士王的荣耀.mid',
    'Piano_COFFIN_DANCE.mid',
    'Piano_千本樱.mid',
    'Piano_梦中的婚礼.mid',
    'Piano_水边的阿蒂丽娜.mid',
    'Piano_卡农.mid',
    'Piano_Summer.mid',
    'Piano_Flower_Dance_DJ_Okawari.mid',
    'Piano_Butterfly.mid',
    'Piano_天空之城.mid',
    'Piano_大鱼海棠.mid',
    'Piano_梁祝.mid',
    'Piano_青花瓷.mid',
    'Piano_贝加尔湖畔.mid',
    'Piano_童话.mid',
    'Piano_林俊傑_JJ_Lin_可惜沒如果.mid',
    'Piano_她说.mid',
    'Piano_夜空中最亮的星.mid',
    'Piano_Game_of_Thrones.mid'
]
player_args = {
    'speed': 1.0
}


def get_help():
    help_str = 'usage: --num [1-%d]\n' % (len(playlist))
    song_name_list = [entry for entry in playlist]
    help_str += '\n'.join(["%d: %s" % (index + 1, song_name_list[index])
                           for index in range(len(song_name_list))])
    return help_str


def adjust_speed(player: MidiPlayer, args, flag):
    args['speed'] += 0.04 * flag
    player.set_speed(args['speed'])
    print('adjust speed to: %.2f' % args['speed'])


if __name__ == '__main__':
    midi_player = MidiPlayer()
    hotkey_listener = HotkeyListener()
    hotkey_listener.register_hotkey("f7", adjust_speed, args=(midi_player, player_args, -1))
    hotkey_listener.register_hotkey("f8", adjust_speed, args=(midi_player, player_args, 1))
    hotkey_listener.start_listener()
    print('start listening hotkeys: use f7/f8 to adjust speed...')
    line = ''
    while True:
        print(get_help())
        print('input your music choice:')
        try:
            line = input()
        except KeyboardInterrupt:
            hotkey_listener.stop_listener()
            exit(0)

        try:
            choice = int(line)
            if 0 < choice <= len(playlist):
                mid = playlist[choice - 1]
                midi_player.play("midi_files/" + mid)
            else:
                continue
        except (NameError, ValueError, KeyboardInterrupt):
            continue
