#from apps.chrome.youtube import YTDriver as youtube
from apps.chrome.selenium_yt import SeleniumYTMusic
from apps.open import selenium_start
from voice_driver import voice_driver

def yt_play(phrase_arr, vd : voice_driver):
    vd.tts("starting selenium driver")
    music = SeleniumYTMusic()
    vd.local_objects.append(music)
    play_func = vd.remove_commands(["play"])[0]
    def music_stop(*args):
        music.stop()
        vd.remove_commands(["music"], prefix=True)
        vd.add_commands({"play": play_func})
    vd.run_on_exit({"music stop": music_stop})
    vd.add_commands({
        "music play next" : lambda st, vd: music.add_to_queue(st[2:]),
        "music play" : lambda st, vd: music.play(st[2:]),
        "music pause" : lambda st, vd: music.pause(),
        "music unpause" : lambda st, vd: music.unpause(),
        "music back" : lambda st, vd: music.prev(),
        "music previous" : lambda st, vd: music.prev(),
        "music skip" : lambda st, vd: music.next(),
        "music next" : lambda st, vd: music.next(),
        "music stop" : music_stop,
        "music add" : lambda st, vd: music.add_to_queue(st[2:]),
        "music toggle" : lambda st, vd: music.toggle_music_page(),
        "music repeat" : lambda st, vd: music.toggle_repeat(),
        "music search" : lambda st, vd: music.search(st[2:]),
        "music shuffle" : lambda st, vd: music.toggle_shuffle()
    })
    vd.tts("playing " + " ".join(phrase_arr[1:]))
    music.play(phrase_arr[1:])