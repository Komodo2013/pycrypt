from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import os
import random
import time

words = []
with open("words") as f:
    for line in f:
        words.append(line)

def get_system_entropy():
    entropy = os.getloadavg() + (os.getpid(), os.getppid(), time.time(), time.clock_gettime_ns(time.CLOCK_MONOTONIC))
    return str(entropy)

class UserEntropyPopup(Popup):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self.title = 'Collecting User Entropy'
        self.size_hint = (0.7, 0.5)

        content = Label(text=text, font_size='16sp')
        self.content = content


def show_user_entropy_popup(text):
    popup = UserEntropyPopup(text=text)
    popup.open()

def get_user_entropy():
    sentence = ""
    for _ in range(10):
        sentence += words[random.randint(0, len(words))][:-1] + " "

    show_user_entropy_popup(f'Please type the following sentence as quickly as you can:\n{sentence}')

    keystimes = []
    return keystimes


"""
for _ in range(16):
    print(get_system_entropy())
    time.sleep(1)
"""
for _ in range(1):
    print(get_user_entropy())
    time.sleep(1)
