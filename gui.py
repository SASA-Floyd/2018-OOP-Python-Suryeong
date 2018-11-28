# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

# pygame 초기화
pygame.init()

# pygame에서 사용할 변수 선언
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = ( 47, 157,  39)
RED   = (255,   0,   0)
YELLOW= (255, 187,   0)
fontObj = pygame.font.SysFont('Arial.ttf', 18)

pygame.init()

# 플레이어 기본 화면 구성
def window():
    screen = pygame.display.set_mode([1000, 600])
    pygame.display.set_caption('Blue Block')
    screen.fill(YELLOW)

    # 기본 화면 구획
    pygame.draw.rect(screen, WHITE, [660, 70, 310, 500])    # 플레이어 정보 출력 부분
    pygame.draw.rect(screen, WHITE, [30, 420, 600, 150])    # 금액 입력 부분..?
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
    def present(self):
        pygame.draw.rect(self.screen, BLACK, [690, 90+120*self.turn, 250, 100])
        textSurfaceObj = fontObj.render(self.name, True, WHITE, BLACK)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (700, 100+120*self.turn)
        self.screen.blit(textSurfaceObj, textRectObj)


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
        player1 = player(screen, 'hwangsae', 0, 0)
        player2 = player(screen, 'foodduck', 1, 0)
        player3 = player(screen, 'yaho', 2, 0)
        player4 = player(screen, 'helpme', 3, 0)
        player1.present()
        player2.present()
        player3.present()
        player4.present()

        # 사용자 행위

        # 게임 창에 적용
        pygame.display.flip()