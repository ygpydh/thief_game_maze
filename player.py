import pygame
from config import TILE_SIZE, GREEN

player_pos = [1, 1]

def draw_player(screen):
    x, y = player_pos
    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, GREEN, rect)

def move_player(dx, dy, maze, COLS, ROWS):
    nx, ny = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] != 1:
        player_pos[0], player_pos[1] = nx, ny
