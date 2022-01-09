import multiprocessing
from pynput import keyboard
import threading
from pathlib import Path
from os.path import dirname, abspath


class KeyboardListen(threading.Thread):
    def __init__(self, keyboard_queue: multiprocessing.Queue):
        super().__init__()
        self.path = Path(dirname(abspath(__file__)))
        self.keyboard_listener = keyboard.Listener(on_press=self.collect_data)
        self.keyboard_listener.start()
        self.pressed = False
        self.keyboard_queue = keyboard_queue

    def collect_data(self, key):
        if key == keyboard.Key.space:
            self.keyboard_queue.put("record")
        elif hasattr(key, 'char') and key.char == 'q':
            self.keyboard_queue.put("quit")
        elif hasattr(key, 'char') and key.char == 'x':
            print("Keyboard Ready")

    def run(self) -> None:
        print("Keyboard Listening")
