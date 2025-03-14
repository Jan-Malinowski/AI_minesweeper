import pygame
import random
from collections import deque

WIDTH, HEIGHT = 720, 720
ROWS, COLS = 16, 16
MINE_COUNT = 20
CELL_SIZE = WIDTH//COLS

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FLAG_COLOR = RED

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True

def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Place mines
    mines = random.sample(range(ROWS * COLS), MINE_COUNT)
    for mine in mines:
        row, col = divmod(mine, COLS)
        grid[row][col] = -1  # Mine
    
    # Calculate numbers
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == -1:
                continue  # Skip mines
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    r, c = row + dr, col + dc
                    if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c] == -1:
                        count += 1
            grid[row][col] = count
    
    return grid

def draw_grid(grid, revealed, flags, game_over, game_won):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if revealed[row][col]:  # Revealed tiles
                if grid[row][col] == -1:  
                    pygame.draw.rect(screen, RED, rect)  # Mine
                else:
                    pygame.draw.rect(screen, WHITE, rect)  
                    if grid[row][col] > 0:
                        text = font.render(str(grid[row][col]), True, BLACK)
                        screen.blit(text, (col * CELL_SIZE + 15, row * CELL_SIZE + 10))
            elif flags[row][col]:  # Flagged tiles
                pygame.draw.rect(screen, FLAG_COLOR, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)  # Hidden tiles
            
            pygame.draw.rect(screen, BLACK, rect, 1)  # Border

    # Display game messages
    if game_over:
        text = font.render("Game Over! Press R to restart", True, RED)
        screen.blit(text, (50, HEIGHT // 2))
    elif game_won:
        text = font.render("You Win! Press R to restart", True, GREEN)
        screen.blit(text, (80, HEIGHT // 2))

# Flood fill to reveal empty spaces
def flood_fill(grid, revealed, row, col):
    queue = deque([(row, col)])
    
    while queue:
        r, c = queue.popleft()
        if revealed[r][c]: 
            continue
        
        revealed[r][c] = True

        if grid[r][c] == 0:  
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and not revealed[nr][nc]:
                        queue.append((nr, nc))

# Check if the player won
def check_win(grid, revealed):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != -1 and not revealed[row][col]:  # If there's an unrevealed non-mine tile
                return False
    return True  # All non-mine tiles are revealed

# Reset game
def reset_game():
    global grid, revealed, flags, game_over, game_won
    grid = create_grid()
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
    game_over = False
    game_won = False

# Reveal a tile when clicked
def reveal_tile(grid, revealed, flags, row, col):
    global game_over, game_won
    if revealed[row][col] or flags[row][col]:  
        return

    if grid[row][col] == -1:  # Mine clicked → Game over
        game_over = True
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == -1:
                    revealed[r][c] = True  # Reveal all mines
    else:
        flood_fill(grid, revealed, row, col)  

    if check_win(grid, revealed):  
        game_won = True

# Main game loop
grid = create_grid()
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flags = [[False for _ in range(COLS)] for _ in range(ROWS)]
game_over = False
game_won = False

while running:
    screen.fill((0, 0, 0))  
    draw_grid(grid, revealed, flags, game_over, game_won)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col, row = x // CELL_SIZE, y // CELL_SIZE  

            if event.button == 1 and not game_over and not game_won:  # Left click
                reveal_tile(grid, revealed, flags, row, col)
            elif event.button == 3 and not game_over and not game_won:  # Right click (Flag)
                if not revealed[row][col]:  
                    flags[row][col] = not flags[row][col]  

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press R to restart
                reset_game()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
