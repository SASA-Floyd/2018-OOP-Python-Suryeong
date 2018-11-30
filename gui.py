# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import pygame_textinput

# pygame 초기화
pygame.init()

# pygame에서 사용할 색상
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
GREEN = (0, 128,   0)
RED = (255,   0,   0)
YELLOW = (255, 187,   0)
SILVER = (192, 192, 192)

# 사용할 기본 아이템
'''
rb = pygame.image.load('')
bb = pygame.image.load('')
wd = pygame.image.load('')
fe = pygame.image.load('')
cm = pygame.image.load('')
su = pygame.image.load('')
hw = pygame.image.load('')
'''

# 플레이어 이미지
p1 = pygame.image.load('images\\hwangsae.png')
p2 = pygame.image.load('images\\sooryeong.png')
p3 = pygame.image.load('images\\hwangsae.png')
p4 = pygame.image.load('images\\sooryeong.png')
img = [p1, p2, p3, p4]


# 플레이어 기본 창
def window():
    screen = pygame.display.set_mode([1000, 600], 0, 32)
    pygame.display.set_caption('Blue Brick')
    return screen

# 플레이 화면 구성
def window_deco(screen):
    # 기본 화면 구획
    bgi = pygame.image.load('images\\wall1.png')    # 백그라운드 이미지
    screen.blit(bgi, (0, 0))
    pygame.draw.rect(screen, BLACK, [660, 70, 310, 500])    # 플레이어 정보 출력 부분
    pygame.draw.rect(screen, BLACK, [30, 470, 600, 100])    # 금액 입력 부분
    pygame.draw.rect(screen, WHITE, [28, 468, 604, 104], 5)
    pygame.draw.rect(screen, GREEN, [30, 70, 600, 200])     # 아이템 제시 및 기타 정보
    pygame.draw.rect(screen, SILVER, [30, 70, 600, 200], 5)
    # 보유금액 표시 부분
    pygame.draw.rect(screen, WHITE, [410, 495, 200, 50], 4)
    font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 18)
    text = font.render('보유금액', True, WHITE, None)
    screen.blit(text, [420, 510])
    # 타이머 표시 부분
    pygame.draw.rect(screen, BLACK, [530, 150, 80, 100])
    font = pygame.font.Font('fonts\\aJeonjaSigye.ttf', 16)
    text = font.render('TIMER', True, WHITE, None)
    textRect = text.get_rect()
    textRect.center = (570, 160)
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
        pygame.draw.rect(self.screen, SILVER, [
                         680, 90+120*self.turn, 270, 100])
        # 플레이어 이미지 출력
        screen.blit(img[self.turn], (30+157*self.turn, 150))
        pygame.draw.rect(self.screen, BLACK, [30 + 157 * self.turn, 375, 130, 90])
        pygame.draw.rect(self.screen, WHITE, [30 + 157 * self.turn, 375, 130, 90], 4)
        # 플레이어 이름 출력
        font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 18)
        text = font.render(self.name, True, BLACK, None)
        self.screen.blit(text, [695, 105 + 120 * self.turn])
        # 플레이어 아이템 출력
        # 플레이어 보유금액 출력

    # 플레이어가 제시한 금액을 띄우는 함수
    def take_my_money(self, money):
        # 금액 출력
        pygame.draw.rect(self.screen, BLACK, [30 + 157 * self.turn, 375, 130, 90])
        pygame.draw.rect(self.screen, WHITE, [30 + 157 * self.turn, 375, 130, 90], 4)
        font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 48)
        if money != 0:
            text = font.render(str(money), True, YELLOW, None)
            textRect = text.get_rect()
            textRect.center = (95+158*self.turn, 420)
            self.screen.blit(text, textRect)


# 금액 입력 기능(아직ㅠㅜ)
def call(screen):
    textinput = pygame_textinput.TextInput('금액을 입력하세요.','fonts\\aJJinbbangB.ttf', 35, True, WHITE, WHITE)
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        textinput.update(events)
        screen.blit(textinput.get_surface(), (50, 490))


if __name__ == '__main__':
    TARGET_FPS = 10
    clock = pygame.time.Clock()
    play = True

    while play:
        clock.tick(TARGET_FPS)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        # 화면 설정
        screen = window()
        window_deco(screen)


        # 테스트!!!
        player1 = player(screen, '황새', 0, 200, 0)
        player2 = player(screen, 'dimen', 1, 200, 0)
        player3 = player(screen, '수령', 2, 200, 0)
        player4 = player(screen, '???', 3, 200, 0)
        player1.info()
        player2.info()
        player3.info()
        player4.info()
        call(screen)
        player1.take_my_money(10)
        player1.take_my_money(20)
        player3.take_my_money(30)
        player3.take_my_money(0)
        player4.take_my_money(40)

        # 사용자 행위

        # 게임 창에 적용
        pygame.display.update()
