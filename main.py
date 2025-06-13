import pygame
import sys
import time

# 屏幕与格子设置
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 32
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
LIGHT_RED = (255, 200, 200)
ORANGE = (255, 165, 0)

# 迷宫地图
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

player_pos = [1, 1]
guard_pos = [1, 8]
guard_path = [(1, 8), (5, 8)]
guard_index = 0

got_treasures = 0
total_treasures = sum(row.count(2) for row in maze)

bombs = []
explosions = []

def draw_maze(screen):
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
    x, y = player_pos
    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, GREEN, rect)

def draw_guard(screen):
    x, y = guard_pos
    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, RED, rect)
    for i in range(1, 4):
        vy = y + i
        if vy >= ROWS or maze[vy][x] == 1:
            break
        vrect = pygame.Rect(x*TILE_SIZE, vy*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, LIGHT_RED, vrect)

def draw_bombs(screen):
    for bx, by, _ in bombs:
        rect = pygame.Rect(bx*TILE_SIZE, by*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, ORANGE, rect)

def draw_explosions(screen):
    for ex, ey, _ in explosions:
        rect = pygame.Rect(ex*TILE_SIZE, ey*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, rect)

def check_guard_sight():
    gx, gy = guard_pos
    px, py = player_pos
    if px == gx and py > gy and py - gy <= 3:
        for y in range(gy + 1, py):
            if maze[y][gx] == 1:
                return False
        return True
    return False

def move_guard():
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

def explode(x, y):
    positions = [(x, y)]
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        for i in range(1, 3):
            nx, ny = x + dx*i, y + dy*i
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if maze[ny][nx] == 1:
                    break
                positions.append((nx, ny))
    return positions

def run():
    global got_treasures
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("小偷游戏 - 炸弹迷宫")
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        draw_maze(screen)
        draw_guard(screen)
        draw_player(screen)
        draw_bombs(screen)
        draw_explosions(screen)

        now = time.time()

        for bx, by, t in bombs[:]:
            if now - t >= 2:
                area = explode(bx, by)
                for pos in area:
                    explosions.append((pos[0], pos[1], now))
                bombs.remove((bx, by, t))

        for ex, ey, t in explosions[:]:
            if now - t >= 1:
                explosions.remove((ex, ey, t))

        for ex, ey, _ in explosions:
            if (guard_pos[0], guard_pos[1]) == (ex, ey):
                show_end_screen(screen, "守卫被炸晕，胜利！", GREEN)
                pygame.quit()
                return

        if check_guard_sight():
            show_end_screen(screen, "你被发现了！游戏失败", RED)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x, y = player_pos
                    if maze[y][x] == 0:
                        bombs.append((x, y, now))

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_DOWN]: dy = 1
        if keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_RIGHT]: dx = 1

        if dx or dy:
            nx, ny = player_pos[0] + dx, player_pos[1] + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] != 1:
                player_pos[0], player_pos[1] = nx, ny

        x, y = player_pos
        if maze[y][x] == 2:
            got_treasures += 1
            maze[y][x] = 0

        if maze[y][x] == 3:
            if got_treasures == total_treasures:
                show_end_screen(screen, "你成功逃脱了！胜利！", GREEN)
                break

        move_guard()
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    run()
