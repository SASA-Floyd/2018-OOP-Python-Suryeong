# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

# pygame 초기화
pygame.init()

# pygame에서 사용할 변수 선언
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
GREEN = (0, 128,   0)
RED = (255,   0,   0)
YELLOW = (255, 187,   0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)


# 플레이어 기본 화면 구성
def window():
    screen = pygame.display.set_mode([1000, 600], 0, 32)
    pygame.display.set_caption('Blue Brick')
    screen.fill(YELLOW)

    # 기본 화면 구획
    pygame.draw.rect(screen, WHITE, [660, 70, 310, 500])    # 플레이어 정보 출력 부분
    pygame.draw.rect(screen, BLACK, [30, 470, 600, 100])    # 금액 입력 부분..?
    pygame.draw.rect(screen, WHITE, [28, 468, 604, 104], 4)
    pygame.draw.rect(screen, GREEN, [30, 70, 600, 200])     # 아이템 제시 및 기타 정보

    return screen


# 플레이어 정보 출력
class player:
    def __init__(self, screen, name, turn, item):
        self.name = name
        self.screen = screen
        self.item = item
        self.turn = turn

    # 플레이어의 정보를 띄우는 함수
    def info(self):
        # 배경 설정
        pygame.draw.rect(self.screen, SILVER, [
                         680, 90+120*self.turn, 270, 100])
        # 이미지 출력
        pygame.draw.rect(self.screen, BLACK, [30+157*self.turn, 378, 130, 90])
        # 플레이어 이름 출력
        try:
            font = pygame.font.Font('fonts\\aJJinbbangB.ttf', 18)
            text = font.render(self.name, True, BLACK, None)
            textRect = text.get_rect()
            textRect.center = (730, 105+120*self.turn)
            self.screen.blit(text, textRect)
        except:
            print("no font file")
            pass
        # 플레이어 아이템 출력

    # 플레이어가 제시한 금액을 띄우는 함수
    def take_my_money(self, money):
        # 금액 출력
        pass


# 채팅창(보류)
class chat:
    pass


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

        # 테스트!!!
        player1 = player(screen, '황새', 0, 0)
        player2 = player(screen, 'foodduck', 1, 0)
        player3 = player(screen, 'yaho', 2, 0)
        player4 = player(screen, 'helpme', 3, 0)
        player1.info()
        player2.info()
        player3.info()
        player4.info()

        # 사용자 행위

        # 게임 창에 적용
        pygame.display.update()
