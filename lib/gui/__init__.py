import os
# os.environ['KIVY_NO_CONSOLELOG'] = '1'

import kivy
kivy.require('1.11.1')
from kivy.app import App

class T0mApp(App):
    def build(self) -> None:
        pass

def show() -> None:
    T0mApp().run()