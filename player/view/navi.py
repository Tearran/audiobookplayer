''' navigate in audiobook
    chapter forward/backward and back to start
    get to file view from here
'''
from tkinter import *
from tkinter import ttk

from view.timer import Timer
import view.parentview as view


class NaviView(view.View):
    ''' navigate through audiobook
        forward, backward, back to start
        get to file view
    '''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.listindex = 0
        self.listlength = 0

        self.chapter = []

        self.button_data = [{'r': 0, 'c': 0, 'icon': 'listup.png'},     # but A
                            {'r': 1, 'c': 0, 'icon': 'listdown.png'},  # but B
                            {'r': 0, 'c': 2, 'icon': 'small_files.png'},     # but X
                            {'r': 1, 'c': 2, 'icon': 'ok.png'}]   # but Y

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
            label.grid(column=d['c'], row=d['r'])

        self.show_list()

    def timeup(self):
        '''if countdown runs out'''
        self.v.destroy()
        self.app.show_view("play")

    def show_list(self):
        self.chapter = []
        self.listlength = self.app.audio.mediaplayer.get_chapter_count()
        print("listlength: ",self.listlength)
        for i in range(self.listlength):
            self.chapter.append("chapter "+str(i))
        print(self.chapter)
        choosechapter = StringVar(value=self.chapter)
        self.liste = Listbox(self.v,
                             width=25,
                             height=13,
                             listvariable=choosechapter)
        self.listindex = self.app.audio.mediaplayer.get_chapter()
        self.liste.selection_set(self.listindex)
        self.liste.activate(self.listindex)
        self.liste.grid(column=1, row=0, rowspan=3)
        self.liste.see(self.listindex)
        self.liste.focus()

    def A(self):
        '''go up in chapter list'''
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
        '''go down in chapter list'''
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
        '''go to file view'''
        self.timer.stop()
        self.v.destroy()
        self.app.show_view("file")

    def Y(self):
        '''go to next chapter of audiobook'''
        self.timer.reset()
        if self.liste.curselection() != "":
            cur = self.liste.curselection()[0]
        else:
            cur = 0
        print(cur,type(cur))
        self.app.audio.mediaplayer.set_chapter(cur)
