''' settings.py
    view to toggle sleep, shutdown or reset position of audiobook
'''

from tkinter import *
from tkinter import ttk
import subprocess
import time

from view.timer import Timer
import view.parentview as view


class SettingsView(view.View):
    '''
        Show the settings window
        turn sleep on/off
        turn wifi on/off
        shutdown app
        go to play view
    '''
    def __init__(self, app):
        ttk.Frame.__init__(self, app.root)

        self.app = app

        self.wifion = bool

        self.button_data = [{'r': 0, 'c': 1, 'icon': 'play_settings.png'},
                            {'r': 1, 'c': 1, 'icon': 'shutdown.png'}]

    def view(self):
        '''look of the view'''
        self.app.set_view(self)

        self.sleep_on = self.app.sleep.get_sleep_on()
        self.countdown()

        self.v = ttk.Frame(self.app.root)
        self.v.grid(row=0, column=0, sticky="nsew")

        for d in self.button_data:
            label = self.get_image(d['icon'])
            label.grid(row=d['r'], column=d['c'])

        # sleep label dependent on sleep status
        if self.sleep_on:
            labeltext = "sleepison.png"
        else:
            labeltext = "sleepisoff.png"
        l_sleep = self.get_image(labeltext)
        l_sleep.grid(row=0, column=0)

        # wifi label dependent on wifi status
        self.check_wifi()
        if self.wifion:
            labeltext = "turnwifioff.png"
        else:
            labeltext = "turnwifion.png"
        l_wifi = self.get_image(labeltext)
        l_wifi.grid(row=1, column=0)

    def timeup(self):
        '''if timer runs out'''
        self.timer.stop()
        self.v.destroy()
        self.app.show_view("play")

    def check_wifi(self):
        '''check if wifi is connected or not'''
        ps = subprocess.Popen(['rfkill', 'list'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
        output = subprocess.check_output(('grep', 'Soft'), stdin=ps.stdout)
        out = str(output).split(" ")
        status = out[2]
        status = status.rstrip("\\n'")
        if status == "no":
            self.wifion = True
        else:
            self.wifion = False

    def start_sleep(self):
        '''start sleep timer'''
        self.app.sleep.set_sleep_on(True)
        self.v.destroy()
        self.show()
        self.app.sleep.restart()

    def stop_sleep(self):
        '''stop sleep timer'''
        self.app.sleep.set_sleep_on(False)
        self.v.destroy()
        self.show()
        self.app.sleep.stop()

    def A(self):
        '''start or stop sleep timer'''
        self.timer.reset()
        if self.sleep_on:
            self.stop_sleep()
        else:
            self.start_sleep()

    def B(self):
        '''toggle wifi'''
        self.timer.reset()
        if self.wifion:
            subprocess.run("/home/pi/player/turnwifioff.sh")
        else:
            subprocess.run("/home/pi/player/turnwifion.sh")
        time.sleep(2)
        self.v.destroy()
        self.show()

    def X(self):
        '''go to play window'''
        self.timer.stop()
        self.v.destroy()
        self.app.show_view("play")

    def Y(self):
        '''
            Save the last position of audiobook.
            End the application.
        '''
        self.timer.reset()
        self.app.shutdown()
