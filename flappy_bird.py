# Imports
import pygame
import random

# Intializing Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_SPEED = 5
PIPE_GAP = 150

# Loading assets
BIRD_IMG = pygame.Surface((30, 30))
BIRD_IMG.fill(GREEN)

# Creating a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(BIRD_IMG, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, 50, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, 50, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def off_screen(self):
        return self.x < -50

    def collide(self, bird):
        if bird.y < self.height or bird.y > self.height + PIPE_GAP:
            if self.x < bird.x < self.x + 50:
                return True
        return False

# Main game loop
def game_loop():
    bird = Bird()
    pipes = [Pipe()]
    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Bird updates
        bird.update()
        bird.draw()

        # Pipe updates
        if pipes[-1].x < SCREEN_WIDTH // 2:
            pipes.append(Pipe())

        for pipe in pipes:
            pipe.update()
            pipe.draw()

            if pipe.collide(bird):
                running = False

            if pipe.x < bird.x and not pipe.passed:
                pipe.passed = True
                score += 1

        # Removing off-screen pipes
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Checking if bird is out of screen
        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False

        # Updating display
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
game_loop()