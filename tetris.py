import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_X = (WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, WHITE, 
                           (GRID_X + x * BLOCK_SIZE, GRID_Y + y * BLOCK_SIZE, 
                            BLOCK_SIZE - 1, BLOCK_SIZE - 1), 1)

def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, tetromino.color,
                               (GRID_X + (tetromino.x + x) * BLOCK_SIZE,
                                GRID_Y + (tetromino.y + y) * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))

def check_collision(tetromino, grid, dx=0, dy=0):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetromino.x + x + dx
                new_y = tetromino.y + y + dy
                if (new_x < 0 or new_x >= GRID_WIDTH or 
                    new_y >= GRID_HEIGHT or 
                    (new_y >= 0 and grid[new_y][new_x])):
                    return True
    return False

def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines(grid):
    lines_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [None] * GRID_WIDTH)
            lines_cleared += 1
    return lines_cleared

def main():
    grid = [[None] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_piece = Tetromino()
    fall_time = 0
    fall_speed = 50  # Lower is faster
    score = 0
    game_over = False

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        fall_time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(current_piece, grid, dx=-1):
                    current_piece.x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(current_piece, grid, dx=1):
                    current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    fall_speed = 5  # Speed up when holding down
                if event.key == pygame.K_UP:
                    original_shape = current_piece.shape
                    current_piece.rotate()
                    if check_collision(current_piece, grid):
                        current_piece.shape = original_shape

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            fall_speed = 50  # Reset speed

        if fall_time >= fall_speed:
            fall_time = 0
            if not check_collision(current_piece, grid, dy=1):
                current_piece.y += 1
            else:
                merge_tetromino(current_piece, grid)
                score += clear_lines(grid) * 100
                current_piece = Tetromino()
                if check_collision(current_piece, grid):
                    game_over = True

        screen.fill(BLACK)
        draw_grid()
        
        # Draw landed pieces
        for y, row in enumerate(grid):
            for x, color in enumerate(row):
                if color:
                    pygame.draw.rect(screen, color,
                                   (GRID_X + x * BLOCK_SIZE,
                                    GRID_Y + y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))
        
        draw_tetromino(current_piece)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - 70, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()