import socket
import random
import threading
import copy
from time import sleep


SERVER_IP = 'localhost'
SERVER_PORT = 50000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
NUMBER_OF_PLAYER = 2

# 3초세는거 하기 위한 전역변수
current_keeper = 0
call_count = 0
highest_bidder = None
is_receiving = True

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

print("*******BLUE BRICK*******")
print("Waiting for players...({}/{})".format(len(client_list), NUMBER_OF_PLAYER))


class client(threading.Thread):

    def __init__(self, client_socket, client_address, money):

        threading.Thread.__init__(self)
        self.my_socket = client_socket
        self.my_address = client_address
        self.money = money
        self.nickname = None
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
        if self.money < 0:
            self.is_bankrupt = True
            self.send("파산!")

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

                data = self.my_socket.recv(1024)
                data = data.decode('utf-8')

                if is_receiving is False:
                    continue

            except:
                print("Connection with %d lost!" % (self.name))

            if data == 'CALL':  # 콜을 받았을 경우
                # 변수 업데이트
                call_count += 1
                highest_bidder = self
                # 새 타이머 시작
                # 타이머 이름은 호출 횟수와 같음
                # 가장 최근에 호출된 타이머를 판별하기 위해
                new_keeper = timekeeper(5, call_count)
                new_keeper.start()
                # 전체에게 메세지 보내기
                sendMessage(client_list, "{} bid!".format(self.nickname))
                sendMessage(
                    client_list, "Current price is {}".format(call_count*10))


# pragma timekeeper

# 타이머 클래스
class timekeeper(threading.Thread):

    def __init__(self, time, name):

        threading.Thread.__init__(self)
        self.time = time
        self.isRunning = True
        # 타이머에 이름 부여
        self.name = name

    # 현재 돌아가고 있는 타이머가 본인인지 체크

    def check(self):
        global call_count
        # 이 부분이 오류였음
        return int(call_count) == int(self.name)

    def run(self):

        global is_receiving
        global client_list

        # 3초세기
        print(self.time)
        for i in range(self.time):

            # 만일 현재 돌아가는 타이머가 본인이 아니라면,
            # 즉 내가 실행된 뒤 새로 입찰 요청이 와 타이머가 시작되었다면
            # 숫자세기를 멈춤
            print(self.check())
            if self.check() is False:
                break
            sendMessage(client_list, str(self.time-i))
            sleep(1)
            print(i)

        if self.check() is True:
            is_receiving = False
            sendMessage(client_list, "end")


def flagkeeper():

    while is_receiving is True:
        sleep(0.05)

    print('flag end')


def sendMessage(client_list, message):

    for client in client_list:
        client.send(message)


def connection():

    global client_list

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen()

    while len(client_list) < NUMBER_OF_PLAYER:

        try:
            client_socket, client_address = server_socket.accept()
        except:
            break

        new_client = client(client_socket, client_address, START_MONEY)
        nick = client_socket.recv(1024)
        nick = nick.decode('utf-8')
        new_client.nickname = nick
        client_list.append(new_client)

        print("Waiting for players...({}/{})".format(len(client_list), NUMBER_OF_PLAYER))

    print("Game Starts!")

    for c in client_list:
        c.start()


# 경매 물품 하나를 랜덤으로 선택 (반환값: 아이템 이름 문자열)
def randomSelect():
    random_item = random.choice(list(item_dict.keys()))
    item_dict[random_item] -= 1
    # 남아있는 물품이 없다면 삭제
    if item_dict[random_item] == 0:
        del item_dict[random_item]
    return random_item


def timeOut():
    pass


def auctionTime():

    global current_keeper
    global call_count
    global is_receiving
    current_keeper = 0
    call_count = 0
    is_receiving = True

    for client in client_list:
        client = copy.copy(client)

    rand_item = randomSelect()
    sendMessage(client_list, "This round's item is {}\n".format(rand_item))
    sendMessage(client_list, "Bidding Starts...")
    sleep(1)
    sendMessage(client_list, "now!")

    flag = threading.Thread(target=flagkeeper)
    flag.start()
    flag.join()

    # for client in client_list:
    #     client.join()

    print("{} won {}".format(highest_bidder, rand_item))
    sendMessage(client_list, "{} won {}".format(
        highest_bidder.nickname, rand_item))
    highest_bidder.update(rand_item, 10 * call_count)
    informMoney(client_list)

    if existsWinner():
        sendMessage(client_list, "{} won the game!!".format(
            highest_bidder.nickname))
        exit()


def existsWinner():
    for client in client_list:
        if "빨간 벽돌" in client.items and "파란 벽돌" in client.items:
            return True
    return False


def informMoney(clinet_list):
    for client in client_list:
        client.send("Left money: {}\n".format(client.money))
        client.send("Inventory: {}\n".format(client.items))


# pragma MAIN
def main():

    connection()
    while item_dict:
        auctionTime()


if __name__ == '__main__':
    while True:
        main()
