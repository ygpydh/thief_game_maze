import pygame
import sys

# 屏幕与格子设置
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
ROWS = len(maze)
COLS = len(maze[0])


# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
LIGHT_RED = (255, 200, 200)

# 迷宫地图：0=空地，1=墙，2=宝藏，3=出口，9=敌人出生点
maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,2,0,0,3,1],
    [1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,0,0,1],
    [1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,2,0,1,0,1],
    [1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,9,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# 初始定位
player_pos = [1, 1]              # 玩家起始位置
guard_pos = [1, 8]               # 守卫起始位置（由地图中的9定义）
guard_path = [(1, 8), (5, 8)]    # 守卫巡逻路径
guard_index = 0                 # 当前目标路径点下标

# 宝藏统计
got_treasures = 0
total_treasures = sum(row.count(2) for row in maze)

def draw_maze(screen):
    # 绘制迷宫地图（墙、宝藏、出口）
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = maze[y][x]
            if tile == 1:
                pygame.draw.rect(screen, GRAY, rect)
            elif tile == 2:
                pygame.draw.rect(screen, YELLOW, rect)
            elif tile == 3:
                pygame.draw.rect(screen, BLUE, rect)

def draw_player(screen):
    # 绘制玩家
    x, y = player_pos
    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, GREEN, rect)

def draw_guard(screen):
    # 绘制守卫与其视野（向下3格）
    x, y = guard_pos
    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, RED, rect)
    for i in range(1, 4):
        vy = y + i
        if vy >= ROWS or maze[vy][x] == 1:
            break
        vrect = pygame.Rect(x*TILE_SIZE, vy*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, LIGHT_RED, vrect)

def check_guard_sight():
    # 判断玩家是否在守卫视野内
    gx, gy = guard_pos
    px, py = player_pos
    if px == gx and py > gy and py - gy <= 3:
        for y in range(gy + 1, py):
            if maze[y][gx] == 1:
                return False
        return True
    return False

def move_guard():
    # 守卫沿路径巡逻移动
    global guard_index
    gx, gy = guard_pos
    tx, ty = guard_path[guard_index]
    if gx < tx:
        guard_pos[0] += 1
    elif gx > tx:
        guard_pos[0] -= 1
    elif gy < ty:
        guard_pos[1] += 1
    elif gy > ty:
        guard_pos[1] -= 1
    else:
        guard_index = (guard_index + 1) % len(guard_path)

def show_end_screen(screen, message, color):
    # 游戏结束提示画面
    font = pygame.font.SysFont("Arial", 48)
    text = font.render(message, True, color)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                waiting = False

def run():
    global got_treasures
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("小偷游戏 - 夜间迷宫")
    clock = pygame.time.Clock()

    # 主循环
    while True:
        screen.fill(BLACK)
        draw_maze(screen)
        draw_guard(screen)
        draw_player(screen)

        # 守卫发现玩家则失败
        if check_guard_sight():
            show_end_screen(screen, "你被发现了！游戏失败", RED)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 读取玩家输入方向
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1

        # 判断新位置是否可走
        if dx or dy:
            nx, ny = player_pos[0] + dx, player_pos[1] + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] != 1:
                player_pos[0], player_pos[1] = nx, ny

        # 玩家当前位置处理
        x, y = player_pos
        if maze[y][x] == 2:
            got_treasures += 1
            maze[y][x] = 0
            print(f"你偷到了宝藏（{got_treasures}/{total_treasures}）")

        if maze[y][x] == 3:
            if got_treasures == total_treasures:
                show_end_screen(screen, "你成功逃脱了！胜利！", GREEN)
                break
            else:
                print("你还没偷完宝藏！")

        move_guard()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    run()
