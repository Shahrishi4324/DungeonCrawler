import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Crawler: The Lost Temple")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)

# Define player settings
player_size = 40
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Define the dungeon grid
tile_size = 40
dungeon_rows, dungeon_cols = HEIGHT // tile_size, WIDTH // tile_size
dungeon = [[0 for _ in range(dungeon_cols)] for _ in range(dungeon_rows)]

# Generate a simple dungeon
def generate_dungeon():
    for row in range(dungeon_rows):
        for col in range(dungeon_cols):
            if random.choice([True, False]):
                dungeon[row][col] = 1  # Wall
            else:
                dungeon[row][col] = 0  # Floor

# Game loop
def main():
    clock = pygame.time.Clock()
    generate_dungeon()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
            player_pos[1] += player_speed

        # Fill the background
        window.fill(DARK_GRAY)

        # Draw the dungeon grid
        for row in range(dungeon_rows):
            for col in range(dungeon_cols):
                color = LIGHT_GRAY if dungeon[row][col] == 1 else BLACK
                pygame.draw.rect(window, color, (col * tile_size, row * tile_size, tile_size, tile_size))

        # Draw the player
        pygame.draw.rect(window, WHITE, (*player_pos, player_size, player_size))

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()