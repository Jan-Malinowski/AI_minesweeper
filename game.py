import pygame
import random
import time
from ai_basic import MinesweeperAI

# Constants
WIDTH, HEIGHT = 500, 500
ROWS, COLS = 8, 8
MINE_COUNT = 10
CELL_SIZE = WIDTH // COLS
WHITE, GRAY, BLACK, RED, GREEN = (255,255,255), (200,200,200), (0,0,0), (255,0,0), (0,255,0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper AI")
font = pygame.font.Font(None, 36)

# Create grid function
def create_grid():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    mines = random.sample(range(ROWS * COLS), MINE_COUNT)
    for mine in mines:
        row, col = divmod(mine, COLS)
        grid[row][col] = -1  
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == -1:
                continue
            grid[row][col] = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1] 
                                 if 0 <= row+dr < ROWS and 0 <= col+dc < COLS and grid[row+dr][col+dc] == -1)
    return grid

# Draw grid
def draw_grid(grid, revealed, game_over, lastrow, lastcol):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # Show mines in red if game over
            if game_over and grid[row][col] == -1:
                if lastrow==row and lastcol==col:
                    pygame.draw.rect(screen, BLACK, rect)
                else:
                    pygame.draw.rect(screen, RED, rect)
            elif revealed[row][col]:
                pygame.draw.rect(screen, WHITE, rect)
                if grid[row][col] > 0:
                    text = font.render(str(grid[row][col]), True, BLACK)
                    screen.blit(text, (col * CELL_SIZE + 15, row * CELL_SIZE + 10))
            else:
                pygame.draw.rect(screen, GRAY, rect)
            
            pygame.draw.rect(screen, BLACK, rect, 1)

# Reveal function
def reveal_tile(grid, revealed, row, col):
    """Reveal the tile and its adjacent tiles if it's a '0'."""
    if revealed[row][col]:
        return "playing"
    
    if grid[row][col] == -1:
        return "game_over"
    
    # Reveal the current cell
    revealed[row][col] = True

    # If the cell is '0', reveal all adjacent cells recursively
    if grid[row][col] == 0:
        # Iterate over all adjacent cells (8 directions)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = row + dr, col + dc
                # Ensure the adjacent cell is within bounds
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    if not revealed[new_row][new_col]:  # If not already revealed
                        reveal_tile(grid, revealed, new_row, new_col)

    return "win" if all(revealed[r][c] or grid[r][c] == -1 for r in range(ROWS) for c in range(COLS)) else "playing"


# Reset function
def reset_game():
    return create_grid(), [[False]*COLS for _ in range(ROWS)], False, False

# Initialize game
grid, revealed, game_over, game_won = reset_game()
ai = MinesweeperAI(ROWS, COLS)
ai.load_model()
running = True
lose_time = None  # Track when the loss happened
game_number=1
nr_moves=0
move = [0, 0]

while running:
    screen.fill(BLACK)
    draw_grid(grid, revealed, game_over, *move)
    

    if game_over:
        nr_moves=0
        grid, revealed, game_over, game_won = reset_game()

    
    # if game_over:
    #     text = font.render("GAME OVER!", True, GREEN)
    #     screen.blit(text, (WIDTH // 3, HEIGHT // 2))
    #     if lose_time is None:  # Start 5s countdown
    #         lose_time = time.time()
    #     elif time.time() - lose_time > 1:  # Restart after 1s
    #         grid, revealed, game_over, game_won = reset_game()
    #         nr_moves=0
    #         lose_time = None

    pygame.display.flip()

    if not game_over and not game_won:
        #time.sleep(0.3)  
        prev_revealed = [row[:] for row in revealed]  
        move = ai.choose_move(revealed)  
        if move:
            result = reveal_tile(grid, revealed, *move)
            if(result=="game_over"):
                if nr_moves==0:
                    reward=1;
                else:
                    reward=nr_moves*-2
            elif(result=="playing"):
                reward=nr_moves*2
            else:
                reward=500
            ai.update(prev_revealed, move, reward, revealed)
            nr_moves+=1
            if result == "game_over":
                game_over = True
                print(game_number, nr_moves)
                game_number+=1
            elif result == "win":
                game_won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            grid, revealed, game_over, game_won = reset_game()
            lose_time = None
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            running = False

ai.save_model()
print("Model saved") 
pygame.quit()
