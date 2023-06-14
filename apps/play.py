from apps.chrome.youtube import YTDriver as youtube

def yt_play(phrase_arr):
    yt = youtube(phrase_arr[1:])
    yt.play()