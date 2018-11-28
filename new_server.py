import socket
import random
import threading
from time import sleep


SERVER_IP = 'localhost'
SERVER_PORT = 50000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)

# 3초세는거 하기 위한 전역변수
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

    # 물건을 샀을때 업데이트
    def update(self, item, price):

        try:
            self.items[item] += 1
        except KeyError:
            self.items[item] = 1

        self.money -= price

    # 클라이언트에게 메세지 보내기
    def send(self, msg):

        byte_msg = bytes(msg, 'utf-8')
        self.my_socket.send(byte_msg)

    # 입찰 요청 받고 처리
    def run(self):

        # 가장 최근에 call한 사용자가 호출한 타이머
        global call_count
        # 가장 최근 호출한 사용자
        global highest_bidder

        while True:
            try:
                if is_recieving == False:
                    break
                data = self.my_socket.recv(1024)

            except:
                print("Connection with %d lost!" % (self.name))

            if data == 'CALL':  # 콜을 받았을 경우
                # 변수 업데이
                call_count += 1
                highest_bidder = self.name
                # 새 타이머 시작
                # 타이머 이름은 호출 횟수와 같음
                # 가장 최근에 호출된 타이머를 판별하기 위해
                new_keeper = timekeeper(3, None, False, call_count)
                new_keeper.start()
                # 전체에게 메세지 보내기
                sendMessage(client_list, "{} bid!".format(self.name))


# pragma timekeeper

# 타이머 클래스
class timekeeper(threading.Thread):

    def __init__(self, time, server_socket, is_connection, name):

        threading.Thread.__init__(self)
        self.time = time
        self.isRunning = True
        self.server_socket = server_socket
        # 타이머에 이름 부여
        self.name = name
        # 이건 나중에 지울수도
        self.is_connection = is_connection

    # 현재 돌아가고 있는 타이머가 본인인지 체크
    def check(self):
        global call_count
        return call_count == self.name

    def run(self):

        global is_recieving
        global client_list
        # 3초세기
        for i in range(self.time):

            # 만일 현재 돌아가는 타이머가 본인이 아니라면,
            # 즉 내가 실행된 뒤 새로 입찰 요청이 와 타이머가 시작되었다면
            # 숫자세기를 멈춤
            if self.check() is False:
                break
            sleep(1)
            print(i)
            sendMessage(client_list, str(3-i))

        if self.is_connection is True:
            self.server_socket.close()

        if self.check() is True:
            is_recieving = False
            sendMessage(client_list, "end")


def sendMessage(clientList, message):

    for client in clientList:
        client.send(message)


def connection():

    global client_list

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


if __name_ '__main__':
    while True:
        main()
