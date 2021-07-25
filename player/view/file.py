''' file.py
    view to search for different audio file
'''

from tkinter import *
from tkinter import ttk
from pathlib import Path

import view.parentview as view


class FileView(view.View):
    '''
        Show file window
        move through file system
        get to settings view
    '''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app
        self.path = Path(self.app.audio.current_path)

        self.listindex = 0
        self.listlength = 0

        self.button_data = [{'r': 0, 'c': 0, 'icon': 'listup.png'},    # but A
                            {'r': 1, 'c': 0, 'icon': 'listdown.png'},  # but B
                            {'r': 0, 'c': 2, 'icon': 'settings.png'},  # but X
                            {'r': 1, 'c': 2, 'icon': 'ok.png'}]        # but Y

        self.d = {"<u>": self.A,
                  "<j>": self.B,
                  "<i>": self.X,
                  "<k>": self.Y}

    def view(self):
        '''look of the view'''
        self.set_keys(self.app.root, self.d)
        self.app.set_view(self)
        self.countdown()

        self.v = ttk.Frame(self.app.root, width=240, height=240)
        self.v.grid(row=0, column=0, sticky="nswe")

        for d in self.button_data:
            label = self.get_image(d['icon'])
            label.grid(row=d['r'], column=d['c'])

        self.path = Path(self.app.audio.current_path)

        self.show_list()

    def timeup(self):
        '''if countdown runs up'''
        self.timer.stop()
        self.v.destroy()
        self.app.show_view("play")

    def show_list(self):
        '''
            Show self.liste in the file frame of the app.
        '''
        files = self.get_filelist()
        choosefiles = StringVar(value=files)
        self.liste = Listbox(self.v,
                             width=25,
                             height=13,
                             listvariable=choosefiles)
        self.liste.selection_set(self.listindex)
        self.liste.activate(self.listindex)
        self.liste.grid(column=1, row=0, rowspan=3)
        self.liste.see(self.listindex)

        self.liste.focus()

    def get_filelist(self):
        '''
            Return a list with all mp3, m4a and directories
            found in current_path.
        '''
        files = sorted([f.name for f in self.path.iterdir()
                        if f.is_dir() or f.suffix == '.m4a'
                        or f.suffix == '.mp3'])
        files.append("..")
        self.listlength = len(files)
        return files

    def A(self):
        '''
            Walk the cursor up in self.liste,
            visually and in actual list.
        '''
        self.timer.reset()
        self.liste.selection_clear(self.listindex)
        if self.listindex > 0:
            self.listindex -= 1
        else:
            self.listindex = self.listlength - 1
        self.liste.selection_set(self.listindex)
        self.liste.see(self.listindex)
        self.liste.activate(self.listindex)

    def B(self):
        '''
            Walk the cursor down in self.liste,
            visually and in actual list.
        '''
        self.timer.reset()
        self.liste.selection_clear(self.listindex)
        if self.listindex < self.listlength-1:
            self.listindex += 1
        else:
            self.listindex = 0
        self.liste.selection_set(self.listindex)
        self.liste.see(self.listindex)
        self.liste.activate(self.listindex)

    def X(self):
        '''Go to settings window.'''
        self.timer.stop()
        self.v.destroy()
        self.app.show_view("settings")

    def Y(self):
        '''
            Highlighted file is mp3 or m4a -> play it
            Highlighted file is dir -> show dir
        '''
        self.timer.reset()
        if self.liste.curselection() != "":
            cur = self.liste.curselection()
        else:
            cur = 0

        # save the position of the position of last audiobook
        # put new filename into music object
        selected_file = self.liste.get(cur)
        if selected_file.endswith(".mp3") or selected_file.endswith(".m4a"):
            self.app.audio.save_position()
            if self.app.audio.mediaplayer.is_playing():
                self.app.audio.mediaplayer.stop()
            self.app.audio.current_path = self.path
            self.app.audio.current_book = Path(selected_file)
            self.app.audio.set_book(Path(self.path, selected_file))
            self.app.audio.play()
            self.v.destroy()
            self.app.show_view("play")
        elif Path(self.path, selected_file).is_dir():
            self.path = Path(self.path, selected_file)
            self.listindex = 0

            self.show_list()
