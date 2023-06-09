import pyaudio
import keyboard
from os import get_terminal_size, system

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()

def print_sl(msg):
    def clear_terminal_line(end='\r'):
        columns, _ = get_terminal_size()
        print('', end='\r')  # return cursor to beginning
        print(' ' * (columns - 1), end=end)  # Fill line with spaces
    clear_terminal_line()
    print(msg, end='\r')

if __name__ == "__main__":
    system('CLS')
    print_sl('starting...')
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                input=True)
    frames=[]
    err = None
    print_sl('press f to start recording')
    keyboard.wait("f", suppress=True)
    print_sl('recording, press esc to stop...')
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if(keyboard.is_pressed("esc")):
            print_sl("esc pressed! ending recording...")
            break
    stream.stop_stream()
    stream.close()
    print_sl("playing...")
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                output=True)
    for frame in frames:
        stream.write(frame)
    stream.close()
    p.terminate()
    print_sl("finished")
