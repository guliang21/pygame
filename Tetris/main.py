import sys
import time
import pygame
from pygame.locals import *
import blocks

SIZE = 30  # 每个小方格大小
BLOCK_HEIGHT = 25  # 游戏区高度
BLOCK_WIDTH = 10   # 游戏区宽度
BORDER_WIDTH = 4   # 游戏区边框宽度
BORDER_COLOR = (40, 40, 200)  # 游戏区边框颜色
SCREEN_WIDTH = SIZE * (BLOCK_WIDTH + 5)  # 游戏屏幕的宽
SCREEN_HEIGHT = SIZE * BLOCK_HEIGHT      # 游戏屏幕的高
BG_COLOR = (40, 40, 60)  # 背景色
BLOCK_COLOR = (20, 128, 200)  #
BLACK = (0, 0, 0)
RED = (200, 30, 30)      # GAME OVER 的字体颜色


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('俄罗斯方块')

    font1 = pygame.font.SysFont('SimHei', 24)  # 黑体24
    font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
    font_pos_x = BLOCK_WIDTH * SIZE + BORDER_WIDTH + 10  # 右侧信息显示区域字体位置的X坐标
    gameover_size = font2.size('GAME OVER')
    font1_height = int(font1.size('得分')[1])

    cur_block = None   # 当前下落方块
    next_block = None  # 下一个方块
    cur_pos_x, cur_pos_y = 0, 0

    game_area = None    # 整个游戏区域
    game_over = True
    start = False       # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0           # 得分
    orispeed = 0.5      # 原始速度
    speed = orispeed    # 当前速度
    pause = False       # 暂停
    last_drop_time = None   # 上次下落时间
    last_press_time = None  # 上次按键时间

    def _dock():
        nonlocal cur_block, next_block, game_area, cur_pos_x, cur_pos_y, game_over, score, speed
        for _i in range(cur_block.start_pos.Y, cur_block.end_pos.Y + 1):
            for _j in range(cur_block.start_pos.X, cur_block.end_pos.X + 1):
                if cur_block.template[_i][_j] != '.':
                    game_area[cur_pos_y + _i][cur_pos_x + _j] = '0'
        if cur_pos_y + cur_block.start_pos.Y <= 0:
            game_over = True
        else:
            # 计算消除
            remove_idxs = []
            for _i in range(cur_block.start_pos.Y, cur_block.end_pos.Y + 1):
                if all(_x == '0' for _x in game_area[cur_pos_y + _i]):
                    remove_idxs.append(cur_pos_y + _i)
            if remove_idxs:
                # 计算得分
                remove_count = len(remove_idxs)
                if remove_count == 1:
                    score += 100
                elif remove_count == 2:
                    score += 300
                elif remove_count == 3:
                    score += 700
                elif remove_count == 4:
                    score += 1500
                speed = orispeed - 0.03 * (score // 10000)
                # 消除
                _i = _j = remove_idxs[-1]
                while _i >= 0:
                    while _j in remove_idxs:
                        _j -= 1
                    if _j < 0:
                        game_area[_i] = ['.'] * BLOCK_WIDTH
                    else:
                        game_area[_i] = game_area[_j]
                    _i -= 1
                    _j -= 1
            cur_block = next_block
            next_block = blocks.get_block()
            cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y

    def _judge(pos_x, pos_y, block):
        nonlocal game_area
        for _i in range(block.start_pos.Y, block.end_pos.Y + 1):
            if pos_y + block.end_pos.Y >= BLOCK_HEIGHT:
                return False
            for _j in range(block.start_pos.X, block.end_pos.X + 1):
                if pos_y + _i >= 0 and block.template[_i][_j] != '.' and game_area[pos_y + _i][pos_x + _j] != '.':
                    return False
        return True

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        score = 0
                        last_drop_time = time.time()
                        last_press_time = time.time()
                        game_area = [['.'] * BLOCK_WIDTH for _ in range(BLOCK_HEIGHT)]
                        cur_block = blocks.get_block()
                        next_block = blocks.get_block()
                        cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos.X - 1) // 2, -1 - cur_block.end_pos.Y
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    # 旋转
                    # 其实记得不是很清楚了，比如
                    # .0.
                    # .00
                    # ..0
                    # 这个在最右边靠边的情况下是否可以旋转，我试完了网上的俄罗斯方块，是不能旋转的，这里我们就按不能旋转来做
                    # 我们在形状设计的时候做了很多的空白，这样只需要规定整个形状包括空白部分全部在游戏区域内时才可以旋转
                    if 0 <= cur_pos_x <= BLOCK_WIDTH - len(cur_block.template[0]):
                        _next_block = blocks.get_next_block(cur_block)
                        if _judge(cur_pos_x, cur_pos_y, _next_block):
                            cur_block = _next_block

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not game_over and not pause:
                    if time.time() - last_press_time > 0.1:
                        last_press_time = time.time()
                        if cur_pos_x > - cur_block.start_pos.X:
                            if _judge(cur_pos_x - 1, cur_pos_y, cur_block):
                                cur_pos_x -= 1
            if event.key == pygame.K_RIGHT:
                if not game_over and not pause:
                    if time.time() - last_press_time > 0.1:
                        last_press_time = time.time()
                        # 不能移除右边框
                        if cur_pos_x + cur_block.end_pos.X + 1 < BLOCK_WIDTH:
                            if _judge(cur_pos_x + 1, cur_pos_y, cur_block):
                                cur_pos_x += 1
            if event.key == pygame.K_DOWN:
                if not game_over and not pause:
                    if time.time() - last_press_time > 0.1:
                        last_press_time = time.time()
                        if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                            _dock()
                        else:
                            last_drop_time = time.time()
                            cur_pos_y += 1

        _draw_background(screen)

        _draw_game_area(screen, game_area)

        _draw_gridlines(screen)

        _draw_info(screen, font1, font_pos_x, font1_height, score)
        # 画显示信息中的下一个方块
        _draw_block(screen, next_block, font_pos_x, 30 + (font1_height + 6) * 5, 0, 0)

        if not game_over:
            cur_drop_time = time.time()
            if cur_drop_time - last_drop_time > speed:
                if not pause:
                    # 不应该在下落的时候来判断到底没，我们玩俄罗斯方块的时候，方块落到底的瞬间是可以进行左右移动
                    if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                        _dock()
                    else:
                        last_drop_time = cur_drop_time
                        cur_pos_y += 1
        else:
            if start:
                print_text(screen, font2,
                           (SCREEN_WIDTH - gameover_size[0]) // 2, (SCREEN_HEIGHT - gameover_size[1]) // 2,
                           'GAME OVER', RED)

        # 画当前下落方块
        _draw_block(screen, cur_block, 0, 0, cur_pos_x, cur_pos_y)

        pygame.display.flip()


