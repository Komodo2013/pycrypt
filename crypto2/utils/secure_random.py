import base64
import math
import struct

import keyboard
import os
import random
import time

def get_system_entropy():
    entropy = os.getloadavg() + (os.getpid(), os.getppid(), time.time(), time.clock_gettime_ns(time.CLOCK_MONOTONIC))
    return str(entropy)


def get_user_entropy():
    collected_data = []
    words = []
    with open("words") as f:
        for line in f:
            words.append(line)

    sentence = ""
    for _ in range(10):
        sentence += words[random.randint(0, len(words) - 1)][:-1] + " "

    print("Type the following sentence as fast as possible:")
    print(sentence)

    results = []
    before = time.time()

    def on_key_press(event):
        nonlocal before
        now = time.time()
        results.append([event.name, now - before])
        before = now

    keyboard.on_press(on_key_press)
    # Keep the program running until the sentence is typed
    while len(results) < len(sentence) - 1:
        pass

    packed = b''

    for item in results:
        packed += struct.pack('sf', item[0].encode(), item[1])

    return base64.b64encode(packed)

class Secure_Random():
    #TODO: I need to finish this part... but I need my hash algorithm before I can
    def __init__(self, get_user=True):
        self.__internal = 0
        self.__since_last_user = math.inf if get_user else -math.inf
        self.__since_last_system = math.inf

    def get_random(self):
        yield random.random()

    def get_random_int(self, lower, upper):
        yield random.randint(lower, upper)