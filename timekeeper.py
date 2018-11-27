import time
import socket
import threading

current_timekeeper = 0


class timekeeper(threading.Thread):

    def __init__(self, time, name):

        threading.Thread.__init__(self)
        self.time = time
        self.name = name
        self.isRunning = True

    def check(self):

        if current_timekeeper == self.name:
            return True
        else:
            return False 

    def run(self):

        for i in range(self.time):

            if self.check() is false:
                break

            time.sleep(1)
            print(i)
