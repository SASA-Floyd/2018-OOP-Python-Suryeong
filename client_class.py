import socket
import threading


class client:

    def __init__(self, client_socket, client_address, money):
        self.my_socket = client_socket
        self.my_address = client_address
        self.money = money
        self.items = {}
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
<<<<<<< HEAD


    def run(self):

        while True:
            try:
                data = self.my_socket.recv(1024)
            except:
                print("Connection with %d lost!" % (self.my_socket.fileno()))

            if data == 'CALL':
                




        
=======
>>>>>>> e9eb2e731aa374e77b662865121b943ed3a24aae
