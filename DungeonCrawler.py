import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Colors
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)

# Tile size and dungeon dimensions
TILE_SIZE = 40
dungeon_width = WIDTH // TILE_SIZE
dungeon_height = HEIGHT // TILE_SIZE

# Player properties
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = TILE_SIZE
player_health = 100
player_attack_power = 10

# Enemy, item, power-up, and boss data
enemies = []
items = []
power_ups = []
boss_present = False
boss_pos = [0, 0]
boss_health = 200

# Game level
level = 1

def generate_dungeon():
    global level
    dungeon = [[random.choice([0, 1]) for _ in range(dungeon_width)] for _ in range(dungeon_height)]
    dungeon[dungeon_height // 2][dungeon_width // 2] = 0  # Ensure the player starts in an open space
    exit_pos = (random.randint(0, dungeon_height - 1), random.randint(0, dungeon_width - 1))
    dungeon[exit_pos[0]][exit_pos[1]] = 2  # Mark the exit
    
    # Increase difficulty with level
    num_enemies = 5 + level
    num_items = max(3 - level, 1)
    num_power_ups = 2
    
    # Generate enemies
    global enemies, items, power_ups, boss_present, boss_pos
    enemies = [(random.randint(0, dungeon_width - 1) * TILE_SIZE, random.randint(0, dungeon_height - 1) * TILE_SIZE) for _ in range(num_enemies)]
    
    # Generate items (health potions)
    items = [(random.randint(0, dungeon_width - 1) * TILE_SIZE, random.randint(0, dungeon_height - 1) * TILE_SIZE) for _ in range(num_items)]
    
    # Generate power-ups
    power_ups = [(random.randint(0, dungeon_width - 1) * TILE_SIZE, random.randint(0, dungeon_height - 1) * TILE_SIZE) for _ in range(num_power_ups)]
    
    # Generate boss
    if random.random() < 0.5:  # 50% chance for the boss to appear
        boss_present = True
        boss_pos = [random.randint(0, dungeon_width - 1) * TILE_SIZE, random.randint(0, dungeon_height - 1) * TILE_SIZE]
    else:
        boss_present = False

    return dungeon, exit_pos

# Initialize the first dungeon level
dungeon_map, exit_pos = generate_dungeon()

# Game loop
def main():
    global boss_health, player_attack_power, player_health, level
    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_over:
            # Handle game over screen input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Restart the game
                player_health = 100
                player_attack_power = 10
                level = 1
                dungeon_map, exit_pos = generate_dungeon()
                player_pos[0], player_pos[1] = WIDTH // 2, HEIGHT // 2
                boss_health = 200
                game_over = False

        else:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - TILE_SIZE:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - TILE_SIZE:
                player_pos[1] += player_speed

            # Check if player reaches the exit
            player_tile = (player_pos[1] // TILE_SIZE, player_pos[0] // TILE_SIZE)
            if player_tile == exit_pos:
                level += 1
                dungeon_map, exit_pos = generate_dungeon()
                player_pos[0], player_pos[1] = WIDTH // 2, HEIGHT // 2
                boss_health = 200  # Reset boss health

            # Check for collisions with enemies
            for enemy in enemies:
                if player_pos[0] == enemy[0] and player_pos[1] == enemy[1]]:
                    player_health -= 10  # Player takes damage from the enemy
                    enemies.remove(enemy)  # Remove the enemy after collision
                    if player_health <= 0:
                        game_over = True

            # Check for item collection (health potions)
            for item in items:
                if player_pos[0] == item[0] and player_pos[1] == item[1]]:
                    player_health = min(player_health + 20, 100)  # Increase player's health, max 100
                    items.remove(item)  # Remove the item after collection

            # Check for power-up collection
            for power_up in power_ups:
                if player_pos[0] == power_up[0] and player_pos[1] == power_up[1]]:
                    player_attack_power += 10  # Increase player's attack power
                    power_ups.remove(power_up)  # Remove the power-up after collection

            # Check for boss battle
            if boss_present and player_pos[0] == boss_pos[0] and player_pos[1] == boss_pos[1]]:
                boss_health -= player_attack_power  # Player attacks the boss
                if boss_health <= 0:
                    boss_present = False  # Boss defeated

            # Drawing the dungeon
            window.fill(BLACK)
            for row in range(dungeon_height):
                for col in range(dungeon_width):
                    if dungeon_map[row][col] == 1:
                        pygame.draw.rect(window, GRAY, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    elif dungeon_map[row][col] == 2:
                        pygame.draw.rect(window, GREEN, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            # Draw enemies
            for enemy in enemies:
                pygame.draw.rect(window, YELLOW, (*enemy, TILE_SIZE, TILE_SIZE))

            # Draw items (health potions)
            for item in items:
                pygame.draw.rect(window, BLUE, (*item, TILE_SIZE, TILE_SIZE))

            # Draw power-ups
            for power_up in power_ups:
                pygame.draw.rect(window, PURPLE, (*power_up, TILE_SIZE, TILE_SIZE))

            # Draw boss
            if boss_present:
                pygame.draw.rect(window, WHITE, (*boss_pos, TILE_SIZE, TILE_SIZE))

            # Draw the player
            pygame.draw.rect(window, RED, (*player_pos, TILE_SIZE, TILE_SIZE))

            # Display player's health, attack power, and level
            font = pygame.font.Font(None, 36)
            health_text = font.render(f"Health: {player_health}", True, WHITE)
            attack_text = font.render(f"Attack: {player_attack_power}", True, WHITE)
            level_text = font.render(f"Level: {level}", True, WHITE)
            window.blit(health_text, (10, 10))
            window.blit(attack_text, (10, 50))
            window.blit(level_text, (10, 90))

            # Update the display
            pygame.display.flip()
            clock.tick(60)

        else:
            # Game over screen
            window.fill(BLACK)
            font = pygame.font.Font(None, 74)
            game_over_text = font.render("Game Over", True, RED)
            window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press 'R' to Restart", True, WHITE)
            window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()