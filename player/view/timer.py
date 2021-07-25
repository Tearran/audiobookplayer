''' main.py
controlls the main tkinter app and sleep functionality
'''

import threading
import time
from datetime import datetime as dt


class Timer(threading.Thread):
    '''
        Timer for sleep functionality
        also used to set play view after 20secs of inactivity
        in other views
    '''
    def __init__(self, func, time):
        super().__init__()
        self.lock = threading.Lock()
        self.time = time
        self._sleep = time
        self._countdown = 1
        self._sleep_on = True
        self.func = func
        self.timeup = True

    def reset(self):
        '''set timer back to start value'''
        with self.lock:
            self._sleep = self.time

    def pause(self):
        '''pause countdown'''
        with self.lock:
            self._countdown = 0
            self._sleep_on = False

    def stop(self):
        '''stop countdown and reset the countdown time'''
        with self.lock:
            self._sleep = self.time
            self._countdown = 0
            self._sleep_on = False

    def restart(self):
        '''restart countdown after stop'''
        with self.lock:
            self._countdown = 1
            self._sleep_on = True

    def get_sleep_on(self) -> bool:
        '''return status of timer'''
        with self.lock:
            sleep_on = self._sleep_on
        return sleep_on

    def set_sleep_on(self, on: bool):
        '''set timer status'''
        with self.lock:
            self._sleep_on = on

    def run(self):
        '''run when thread is started'''
        try:
            while self._sleep >= 1:
                time.sleep(1)
                with self.lock:
                    self._sleep -= self._countdown
        finally:
            if self.timeup:
                self.func()
