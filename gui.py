# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import pygame_textinput
import time

# pygame 초기화
pygame.init()

# pygame에서 사용할 색상
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
GREEN = (0, 128,   0)
RED = (255,   0,   0)
YELLOW = (255, 187,   0)
LIGHTYELLOW = (255, 255, 108)

# 사용할 기본 아이템
r = pygame.image.load('images\\redbrick.png')
b = pygame.image.load('images\\bluebrick.png')
w = pygame.image.load('images\\wood.png')
i = pygame.image.load('images\\iron.png')
c = pygame.image.load('images\\cement.png')
s = pygame.image.load('images\\pyeongyang.png')
h = pygame.image.load('images\\hwangbird.png')

# 플레이어 이미지
p1 = pygame.image.load('images\\hwangsae.png')
p2 = pygame.image.load('images\\sooryeong.png')
p3 = pygame.image.load('images\\justdimen.png')
p4 = pygame.image.load('images\\catthecat.png')
img = [p1, p2, p3, p4]


# 플레이어 기본 창
def window():
    screen = pygame.display.set_mode([1000, 600], 0, 32)
    pygame.display.set_caption('Blue Brick')
    return screen


def waiting_player(screen):
    screen.fill(BLACK)
    font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 25)
    text = font.render('다른 플레이어를 기다리는 중 . . .', True, WHITE, None)
    textRect = text.get_rect()
    textRect.center = (500, 300)
    screen.blit(text, textRect)
    pygame.display.update()


# 게임 접속할때까지 대기하는 화면
def waiting(screen):
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 20)
    text = font.render('접속 중 . . . ', True, WHITE, None)
    textRect = text.get_rect()
    textRect.center = (500, 300)
    screen.blit(text, textRect)
    pygame.display.update()


# 게임 접속시 닉네임을 입력받는 화면
def nickname(screen):
    screen.fill(BLACK)
    # 안내 문구
    font1 = pygame.font.Font('fonts\\aJJinbbangB.ttf', 30)
    font2 = pygame.font.Font('fonts\\aJJinbbangB.ttf', 15)
    text1 = font1.render('닉네임을 입력하세요(10자).', True, WHITE, None)
    text2 = font2.render('닉네임을 결정하셨다면 ENTER키를 누르세요.', True, WHITE, None)
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect1.center = (500, 250)
    textRect2.center = (500, 285)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    # 텍스트 입력 부분
    textinput1 = pygame_textinput.TextInput(
        '', 'fonts\\aJJinbbangB.ttf', 30, True, 9, WHITE, WHITE)
    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        pygame.draw.rect(screen, WHITE, [380, 300, 240, 80])    # 닉네임 입력 창
        pygame.draw.rect(screen, BLACK, [386, 306, 228, 68])

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 엔터키를 누르면 닉네임 리턴
            if event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                    name = textinput1.get_text()
                    return name

        textinput1.update(events)
        screen.blit(textinput1.get_surface(), (400, 325))
        pygame.display.update()
        clock.tick(30)


# 플레이 화면 구성


def window_deco(screen):
    # 기본 화면 구획
    bgi = pygame.image.load('images\\wall1.png')    # 백그라운드 이미지
    screen.blit(bgi, (0, 0))
    logo = pygame.image.load('images\\logo.png')
    screen.blit(logo, (0, 5))
    pygame.draw.rect(screen, WHITE, [655, 75, 320, 510])    # 플레이어 정보 출력 부분
    pygame.draw.rect(screen, BLACK, [660, 80, 310, 500])
    pygame.draw.rect(screen, BLACK, [30, 470, 600, 100])    # call 이루어지는 부분
    pygame.draw.rect(screen, WHITE, [28, 468, 604, 104], 5)
    pygame.draw.rect(screen, GREEN, [30, 80, 600, 200])     # 아이템 제시 및 기타 정보
    pygame.draw.rect(screen, LIGHTYELLOW, [30, 80, 600, 200], 8)
    # 보유금액 표시 부분
    pygame.draw.rect(screen, WHITE, [410, 495, 200, 50], 4)
    font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 18)
    text = font.render('가격:', True, WHITE, None)
    screen.blit(text, [420, 510])
    # 타이머 표시 부분
    pygame.draw.rect(screen, BLACK, [530, 100, 80, 100])
    font = pygame.font.Font('fonts\\aJeonjaSigye.ttf', 16)
    text = font.render('TIMER', True, WHITE, None)
    textRect = text.get_rect()
    textRect.center = (570, 110)
    screen.blit(text, textRect)
    return screen


