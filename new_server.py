import socket
import random
import threading
from time import sleep
<<<<<<< HEAD
=======
import os
import sys
sys.path.append(os.path.abspath("/Python/FinalProject"))
from client_class import client
>>>>>>> e9eb2e731aa374e77b662865121b943ed3a24aae


SERVER_IP = 'localhost'
SERVER_PORT = 50000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
current_keeper = 0
call_count = 0
highest_bidder = None
is_recieving = True
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


class client(threading.Thread):

    def __init__(self, client_socket, client_address, money):

        threading.Thread.__init__(self)
        self.my_socket = client_socket
        self.my_address = client_address
        self.money = money
        self.items = {}
        self.name = self.my_socket.fileno()
        self.is_bankrupt = False

    def update(self, item, price):

        try:
            self.items[item] += 1
        except KeyError:
            self.items[item] = 1

        self.money -= price

    def send(self, msg):

        byte_msg = bytes(msg, 'utf-8')
        self.my_socket.send(byte_msg)

    def run(self):

        global current_keeper
        global call_count
        global highest_bidder

        while True:
            try:
                data = self.my_socket.recv(1024)
                if is_recieving == False:
                    break
            except:
                print("Connection with %d lost!" % (self.name))

            if data == 'CALL':
                call_count += 1
                current_keeper = call_count
                highest_bidder = self.name
                new_keeper = timekeeper(3, None, False, call_count)
                new_keeper.start()

                sendMessage(client_list, "{} bid!".format(self.name))


# pragma timekeeper


class timekeeper(threading.Thread):

    def __init__(self, time, server_socket, is_connection, name):

        threading.Thread.__init__(self)
        self.time = time
        self.isRunning = True
        self.server_socket = server_socket
        self.name = name
        self.is_connection = is_connection

    def check(self):

        return current_keeper == self.name

    def run(self):

        global is_recieving
        for i in range(self.time):

            if self.check() is False:
                break
            sleep(1)
            print(i)

        if self.is_connection is True:
            self.server_socket.close()

        if self.check() is True:
            is_recieving = False


def sendMessage(clientList, message):

    for client in clientList:
        client.send(message)


def connection():

    global client_list

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()

<<<<<<< HEAD
    while len(client_list) <= 4:
=======
    timer = timekeeper(60, server_socket, True, -1)
    timer.start()

    while True:
>>>>>>> 1fdca41d7ad610ef8ad127b914a5801c47fcf8b8

        try:
            client_socket, client_address = server_socket.accept()
        except:
            break

        new_client = client(client_socket, client_address, START_MONEY)
        client_list.append(new_client)

        print("Waiting for players...({}/4)".format(len(client_list)))

<<<<<<< HEAD

#
def timeOut():
    pass

# 경매
# 각 클라이언트마다 이 스레드를 가지고 있다
=======
# pragma timeout


def timeOut():
    pass

# pragma auction
>>>>>>> 1fdca41d7ad610ef8ad127b914a5801c47fcf8b8


def auctionTime():

    global current_keeper
    global call_count
    current_keeper = 0
    call_count = 0

    for client in client_list:
        client.start()

    for client in client_list:
        client.join()


# pragma MAIN
def main():

    connect_thread = threading.Thread(target=connection)
    connect_thread.start()
    connect_thread.join()
<<<<<<< HEAD
    for i in client_list:
        thread_timeOut = threading.Thread(target=timeOut, args=(client_sock, ))
        thread_timeOut.start()
        thread_auctionTime = threading.Thread(
            target=timeOut, args=(client_sock, ))
        thread_auctionTime.start()
=======


if __name__ == '__main__':
    main()








>>>>>>> 1fdca41d7ad610ef8ad127b914a5801c47fcf8b8
