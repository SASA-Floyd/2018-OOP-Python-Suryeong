import socket
import random
import threading
from time import sleep
import os
import sys
sys.path.append(os.path.abspath("/Python/FinalProject"))
from client_class import client


SERVER_IP = 'localhost'
SERVER_PORT = 50000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

client_list = []
START_MONEY = 300


class timekeeper(threading.Thread):

    def __init__(self, time, server_socket, isConnection=False):

        threading.Thread.__init__(self)
        self.time = time
        self.isRunning = True
        self.server_socket = server_socket
        self.isConnection = isConnection

    def run(self):

        for i in range(self.time):
            print(i)
            if self.isRunning is True:
                sendMessage(client_list, "Time Over")

        if self.isConnection is True:
            self.server_socket.close()


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

        try:
            client_socket, client_address = server_socket.accept()
        except:
            break

        new_client = client(client_socket, client_address, START_MONEY)
        client_list.append(new_client)


def timeOut():
    pass


def auctionTime():
    pass


def main():

    connect_thread = threading.Thread(target=connection)
    connect_thread.start()
    connect_thread.join()