# 画背景
def _draw_background(screen):
    # 填充背景色
    screen.fill(BG_COLOR)
    # 画游戏区域分隔线
    pygame.draw.line(screen, BORDER_COLOR,
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, 0),
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, SCREEN_HEIGHT), BORDER_WIDTH)


# 画网格线
def _draw_gridlines(screen):
    # 画网格线 竖线
    for x in range(BLOCK_WIDTH):
        pygame.draw.line(screen, BLACK, (x * SIZE, 0), (x * SIZE, SCREEN_HEIGHT), 1)
    # 画网格线 横线
    for y in range(BLOCK_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, y * SIZE), (BLOCK_WIDTH * SIZE, y * SIZE), 1)


# 画已经落下的方块
def _draw_game_area(screen, game_area):
    if game_area:
        for i, row in enumerate(game_area):
            for j, cell in enumerate(row):
                if cell != '.':
                    pygame.draw.rect(screen, BLOCK_COLOR, (j * SIZE, i * SIZE, SIZE, SIZE), 0)


# 画单个方块
def _draw_block(screen, block, offset_x, offset_y, pos_x, pos_y):
    if block:
        for i in range(block.start_pos.Y, block.end_pos.Y + 1):
            for j in range(block.start_pos.X, block.end_pos.X + 1):
                if block.template[i][j] != '.':
                    pygame.draw.rect(screen, BLOCK_COLOR,
                                     (offset_x + (pos_x + j) * SIZE, offset_y + (pos_y + i) * SIZE, SIZE, SIZE), 0)


# 画得分等信息
def _draw_info(screen, font, pos_x, font_height, score):
    print_text(screen, font, pos_x, 10, f'得分: ')
    print_text(screen, font, pos_x, 10 + font_height + 6, f'{score}')
    print_text(screen, font, pos_x, 20 + (font_height + 6) * 2, f'速度: ')
    print_text(screen, font, pos_x, 20 + (font_height + 6) * 3, f'{score // 10000}')
    print_text(screen, font, pos_x, 30 + (font_height + 6) * 4, f'下一个：')


if __name__ == '__main__':
    main()
