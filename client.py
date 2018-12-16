import socket
import threading
from gui import *
import pickle
from time import *


# 접속할 서버의 정보
server_ip = '127.0.0.1'
server_port = 50000
address = (server_ip, server_port)
game_started = False
player_no = 0
client_list = []
player_list = []
class_list = []
username = None
START_MONEY = 300
screen = 0

current_time = 5
current_price = 0
display_message = ''

# 소켓을 이용해서 서버에 접속
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(address)


class Client:

    def __init__(self, name):

        self.name = name
        self.money = START_MONEY
        self.item_list = {}

    def update(self, item, price):

        self.money -= price
        if item in self.item_list:
            self.item_list[item] += 1
        else:
            self.item_list.setdefault(item, 1)


def callGUI():
    # 스레드 종료 키
    global username
    global client_list
    global player_list
    global screen
    thread_end = 0

    TARGET_FPS = 10
    clock = pygame.time.Clock()
    play = True

    screen = window()

    # 접속 대기 화면
    # waiting(screen)

    # 닉네임 입력 화면
    username = nickname(screen)
    mysock.send(bytes(username, 'utf-8'))
    print(player_no)
    waiting_player(screen)
    while True:
        if game_started:
            break

    money = 0
    callcnt = 0
    # 화면 설정
    window_deco(screen)
    sleep(2)
    client_list.append('수령')
    client_list.append('황냥이')

    for client_name in client_list:
        new_client = Client(client_name)
        class_list.append(new_client)

    while play:
        clock.tick(TARGET_FPS)
        timer(screen, current_time)
        sleep(0.01)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit
        # 테스트!!!
        # player1 = player(screen, username, 0, 200, 0)
        # player2 = player(screen, 'dimen', 1, 200, 0)
        display_price(screen, current_price)
        message(screen, display_message)

        player1 = player(screen, client_list[0], 0, 200, {})
        player2 = player(screen, client_list[1], 1, 200, {})
        player3 = player(screen, '수령', 2, 200, {})
        player4 = player(screen, '황냥이', 3, 200, {})
        player_list = [player1, player2, player3, player4]

        for i in range(4):
            c = class_list[i]
            player_list[i].item = c.item_list
        # player1.take_my_money(callcnt*10)
        # player3.take_my_money(30)
        # player2.take_my_money(10)
        # player4.take_my_money(40)
        player1.info()
        player2.info()
        player3.info()
        player4.info()

        for i in range(4):
            c = class_list[i]
            player_list[i].take_my_money(c.money)

            # ** 금액 입력받는 부분 만들어야함 **
        call = call_button(screen)
        if call == 'CALL':
            callcnt += 1
            data = 'CALL'
            mysock.send(bytes(data, 'utf-8'))

        # 사용자 행위

        # 게임 창에 적용
        pygame.display.update()

# 서버가 보내는 메시지를 수신할 함수 | Thread 활용


def receive():

    global mysock
    global current_time
    global current_price
    global screen
    global display_message

    while True:
        try:
            data = mysock.recv(1024)

            try:
                data_dict = pickle.loads(data)
                print(data_dict)

            except:
                data = data.decode('UTF-8')
                if data.isdigit():
                    current_time = int(data)
                elif data.startswith('w'):
                    data = data.split(':')
                    person = data[1]
                    item = data[3]
                    for player in class_list:
                        if player.name == person:
                            player.update(item, current_price)
                    current_price = 0

                elif data.startswith('b'):
                    current_price += 10

                elif data.startswith('v'):
                    turn = int(data[1:])
                    crown_for_winner(screen, turn)

                elif data.startswith('@'):
                    print("====================")
                    print(display_message)
                    display_message = data[1:]

                elif(data == 'player_number'):
                    global player_no
                    player_no = int(mysock.recv(1024).decode('UTF-8'))

                elif(data == 'end'):
                    mysock.send(bytes("end", 'UTF-8'))
                    # current_price = 0

                elif(data == 'start_game'):
                    global game_started
                    game_started = True

                elif(data == 'client_list'):
                    global client_list
                    data = mysock.recv(1024)
                    client_list = pickle.loads(data).copy()

                elif data.startswith('r'):
                    data = mysock.recv(1024)
                    data_dict = pickle.loads(data)
                    message(screen, "Required items are...")
                    sleep(2)
                    for key in data_dict:
                        message(screen, "{}: {} Required".format(
                            key, data_dict[key]))
                        sleep(2)

                # try:
                #     if data.split(':')[0] == 'accept':
                #         print(data)
                #         answer = input("거래 승낙?")
                # except:
                #     print(data)

                print(data)

        except OSError:
            print('연결이 종료되었습니다.')
            break

    mysock.close()


# 메시지를 수신할 스레드 생성 및 실행
thread_recv = threading.Thread(target=receive, args=())
thread_recv.start()
# YOU NEED TO FIX HERE!!! MAKE IT TO A THREAD
callGUI()
print("Started!")


while True:
    try:
        data = input('>')
    except KeyboardInterrupt:
        break

    if data == '!quit' or '':
        break
    elif data == 'CALL':
        mysock.send(bytes(data, 'utf-8'))
    elif data.split()[0] == "request":
        product, price = input("어떤걸, 얼마에?").split()
        msg = "request:{0}:{1}:{2}:NULL".format(username, product, price)
        mysock.send(bytes(msg, 'utf-8'))
    else:
        print("To Bid, enter 'CALL'")
        continue

# 메시지 전송 및 판단
# 서버 접속 종료
mysock.close()
print("disconneted")
