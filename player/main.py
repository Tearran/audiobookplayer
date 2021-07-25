#!/usr/bin/python3
''' main.py
    controll the main tkinter app
    all app-wide objects are instantiated here
'''

import subprocess
from pathlib import Path
from tkinter import *
from tkinter import ttk

import vlc
from PIL import Image, ImageTk
import RPi.GPIO as GPIO

from view.file import FileView
from view.play import PlayView
from view.settings import SettingsView
from view.navi import NaviView
from view.timer import Timer
from music import Music
import constants as c

# GPIO setup for the Raspberry Pi
GPIO.setmode(GPIO.BCM)
butA = c.GPIO_PINS["butA"]
butB = c.GPIO_PINS["butB"]
butX = c.GPIO_PINS["butX"]
butY = c.GPIO_PINS["butY"]
GPIO.setup(butA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butX, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(butY, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Audioplayer():
    '''
        controller of app
        initialize all window objects,
        sleeping and audio objects
    '''
    def __init__(self, root: Tk):
        # Application Window
        super().__init__()
        self.root = root
        self.root.grid()
        self.root.title("audiobooks")

        # everything vlc
        self.audio = Music()

        # frame widget for all content
        mainframe = ttk.Frame(self.root, width=240, height=240)

        self.root.columnconfigure(0, weight=1)  # expand if window is resized
        self.root.rowconfigure(0, weight=1)
        mainframe.grid(row=0, column=0, sticky="nswe")

        # sleep timer
        self.sleep = Timer(self.shutdown, c.SLEEP_TIME)
        self.countdown()

        playview = PlayView(self)
        fileview = FileView(self)
        settingsview = SettingsView(self)
        naviview = NaviView(self)

        self.view_dict = {"play": playview,
                          "file": fileview,
                          "settings": settingsview,
                          "navi": naviview}

        # check if an audiobook is saved from last app run
        # else default audiobook path is used
        if self.audio.current_book != "":
            playview.show()
            self.view = playview
        else:
            self.audio.current_path = Path(c.DEFAULT_AUDIO_PATH)
            fileview.show()
            self.view = fileview

    def show_view(self, viewname: str):
        '''change the visible window to viewname'''
        frame = self.view_dict[viewname]
        frame.show()

    def set_view(self, viewname: str):
        '''set active view'''
        self.view = viewname

    def countdown(self):
        '''initialize sleep countdown'''
        self.sleep.daemon = True
        self.sleep.start()
        self.sleep.stop()

    # callbacks call the corresponding method
    # in the active view
    def callback_butA(self, butA: int):
        '''whenever button A is pressed'''
        self.sleep.reset()
        self.view.A()

    def callback_butB(self, butB: int):
        '''whenever button B is pressed'''
        self.sleep.reset()
        self.view.B()

    def callback_butX(self, butX: int):
        '''whenever button X is pressed'''
        self.sleep.reset()
        self.view.X()

    def callback_butY(self, butY: int):
        '''whenever button Y is pressed'''
        self.sleep.reset()
        self.view.Y()

    def shutdown(self):
        '''tidy up before app shuts down'''
        # save the current position and audiobook
        self.audio.save_position()
        self.audio.writef_lastbook()
        # release GPIO pins
        GPIO.cleanup()
        # shut down the pi
        subprocess.run("/home/pi/player/shutdown.sh")
        # destroy the app
        self.root.destroy()


def main():
    try:
        root = Tk()
        player = Audioplayer(root)

        # connect button presses to functions
        GPIO.add_event_detect(butA, GPIO.RISING,
                              callback=player.callback_butA,
                              bouncetime=200)
        GPIO.add_event_detect(butB, GPIO.RISING,
                              callback=player.callback_butB,
                              bouncetime=200)
        GPIO.add_event_detect(butX, GPIO.RISING,
                              callback=player.callback_butX,
                              bouncetime=200)
        GPIO.add_event_detect(butY, GPIO.RISING,
                              callback=player.callback_butY,
                              bouncetime=200)

        root.mainloop()
    except KeyboardInterrupt:
        player.shutdown()


if __name__ == "__main__":
    main()
