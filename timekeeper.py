import time
import socket
import threading


class timekeeper(threading.Thread):

    def __init__(self, time):

        threading.Thread.__init__(self)
        self.time = time
        self.isRunning = True


    def run():
        
        for i in range(self.time):
            

