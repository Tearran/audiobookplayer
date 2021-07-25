''' play.py
view for play/pause and louder/quieter
get to navi view from here
'''

from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from view.timer import Timer
import view.parentview as view


class PlayView(view.View):
    '''
        Simple music playing window.
    '''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.playing = False

        self.button_data = [{'r': 0, 'c': 0, 'icon': 'louder.png'},  # but A
                            {'r': 1, 'c': 0, 'icon': 'quieter.png'},  # but B
                            {'r': 0, 'c': 1, 'icon': 'navi.png'},  # but X
                            {'r': 1, 'c': 1, 'icon': 'playpause.png'}]  # but Y

        self.d = {"<u>": self.A,
                  "<j>": self.B,
                  "<i>": self.X,
                  "<k>": self.Y}

    def view(self):
        '''look of the view'''
        self.set_keys(self.app.root, self.d)
        self.app.set_view(self)

        self.v = ttk.Frame(self.app.root, width=240, height=240)
        self.v.grid(row=0, column=0, sticky="nswe")

        for d in self.button_data:
            label = self.get_image(d['icon'])
            label.grid(row=d['r'], column=d['c'])

    def A(self):
        '''turn audiobook louder'''
        self.app.audio.louder()

    def B(self):
        '''turn audiobook quieter'''
        self.app.audio.quieter()

    def X(self):
        '''go to navi view'''
        self.v.destroy()
        self.app.show_view("navi")

    def Y(self):
        '''play/pause audiobook'''
        self.app.audio.play()
