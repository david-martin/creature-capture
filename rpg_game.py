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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((255, 255, 255))  # White color
        self.rect = self.image.get_rect()
        self.rect.center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
        self.speed = 4

    def handle_keys(self, obstacles):
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
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = obstacle.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = obstacle.rect.right

        self.rect.y += dy
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = obstacle.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = obstacle.rect.bottom

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
    y = 0
    for row in game_map:
        x = 0
        for tile_type in row:
            tile = Tile(x, y, tile_type)
            tile_group.add(tile)
            x += TILE_SIZE
        y += TILE_SIZE
    return tile_group

def main():
    clock = pygame.time.Clock()
    game_map = load_map('map.txt')
    tile_group = create_map(game_map)

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

    # Identify obstacles for collision detection
    obstacles = [tile for tile in tile_group if tile.type in ('W', 'T')]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player input
        player.handle_keys(obstacles)

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

