import pygame
from config import TILE_SIZE, ORANGE, YELLOW, COLS, ROWS

bombs = []
explosions = []

def draw_bombs(screen):
    for bx, by, _ in bombs:
        rect = pygame.Rect(bx*TILE_SIZE, by*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, ORANGE, rect)

def draw_explosions(screen):
    for ex, ey, _ in explosions:
        rect = pygame.Rect(ex*TILE_SIZE, ey*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, rect)

def explode(x, y, maze):
    positions = [(x, y)]
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        for i in range(1, 3):
            nx, ny = x + dx*i, y + dy*i
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if maze[ny][nx] == 1:
                    break
                positions.append((nx, ny))
    return positions
