import pygame

# Intialize the Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))


# Tile and icon
pygame.display.set_caption("Revenge of Chicken")
icon = pygame.image.load('chicken.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('me.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x,y):
    screen.blit(playerImg, (x, y))

# Game Loop
running = True
while running:

    screen.fill((153, 221, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keystoke
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -0.9
        if event.key == pygame.K_RIGHT:
            playerX_change = 0.9
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
    playerX += playerX_change
    player(playerX, playerY)
    pygame.display.update()