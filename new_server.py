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
client_id = []
client_class_list = []

START_MONEY = 300

# "Item name": Available Number
item_dict = {
    "빨간 벽돌": 6,
    "파란 벽돌": 1,
    "나무 합판": 3,
    "철근": 2,
    "시멘트": 3,
    "수령님의 평양냉면": 1,
    "멸종위기동물 황새": 1
}

print("********BLUE BRICK********")
print("Waiting for players...({}/4)".format(len(client_list)))


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

    while len(client_list) <= 4:

        try:
            client_socket, client_address = server_socket.accept()
        except:
            break

        new_client = client(client_socket, client_address, START_MONEY)
        client_list.append(new_client)

        print("Waiting for players...({}/4)".format(len(client_list)))


#
def timeOut():
    pass

# 경매
# 각 클라이언트마다 이 스레드를 가지고 있다


def auctionTime():
    pass


def main():

    connect_thread = threading.Thread(target=connection)
    connect_thread.start()
    connect_thread.join()
    for i in client_list:
        thread_timeOut = threading.Thread(target=timeOut, args=(client_sock, ))
        thread_timeOut.start()
        thread_auctionTime = threading.Thread(
            target=timeOut, args=(client_sock, ))
        thread_auctionTime.start()
