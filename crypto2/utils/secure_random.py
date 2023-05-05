from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import os
import random
import time
import struct
import base64


collected_data = []
words = []
with open("words") as f:
    for line in f:
        words.append(line)


def get_system_entropy():
    entropy = os.getloadavg() + (os.getpid(), os.getppid(), time.time(), time.clock_gettime_ns(time.CLOCK_MONOTONIC))
    return str(entropy)


class UserEntropyPopup(Popup):
    def __init__(self, text, text2, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.timing = time.time()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self.handle_key_press)

        self.title = 'Collecting User Entropy'
        self.size_hint = (0.7, 0.3)

        self.content = BoxLayout(orientation='vertical')

        self.label = Label(text=text, font_size='20sp')
        self.content.add_widget(self.label)

        self.label2 = Label(text=text2, font_size='16sp')
        self.content.add_widget(self.label2)

        self.label3 = Label(text='', font_size='16sp')
        self.content.add_widget(self.label3)

    def handle_key_press(self, keyboard, keycode, text, modifiers):
        if len(self.label3.text) >= len(self.label2.text) - 2:
            data = self.data.copy()
            self.dismiss()
            return data

        self.label3.text += text or "#"

        now = time.time()
        self.data.append((keycode[1], now - self.timing))
        self.timing = now

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.handle_key_press)
        self._keyboard = None


def on_user_entropy_popup_dismiss(popup):
    data = popup.data
    packed_data = b''
    for item in data:
        packed_data += struct.pack('sf', item[0].encode(), item[1])

    global collected_data
    collected_data = base64.b64encode(packed_data)
    App.get_running_app().stop()


def show_user_entropy_popup():
    sentence = ""
    for _ in range(10):
        sentence += words[random.randint(0, len(words) - 1)][:-1] + " "

    popup = UserEntropyPopup(text=f'Type this as fast as possible:', text2=sentence)
    popup.bind(on_dismiss=on_user_entropy_popup_dismiss)
    popup.open()


class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        button = Button(text='Open Popup', size_hint=(0.3, 0.2))
        button.bind(on_press=show_user_entropy_popup)
        self.add_widget(button)


class MyApp(App):
    def build(self):
        return MainApp()


def get_user_entropy():
    MyApp().run()
    return collected_data

class Secure_Random():
    internal = []

    def get_random(self, get_user=True):
        return v
