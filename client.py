import socket
import threading

# 접속할 서버의 정보
server_ip = '127.0.0.1'
server_port = 50000
address = (server_ip, server_port)

# 소켓을 이용해서 서버에 접속
mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(address)

nickname = input()
mysock.send(bytes(nickname, 'utf-8'))


# 스레드 종료 키
thread_end = 0


# 서버가 보내는 메시지를 수신할 함수 | Thread 활용
def receive():
    global mysock

    while True:
        try:
            data = mysock.recv(1024)
            data = data.decode('UTF-8')
            if(data == 'end'):
                mysock.send(bytes("end", 'UTF-8'))

            print(data)
        except OSError:
            print('연결이 종료되었습니다.')
            break

    mysock.close()


# 메시지를 수신할 스레드 생성 및 실행
thread_recv = threading.Thread(target=receive, args=())
thread_recv.start()
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
