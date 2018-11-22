import socket
import random
import threading
from time import sleep
from client_class import client


SERVER_IP = 'localhost'
SERVER_PORT = 50000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

client_list = []


class timekeeper(threading.Thread):

    def __init__(self, time, isConnection):

        threading.Thread.__init__(self)
        self.time = time
        self.isRunning = True
        self.isConnection = isConnection

    def run(self):

        global server_socket
        for i in range(self.time):
            print(i)
            if self.isRunning is True:
                sendMessage(client_list, "Time Over")

        if self.isConnection is True:
            server_socket.close()


def sendMessage(clientList, message):

    for client in clientList:
        client.send(message)


def connection():

    global client_list
    timer = timekeeper(60, True)
    timer.start()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        




def main():
