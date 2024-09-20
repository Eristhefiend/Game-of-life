import pygame
import random
import sys

pygame.init()
Width, Height = 800, 800
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game of Life")
black = (0, 0, 0)
white = (255, 255, 255)
clock = pygame.time.Clock()
fps = 10
rows, cols = 50, 50
cell_size = Width // cols

def create_grid(randomize=False):
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            if randomize:
                grid[row].append(random.choice([0, 1]))
            else:
                grid[row].append(0)
    return grid

grid = create_grid(randomize=True)

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            x, y = col * cell_size, row * cell_size
            if grid[row][col] == 1:
                pygame.draw.rect(Screen, white, (x, y, cell_size, cell_size))
            else:
                pygame.draw.rect(Screen, black, (x, y, cell_size, cell_size))
def count_live_neighbours(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if row + i < 0 or row + i >= rows or col + j < 0 or col + j >= cols:
                continue
            count += grid[row + i][col + j]
    return count
def next_generation(grid):
    next_gen = create_grid()
    for row in range(rows):
        for col in range(cols):
            live_neighbours = count_live_neighbours(grid, row, col)
            if grid[row][col] == 1:
                if live_neighbours < 2 or live_neighbours > 3:
                    next_gen[row][col] = 0
                else:
                    next_gen[row][col] = 1
            else:
                if live_neighbours == 3:
                    next_gen[row][col] = 1
    return next_gen
def toggle_cell(grid, pos):
    x, y = pos
    row = y // cell_size
    col = x // cell_size
    if grid[row][col] == 1:
        grid[row][col] = 0
    else: grid[row][col] = 1
running = True
paused = False

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                grid = create_grid(randomize=True)
            elif event.key == pygame.K_c:
                grid = create_grid()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not paused:
                pos = pygame.mouse.get_pos()
                toggle_cell(grid, pos)

    if not paused:
        grid = next_generation(grid)
    Screen.fill(black)
    draw_grid()
    pygame.display.flip()

pygame.quit()
sys.exit()