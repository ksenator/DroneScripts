#!/usr/bin/
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

import DroneMissionFunctions


class CreateMissionDialog(FloatLayout):
    create = ObjectProperty(None)
    cancel = ObjectProperty(None)
    ShowFinishedText = 0


class RenameDialog(FloatLayout):
    rename = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    text_input_create = ObjectProperty(None)
    text_input_rename = ObjectProperty(None)

    def dismiss_popup(self):  #
        self._popup.dismiss()

    def show_create(self):
        content = CreateMissionDialog(create=self.create, cancel=self.dismiss_popup)
        self._popup = Popup(title="Create Mission", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_rename(self):
        content = RenameDialog(rename=self.rename, cancel=self.dismiss_popup)
        self._popup = Popup(title="Rename Pictures", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def create(self, path, filename):  # Loads the selected directory
        DroneMissionFunctions.DroneMissionPoints(os.path.join(path, filename[0]))
        # if(CreateMissionDialog.ShowFinishedText):
        self.text_input_create.text = str(CreateMissionDialog.ShowFinishedText)
        self.dismiss_popup()

    def rename(self, path, filename):
        DroneMissionFunctions.RenamePictures(os.path.join(path, filename[0]))
        self.text_input_rename.text = "All Done"

        self.dismiss_popup()


class Launcher(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('CreateMissionDialog', cls=CreateMissionDialog)
Factory.register('RenameDialog', cls=RenameDialog)

if __name__ == '__main__':
    Launcher().run()
