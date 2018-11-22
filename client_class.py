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
