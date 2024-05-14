import sys
import pygame
# need to install pygame:-  pip install pygame

pygame.init()
CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mario Jumps")

X_initial = 200
Y_initial = 450
X_POSITION, Y_POSITION = X_initial, Y_initial
jumping = False
Y_GRAVITY = 0.5
JUMP_HEIGHT = 20
Y_VELOCITY = JUMP_HEIGHT

standing = pygame.transform.scale(pygame.image.load("assets/standing.png"), (52, 86))
right_jump = pygame.transform.scale(pygame.image.load("assets/jumping_right.png"), (50, 58))
left_jump = pygame.transform.scale(pygame.image.load("assets/jumping_left.png"), (50, 58))
jumping_surface = right_jump
BACKGROUND = pygame.transform.scale(pygame.image.load("assets/bg.png"), (600, 600))

jump = standing.get_rect(center=(X_POSITION, Y_POSITION))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_SPACE]:
        jumping = True
    if keys_pressed[pygame.K_LEFT]:
        X_POSITION -= 5
        jumping_surface = left_jump
    if keys_pressed[pygame.K_RIGHT]:
        X_POSITION += 5
        jumping_surface = right_jump
    if keys_pressed[pygame.K_DOWN]:
        X_POSITION = X_initial
        Y_POSITION = Y_initial
    SCREEN.blit(BACKGROUND, (0, 0))

    if jumping:
        Y_POSITION -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < - JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
            Y_GRAVITY = 0.5
        jump = jumping_surface.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(jumping_surface, jump)
    else:
        jumping_surface = standing
        jump = jumping_surface.get_rect(center=(X_POSITION, Y_POSITION))
        SCREEN.blit(jumping_surface, jump)

    pygame.display.update()
    CLOCK.tick(60)
