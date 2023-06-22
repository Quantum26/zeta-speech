import pyttsx3 as pytts
from threading import Thread
from queue import Queue

_sentinel = object()

def tts_thread(in_queue : Queue):
    engine = pytts.init()
    engine.setProperty('voice', engine.getProperty('voices')[1].id)
    while True:
        msg = in_queue.get()
        if msg is _sentinel:
            break
        print(msg)
        engine.say(msg)
        engine.runAndWait()
    engine.stop()

class tts_engine(object):

    def __enter__(self):
        self.queue = Queue()
        self.tts_thread = Thread(target = tts_thread, args=(self.queue,))
        self.tts_thread.start()
        self.running = True
        self.thread_mode = 'm'
        return self

    def stop(self):
        if self.running:
            if self.thread_mode == 'm':
                self.queue.put(_sentinel)
                self.tts_thread.join()
            elif self.thread_mode == 's':
                self.engine.stop()
            self.running = False

    def __exit__(self, type, value, traceback):
        self.stop()

    def restart(self):
        if self.running:
            self.stop()
        self.tts_thread = Thread(target = tts_thread, args=(self.queue,))
        self.tts_thread.start()
        self.running = True
        self.thread_mode = 'm'

    def multi_thread_mode(self):
        self.restart()
    
    def single_thread_mode(self):
        self.queue.put(_sentinel)
        self.tts_thread.join()
        self.thread_mode = 's'
        self.engine = pytts.init()
        self.engine.setProperty('voice', self.engine.getProperty('voices')[1].id)

    def tts(self, msg):
        if not self.running:
            print("tts is not running")
        elif self.thread_mode == 'm':
            self.queue.put(msg)
        elif self.thread_mode == 's':
            print(msg)
            self.engine.say(msg)
            self.engine.runAndWait()
            
if __name__ == "__main__":
    with tts_engine() as engine:
        print("Type in words for tts to speak, type \'quit\' to exit")
        while True:
            input1 = input()
            if input1 == "quit":
                engine.stop()
                break
            engine.tts(input1)