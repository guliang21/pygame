"""五子棋之人人对战"""

import sys
import pygame
from pygame.locals import *
import pygame.gfxdraw
from checkerboard import Checkerboard, BLACK_CHESSMAN, WHITE_CHESSMAN, Point

SIZE = 30  # 棋盘每个点时间的间隔
Line_Points = 19  # 棋盘每行/每列点数
Outer_Width = 20  # 棋盘外宽度
Border_Width = 4  # 边框宽度
Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width  # 边框线的长度
Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width  # 网格线起点（左上角）坐标
SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2  # 游戏屏幕的高
SCREEN_WIDTH = SCREEN_HEIGHT + 200  # 游戏屏幕的宽

Stone_Radius = SIZE // 2 - 3  # 棋子半径
Stone_Radius2 = SIZE // 2 + 3
Checkerboard_Color = (0xE3, 0x92, 0x65)  # 棋盘颜色
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)
BLACK_STONE_COLOR = (45, 45, 45)
WHITE_STONE_COLOR = (219, 219, 219)

RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('五子棋')

    font1 = pygame.font.SysFont('SimHei', 36)
    font2 = pygame.font.SysFont('SimHei', 72)
    fwidth, fheight = font2.size('黑方获胜')

    checkerboard = Checkerboard(Line_Points)
    cur_runner = BLACK_CHESSMAN
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if winner is not None:
                        winner = None
                        cur_runner = BLACK_CHESSMAN
                        checkerboard = Checkerboard(Line_Points)
            elif event.type == MOUSEBUTTONDOWN:
                if winner is None:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        click_point = _get_clickpoint(mouse_pos)
                        if click_point is not None:
                            if checkerboard.can_drop(click_point):
                                winner = checkerboard.drop(cur_runner, click_point)
                                if cur_runner == BLACK_CHESSMAN:
                                    cur_runner = WHITE_CHESSMAN
                                else:
                                    cur_runner = BLACK_CHESSMAN
                        else:
                            print('超出棋盘区域')

        # 画棋盘
        _draw_checkerboard(screen)

        # 画棋盘上已有的棋子
        for i, row in enumerate(checkerboard.checkerboard):
            for j, cell in enumerate(row):
                if cell == BLACK_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                elif cell == WHITE_CHESSMAN.Value:
                    _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

        _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + 20), BLACK_STONE_COLOR)
        _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + 20 + Stone_Radius2 * 3), WHITE_STONE_COLOR)

        if winner:
            print_text(screen, font2, (SCREEN_WIDTH - fwidth)//2, (SCREEN_HEIGHT - fheight)//2, winner.Name + '获胜', RED_COLOR)

        if cur_runner == BLACK_CHESSMAN:
            print_text(screen, font1, RIGHT_INFO_POS_X, Start_X, '获胜' if winner else '落子中', BLUE_COLOR)
        else:
            print_text(screen, font1, RIGHT_INFO_POS_X, Start_X + Stone_Radius2 * 3, '获胜' if winner else '落子中', BLUE_COLOR)

        pygame.display.flip()


# 画棋盘
def _draw_checkerboard(screen):
    # 填充棋盘背景色
    screen.fill(Checkerboard_Color)
    # 画棋盘网格线外的边框
    pygame.draw.rect(screen, BLACK_COLOR, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)
    # 画网格线
    for i in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_Y, Start_Y + SIZE * i),
                         (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                         1)
    for j in range(Line_Points):
        pygame.draw.line(screen, BLACK_COLOR,
                         (Start_X + SIZE * j, Start_X),
                         (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                         1)
    # 画星位和天元
    for i in (3, 9, 15):
        for j in (3, 9, 15):
            if i == j == 9:
                radius = 5
            else:
                radius = 3
            # pygame.draw.circle(screen, BLACK, (Start_X + SIZE * i, Start_Y + SIZE * j), radius)
            pygame.gfxdraw.aacircle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)
            pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)


# 画棋子
def _draw_chessman(screen, point, stone_color):
    # pygame.draw.circle(screen, stone_color, (Start_X + SIZE * point.X, Start_Y + SIZE * point.Y), Stone_Radius)
    pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
    pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)


def _draw_chessman_pos(screen, pos, stone_color):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
    pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)


# 根据鼠标点击位置，返回游戏区坐标
def _get_clickpoint(click_pos):
    pos_x = click_pos[0] - Start_X
    pos_y = click_pos[1] - Start_Y
    if pos_x < -Inside_Width or pos_y < -Inside_Width:
        return None
    x = pos_x // SIZE
    y = pos_y // SIZE
    if pos_x % SIZE > Stone_Radius:
        x += 1
    if pos_y % SIZE > Stone_Radius:
        y += 1
    if x >= Line_Points or y >= Line_Points:
        return None

    return Point(x, y)


if __name__ == '__main__':
    main()