# 플레이어 정보 출력
class player:
    def __init__(self, screen, name, turn, money, item):
        self.name = name
        self.screen = screen
        self.item = item
        self.turn = turn
        self.money = money

    # 플레이어의 정보를 띄우는 함수
    def info(self):
        # 아이템 띄울 배경 설정
        pygame.draw.rect(self.screen, WHITE, [
                         680, 100+120*self.turn, 270, 100])
        pygame.draw.rect(self.screen, BLACK, [684, 104+120*self.turn, 262, 92])
        # 플레이어 이미지 출력
        self.screen.blit(img[self.turn], (30+157*self.turn, 150))
        pygame.draw.rect(self.screen, BLACK, [
                         30 + 157 * self.turn, 375, 130, 90])
        pygame.draw.rect(self.screen, WHITE, [
                         30 + 157 * self.turn, 375, 130, 90], 4)
        pygame.draw.rect(self.screen, BLACK, [
                         30 + 157 * self.turn, 375, 130, 90])
        pygame.draw.rect(self.screen, WHITE, [
                         30 + 157 * self.turn, 375, 130, 90], 4)
        # 플레이어 이름 출력
        font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 18)
        text = font.render(self.name, True, WHITE, None)
        self.screen.blit(text, [695, 115 + 120 * self.turn])

        # 플레이어 아이템 출력
        cnt = 0
        if '빨간 벽돌' in self.item:
            value = self.item.get('빨간 벽돌')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        r, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        r, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value
        if '파란 벽돌' in self.item:
            value = self.item.get('파란 벽돌')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        b, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        b, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value
        if '나무 합판' in self.item:
            value = self.item.get('나무 합판')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        w, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        w, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value
        if '철근' in self.item:
            value = self.item.get('철근')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        i, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        i, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value
        if '시멘트' in self.item:
            value = self.item.get('시멘트')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        c, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        c, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value
        if '수령님의 평양냉면' in self.item:
            value = self.item.get('수령님의 평양냉면')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        s, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        s, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value
        if '멸종위기동물 황새' in self.item:
            value = self.item.get('멸종위기동물 황새')
            j = 0
            while j < value:
                if cnt+j >= 10:
                    self.screen.blit(
                        h, (695 + (cnt+j-10)*25, 165 + 120 * self.turn))
                else:
                    self.screen.blit(
                        h, (695 + (cnt+j)*25, 140 + 120 * self.turn))
                j += 1
            cnt += value

    # 플레이어가 제시한 금액을 띄우는 함수
    def take_my_money(self, money):
        # 금액 출력
        pygame.draw.rect(self.screen, BLACK, [
                         30 + 157 * self.turn, 375, 130, 90])
        pygame.draw.rect(self.screen, WHITE, [
                         30 + 157 * self.turn, 375, 130, 90], 4)
        font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 48)
        if money != 0:
            text = font.render(str(money), True, YELLOW, None)
            textRect = text.get_rect()
            textRect.center = (95+158*self.turn, 420)
            self.screen.blit(text, textRect)

# 타이머 위치에 시간 출력


def timer(screen, time):
    pygame.draw.rect(screen, BLACK, [530, 120, 80, 80])
    font3 = pygame.font.Font('fonts\\aJeonjaSigye.ttf', 60)
    text = font3.render(str(time), True, RED, None)
    textRect = text.get_rect()
    textRect.center = (570, 160)
    screen.blit(text, textRect)

# call 버튼


