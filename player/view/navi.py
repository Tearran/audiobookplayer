''' navigate in audiobook
    chapter forward/backward and back to start
    get to file view from here
'''
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

        self.button_data = [{'r': 0, 'c': 0, 'icon': 'start.png'},     # but A
                            {'r': 1, 'c': 0, 'icon': 'backward.png'},  # but B
                            {'r': 0, 'c': 1, 'icon': 'files.png'},     # but X
                            {'r': 1, 'c': 1, 'icon': 'forward.png'}]   # but Y

    def view(self):
        '''look of the view'''
        self.app.set_view(self)
        self.countdown()

        self.v = ttk.Frame(self.app.root, width=240, height=240)
        self.v.grid(row=0, column=0, sticky="nswe")

        for d in self.button_data:
            label = self.get_image(d['icon'])
            label.grid(column=d['c'], row=d['r'])

    def timeup(self):
        '''if countdown runs out'''
        self.v.destroy()
        self.app.show_view("play")

    def A(self):
        '''set position of audiobook back to beginning'''
        self.timer.reset()
        self.app.audio.mediaplayer.set_position(0)
        self.app.audio.position = 0

    def B(self):
        '''go to previous chapter of audiobook'''
        self.timer.reset()
        self.app.audio.mediaplayer.previous_chapter()

    def X(self):
        '''go to file view'''
        self.timer.stop()
        self.v.destroy()
        self.app.show_view("file")

    def Y(self):
        '''go to next chapter of audiobook'''
        self.timer.reset()
        self.app.audio.mediaplayer.next_chapter()
