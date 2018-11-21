import socket
import random
import threading
from time import sleep
from client_class import client


def sendMessage(clientList, message):
    
    for client in clientList:
        client.send(message)

        