def call_button(screen):
    mouse = pygame.mouse.get_pos()
    if 55+200 > mouse[0] > 55 and 490+55 > mouse[1] > 490:
        # print("==============")
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, YELLOW, (55, 490, 200, 55), 4)
        pygame.draw.rect(screen, BLACK, (59, 494, 192, 47))
        font4 = pygame.font.Font("fonts\\aJJinbbangB.ttf", 33)
        bttext = font4.render("CALL", True, YELLOW, None)
        bttextRect = bttext.get_rect()
        bttextRect.center = (155, 517)
        screen.blit(bttext, bttextRect)
        if click[0] == 1:
            # print("++++++++++++++")
            return 'CALL'
    else:
        # print("^^^^^^^^^^^^^^^^^^")
        pygame.draw.rect(screen, WHITE, (55, 490, 200, 55), 4)
        pygame.draw.rect(screen, BLACK, (59, 494, 192, 47))
        font4 = pygame.font.Font("fonts\\aJJinbbangB.ttf", 33)
        bttext = font4.render("CALL", True, WHITE, None)
        bttextRect = bttext.get_rect()
        bttextRect.center = (155, 517)
        screen.blit(bttext, bttextRect)

    pygame.display.update()

# 보유금액 보여줌


def display_price(screen, price):
    pygame.draw.rect(screen, BLACK, [455, 500, 140, 40])
    font5 = pygame.font.Font("fonts\\aJJinbbangB.ttf", 25)
    text = font5.render(str(price), True, WHITE, None)
    textRect = text.get_rect()
    textRect.midright = (600, 520)
    screen.blit(text, textRect)

# 우승자 티내기


def crown_for_winner(screen, turn):
    crown = pygame.image.load("images\\crown.png")
    screen.blit(crown, (35 + 157 * turn, 150))

# 전체 공지 칠판에 띄우기


old_text = ""


def message(screen, text):
    global old_text
    if text != old_text:
        pygame.draw.rect(screen, GREEN, [90, 140, 440, 70])
    font = pygame.font.Font("fonts\\aJJinbbangB.ttf", 22)
    textsurface = font.render(text, True, (255, 255, 255))
    screen.blit(textsurface, (90, 140))

    pass
    # textlist = []
    # pygame.draw.rect(screen, GREEN, [40, 90, 490, 150])
    # if len(text) > 25:
    #     textlist.append(text[0:25])
    #     textlist.append(text[25:])
    # font6 = pygame.font.Font("fonts\\aJJinbbangB.ttf", 25)
    # for i in textlist:
    #     showtext = font6.render(str(i), True, WHITE, None)
    #     showtextRect = showtext.get_rect()
    #     showtextRect.midleft = (50, 120 + 30 * textlist.index(i))
    #     screen.blit(showtext, showtextRect)


if __name__ == '__main__':
    TARGET_FPS = 30
    clock = pygame.time.Clock()
    play = True

    screen = window()

    # 접속 대기 화면
    waiting(screen)

    # 닉네임 입력 화면
    username = nickname(screen)

    callcnt = 0

    # 화면 설정
    window_deco(screen)
    while play:
        clock.tick(TARGET_FPS)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit

        text = '안녕하세요, 참가자 여러분! test입니다. 하하하하하하하하'
        messege(screen, text)

        call = call_button(screen)
        if call == 'CALL':
            callcnt += 1

        timer(screen, 3)

        # 테스트!!!
        player1 = player(screen, username, 0, 200, {
            "빨간 벽돌": 6,
            "파란 벽돌": 1,
            "나무 합판": 3,
            "철근": 2,
            "시멘트": 4,
            "수령님의 평양냉면": 1,
            "멸종위기동물 황새": 1
        })
        player2 = player(screen, 'dimen', 1, 200, {'철근': 2})
        player3 = player(screen, '수령', 2, 200, {'빨간 벽돌': 2, '철근': 1})
        player4 = player(screen, '황냥이', 3, 200, {})
        player1.info()
        player2.info()
        player3.info()
        player4.info()
        player1.take_my_money(10)
        player3.take_my_money(30)
        player2.take_my_money(10)
        player4.take_my_money(40)

        display_price(screen, 200+callcnt*10)

        crown_for_winner(screen, 3)

        # 게임 창에 적용
        pygame.display.update()
