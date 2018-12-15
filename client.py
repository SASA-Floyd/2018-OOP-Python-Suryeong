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
client_dict = {}
username = None
START_MONEY = 300


current_time = 0
is_bought = False




# 소켓을 이용해서 서버에 접속
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(address)


class Client:
    
    def __init__(self, name):
        
        self.name = name
        self.money = START_MONEY
        self.item_list = []
        
    def update(self, item, price):
        
        self.money -= price
        self.item_list.append(item)
    



def callGUI():
    # 스레드 종료 키
    global username
    global client_list
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

    for client_name in client_list:
        new_client = Client(client_name)
        client_dict.setdefault(client_name, new_client)

    while play:
        clock.tick(TARGET_FPS)
        sleep(0.01)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit
        # 테스트!!!
        # player1 = player(screen, username, 0, 200, 0)
        # player2 = player(screen, 'dimen', 1, 200, 0)
        player1 = player(screen, client_list[0], 0, 200, 0)
        player2 = player(screen, client_list[1], 1, 200, 0)
        player3 = player(screen, '수령', 2, 200, 0)
        player4 = player(screen, '황냥이', 3, 200, 0)
        player1.info()
        player2.info()
        player3.info()
        player4.info()
        player1.take_my_money(callcnt*10)
        player3.take_my_money(30)
        player2.take_my_money(10)
        player4.take_my_money(40)

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
                if(data == 'player_number'):
                    global player_no
                    player_no = int(mysock.recv(1024).decode('UTF-8'))

                if(data == 'end'):
                    mysock.send(bytes("end", 'UTF-8'))

                if(data == 'start_game'):
                    global game_started
                    game_started = True

                if(data == 'client_list'):
                    global client_list
                    data = mysock.recv(1024)
                    client_list = pickle.loads(data).copy()

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
