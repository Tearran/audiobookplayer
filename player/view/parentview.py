''' parentview.py
provides functionality that is needed in all views
'''

from tkinter import *
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk

from view.timer import Timer
import constants as c


class View(ttk.Frame):
    '''
        offers basic functionality for all views
    '''
    def __init__(self):
        ttk.Frame.__init__(self)

    def show(self):
        '''Calling view will be visible.'''
        self.view()
        self.lift()

    def get_image(self, name):
        '''
            Input: name of image
            Return: an ttk.Label object with the image
        '''
        filename = c.ICONS + name
        myimage = Image.open(filename)
        myimage = ImageTk.PhotoImage(myimage)
        myimage_label = ttk.Label(self.v, image=myimage)
        myimage_label.image = myimage

        return myimage_label

    def countdown(self):
        '''
            set up timer thread
            after 20secs the view will run its timeup method
        '''
        self.timer = Timer(self.timeup, 20)
        self.timer.daemon = True
        self.timer.start()

    def timeup(self):
        '''runs if timer object time has run up'''
        pass

    def set_keys(self, root, d):
        '''
            Input: app instance
                   dict with keys and functions
            Bind app key input to functions.
        '''
        for key in d:
            func = d[key]
            root.bind(key, func)

    def view(self):
        '''
            Has to be implemented in child class.
            Define layout of the window.
        '''
        pass

    def A(self):
        '''implement functionality for button A'''
        pass

    def B(self):
        '''implement functionality for button B'''
        pass

    def X(self):
        '''implement functionality for button X'''
        pass

    def Y(self):
        '''implement functionality for button Y'''
        pass
