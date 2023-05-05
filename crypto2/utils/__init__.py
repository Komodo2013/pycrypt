from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget


class UserEntropyPopup(Popup):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        self.title = 'Collecting User Entropy'
        self.size_hint = (0.7, 0.5)
        self.text = text

        content = Label(text=self.text, font_size='16sp')
        self.content = content

        # Bind the keyboard
        Window.bind(on_key_down=self.on_keyboard_down)

        # Initialize the keystrokes
        self.keystrokes = []

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Add the keystroke to the list
        self.keystrokes.append(keycode[1])

    def get_keystrokes(self):
        # Return the list of keystrokes
        return self.keystrokes


def show_user_entropy_popup(text):
    popup = UserEntropyPopup(text=text)
    popup.open()


if __name__ == '__main__':
    show_user_entropy_popup(
        'Please type the following sentence as quickly as you can:\napple banana cherry orange pear')
