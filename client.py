import socket
import threading
from gui import *
import pickle


# 접속할 서버의 정보
server_ip = '127.0.0.1'
server_port = 50000
address = (server_ip, server_port)
game_started = False

# 소켓을 이용해서 서버에 접속
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(address)


def callGUI():
    # 스레드 종료 키
    thread_end = 0

    TARGET_FPS = 10
    clock = pygame.time.Clock()
    play = True

    screen = window()

    # 접속 대기 화면
    waiting(screen)

    # 닉네임 입력 화면
    username = nickname(screen)
    mysock.send(bytes(username, 'utf-8'))

    while True:
        if game_started:
            break

    money = 0

    # 화면 설정
    window_deco(screen)
    while play:
        clock.tick(TARGET_FPS)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit

        # 테스트!!!
        player1 = player(screen, username, 0, 200, 0)
        player2 = player(screen, 'dimen', 1, 200, 0)
        player3 = player(screen, '수령', 2, 200, 0)
        player4 = player(screen, '황냥이', 3, 200, 0)
        player1.info()
        player2.info()
        player3.info()
        player4.info()
        player1.take_my_money(10)
        player1.take_my_money(money)
        player3.take_my_money(30)
        player2.take_my_money(10)
        player4.take_my_money(40)

        # ** 금액 입력받는 부분 만들어야함 **
        money = call(screen)

        # 사용자 행위

        # 게임 창에 적용
        pygame.display.update()


# 서버가 보내는 메시지를 수신할 함수 | Thread 활용
def receive():
    global mysock
    while True:
        try:
            data = mysock.recv(1024)

            try:
                data_dict = pickle.loads(data)
                print(data_dict)

            except:
                data = data.decode('UTF-8')

                if(data == 'end'):
                    mysock.send(bytes("end", 'UTF-8'))
                if(data == 'start_game'):
                    global game_started
                    game_started = True

                print(data)

        except OSError:
            print('연결이 종료되었습니다.')
            break

    mysock.close()


# 메시지를 수신할 스레드 생성 및 실행
thread_recv = threading.Thread(target=receive, args=())
thread_recv.start()
callGUI()
print("Started!")


# 메시지 전송 및 판단
while True:
    try:
        data = input('>')
    except KeyboardInterrupt:
        break

    if data == '!quit' or '':
        break
    elif data == 'CALL':
        mysock.send(bytes(data, 'utf-8'))
    else:
        print("To Bid, enter 'CALL'")
        continue

# 서버 접속 종료
mysock.close()
print("disconneted")
