import pygame
from config import maze, ROWS, COLS, TILE_SIZE, GRAY, YELLOW, BLUE

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
