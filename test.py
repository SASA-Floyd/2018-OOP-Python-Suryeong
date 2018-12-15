import socket
from gui import *
import threading
import pygame
from time import *


def callGUI():

    print(123)
    screen = pygame.display.set_mode((1000, 600))
    print('a')
    pygame.display.set_caption('Blue Brick')
    print(1111)


    def a():
        while True:
            sleep(1)
            print(111)

call = threading.Thread(target=callGUI)
aa = threading.Thread(target=a)
aa.start()
call.start()
