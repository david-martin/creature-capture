import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple RPG Game")

# Tile size
TILE_SIZE = 32

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)  # Grass color
BROWN = (139, 69, 19)  # Tree or obstacle color

def battle(player, enemy):
    # Battle loop
    print(f"A wild Level {enemy.level} enemy appears!")

    # Create a simple battle screen
    battle_running = True
    font = pygame.font.SysFont(None, 24)

    while battle_running:
        # Determine turn order based on speed_stat
        if player.speed_stat >= enemy.speed_stat:
            turn_order = ['player', 'enemy']
        else:
            turn_order = ['enemy', 'player']

        for turn in turn_order:
            if turn == 'player':
                # Player's turn
                action_selected = None
                while action_selected not in ('attack', 'defend'):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a:
                                action_selected = 'attack'
                            elif event.key == pygame.K_d:
                                action_selected = 'defend'

                    # Display battle options
                    screen.fill((0, 0, 0))
                    battle_text = font.render("Battle! Press 'A' to Attack or 'D' to Defend", True, (255, 255, 255))
                    player_hp_text = font.render(f"Your HP: {player.current_hp}/{player.max_hp}", True, (255, 255, 255))
                    enemy_hp_text = font.render(f"Enemy HP: {enemy.current_hp}/{enemy.max_hp}", True, (255, 255, 255))
                    screen.blit(battle_text, (50, 50))
                    screen.blit(player_hp_text, (50, 80))
                    screen.blit(enemy_hp_text, (50, 110))
                    pygame.display.flip()

                if action_selected == 'attack':
                    damage = max(0, player.attack - enemy.defense)
                    enemy.current_hp -= damage
                    print(f"You attack the enemy for {damage} damage!")
                elif action_selected == 'defend':
                    player.defense *= 2
                    print("You brace yourself to defend!")
            else:
                # Enemy's turn
                damage = max(0, enemy.attack - player.defense)
                player.current_hp -= damage
                print(f"The enemy attacks you for {damage} damage!")

            # Check for end of battle
            if enemy.current_hp <= 0:
                print("You defeated the enemy!")
                player.gain_exp(enemy.exp_reward)
                enemy.kill()  # Remove enemy from the game
                battle_running = False
                if enemy.type == 'B':
                    print("Congratulations! You have defeated the main boss and completed the game!")
                    pygame.quit()
                    sys.exit()
                break
            if player.current_hp <= 0:
                print("You have been defeated!")
                pygame.quit()
                sys.exit()

            # Reset defense if player defended
            if turn == 'player' and action_selected == 'defend':
                player.defense //= 2

        # Small delay to make the battle flow visible
        pygame.time.delay(500)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((255, 255, 255))  # White color
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
        self.speed = 4  # Movement speed
        # Player stats
        self.level = 1
        self.max_hp = 100
        self.current_hp = self.max_hp
        self.attack = 10
        self.defense = 5
        self.speed_stat = 5
        self.exp = 0
        self.exp_to_next_level = 100

    def handle_keys(self, obstacles, enemies):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Move and check for collisions
        self.rect.x += dx
        self.check_collisions(dx, 0, obstacles, enemies)
        self.rect.y += dy
        self.check_collisions(0, dy, obstacles, enemies)

    def check_collisions(self, dx, dy, obstacles, enemies):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dx > 0:
                    self.rect.right = obstacle.rect.left
                if dx < 0:
                    self.rect.left = obstacle.rect.right
                if dy > 0:
                    self.rect.bottom = obstacle.rect.top
                if dy < 0:
                    self.rect.top = obstacle.rect.bottom
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                battle(self, enemy)

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level += 100  # Increase EXP required for next level
        # Increase stats
        self.max_hp += 20
        self.current_hp = self.max_hp
        self.attack += 5
        self.defense += 2
        self.speed_stat += 1
        print(f"You leveled up to Level {self.level}!")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        if enemy_type == 'E':
            self.image.fill((255, 0, 0))  # Red for enemies
            self.level = 1
            self.max_hp = 50
            self.current_hp = self.max_hp
            self.attack = 8
            self.defense = 3
            self.speed_stat = 4
            self.exp_reward = 100
        elif enemy_type == 'B':
            self.image.fill((0, 0, 255))  # Blue for boss
            self.level = 3
            self.max_hp = 150
            self.current_hp = self.max_hp
            self.attack = 15
            self.defense = 8
            self.speed_stat = 6
            self.exp_reward = 0  # No EXP as game ends after boss
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
        self.type = enemy_type

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_type):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if tile_type == 'W':
            self.image.fill((139, 69, 19))  # Brown color for walls
        elif tile_type == 'T':
            self.image.fill((34, 139, 34))  # Dark green for trees
        elif tile_type == '.':
            self.image.fill((34, 177, 76))  # Grass color
        elif tile_type == 'E':
            self.image.fill((255, 0, 0))  # Red for enemies
        elif tile_type == 'B':
            self.image.fill((0, 0, 255))  # Blue for boss
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = tile_type  # Store the tile type for collision detection

def load_map(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    game_map = []
    for line in data:
        game_map.append(list(line.strip()))
    return game_map

def create_map(game_map):
    tile_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    y = 0
    for row in game_map:
        x = 0
        for tile_type in row:
            if tile_type in ('W', 'T', '.'):
                tile = Tile(x, y, tile_type)
                tile_group.add(tile)
            elif tile_type in ('E', 'B'):
                # Create enemy
                enemy = Enemy(x, y, tile_type)
                enemy_group.add(enemy)
                # Add ground tile beneath enemy
                tile = Tile(x, y, '.')
                tile_group.add(tile)
            x += TILE_SIZE
        y += TILE_SIZE
    return tile_group, enemy_group


def main():
    clock = pygame.time.Clock()
    game_map = load_map('map.txt')
    tile_group, enemy_group = create_map(game_map)

    # Find player's starting position (first '.' on the map)
    for y, row in enumerate(game_map):
        for x, tile_type in enumerate(row):
            if tile_type == '.':
                start_x = x * TILE_SIZE
                start_y = y * TILE_SIZE
                break
        else:
            continue
        break

    player = Player(start_x, start_y)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy_group)

    # Identify obstacles for collision detection
    obstacles = [tile for tile in tile_group if tile.type in ('W', 'T')]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player input
        player.handle_keys(obstacles, enemy_group)

        # Fill the screen with black before drawing
        screen.fill((0, 0, 0))

        # Draw map tiles
        tile_group.draw(screen)

        # Draw all sprites
        all_sprites.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

