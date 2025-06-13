import pygame
from config import TILE_SIZE, RED, LIGHT_RED, ROWS, maze

guard_pos = [1, 8]
guard_path = [(1, 8), (5, 8)]
guard_index = 0

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

def check_guard_sight(player_pos, maze):
    gx, gy = guard_pos
    px, py = player_pos
    if px == gx and py > gy and py - gy <= 3:
        for y in range(gy + 1, py):
            if maze[y][gx] == 1:
                return False
        return True
    return False

def move_guard():
    global guard_index, guard_pos
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
