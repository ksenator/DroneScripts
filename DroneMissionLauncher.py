#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 09:44:45 2019

@author: ksenator
"""

import os

from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

import DroneMissionSetup


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):  #
        self._popup.dismiss()

    def show_load(self):  # Brings up the selection menu from the starting screen
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):  # Loads the selected directory
        DroneMissionSetup.DroneMissionPoints(os.path.join(path, filename[0]))
        self.text_input.text = "This is the path to the file you chose: \n" + os.path.join(path, filename[
            0]) + "\n" + "All Done"
        self.dismiss_popup()


class Launcher(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == '__main__':
    Launcher().run()
