import sys
import pygame

try:
    pygame.init()
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mario Jumps")

    X_initial = 290
    Y_initial = 450
    X_POSITION, Y_POSITION = X_initial, Y_initial
    jumping = False
    Y_GRAVITY = 0.5
    MIN_JUMP_HEIGHT = 7
    MAX_JUMP_HEIGHT = 22  # Maximum jump height
    Y_VELOCITY = MIN_JUMP_HEIGHT
    MAX_JUMP_DURATION = 2000  # Maximum duration of continuous jumping (in milliseconds)
    jump_count = 0  # Number of consecutive jumps
    last_jump_time = 0  # Time of the last jump

    standing = pygame.transform.scale(pygame.image.load("assets/standing.png"), (52, 86))
    right_jump = pygame.transform.scale(pygame.image.load("assets/jumping_right.png"), (50, 58))
    left_jump = pygame.transform.scale(pygame.image.load("assets/jumping_left.png"), (50, 58))
    jumping_surface = right_jump
    BACKGROUND = pygame.transform.scale(pygame.image.load("assets/bg.png"), (600, 600))

    # Define ground level
    GROUND_LEVEL = 498

    jump = standing.get_rect(center=(X_POSITION, Y_POSITION))

    font = pygame.font.Font(None, 36)  # Choose font and size for the text

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and not jumping:
            jumping = True
            jump_count += 1
            last_jump_time = pygame.time.get_ticks()
            # Adjust jump height based on jump count
            Y_VELOCITY = MIN_JUMP_HEIGHT + jump_count * 2
            if Y_VELOCITY > MAX_JUMP_HEIGHT:
                Y_VELOCITY = MAX_JUMP_HEIGHT

        if keys_pressed[pygame.K_LEFT]:
            X_POSITION -= 5
            jumping_surface = left_jump
        if keys_pressed[pygame.K_RIGHT]:
            X_POSITION += 5
            jumping_surface = right_jump
        if keys_pressed[pygame.K_DOWN]:
            X_POSITION = X_initial
            # Y_POSITION = Y_initial  # Remove this line to keep Mario at the landing position
            jumping = False
            Y_VELOCITY = MIN_JUMP_HEIGHT
            jump_count = 0

        SCREEN.blit(BACKGROUND, (0, 0))

        if jumping:
            Y_POSITION -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY

            if Y_VELOCITY < -MIN_JUMP_HEIGHT and Y_POSITION >= GROUND_LEVEL - jump.height / 2.5:
                jumping = False
                Y_VELOCITY = MIN_JUMP_HEIGHT

            jump = jumping_surface.get_rect(center=(X_POSITION, Y_POSITION))
        else:
            jumping_surface = standing
            # X_POSITION = X_initial  # Remove this line to keep Mario at the landing position
            # Y_POSITION = Y_initial  # Remove this line to keep Mario at the landing position
            jump = jumping_surface.get_rect(center=(X_POSITION, Y_POSITION))

        # Check collision with ground
        if jump.bottom >= GROUND_LEVEL:
            Y_POSITION = GROUND_LEVEL - jump.height / 2.5
            jumping = False
            Y_VELOCITY = MIN_JUMP_HEIGHT

        # Reset jump count after 1 second of last jump
        current_time = pygame.time.get_ticks()
        if current_time - last_jump_time > 1700:
            jump_count = 0

        # Render jump count text
        text = font.render(f"Jump Count: {jump_count}", True, (255, 255, 255))
        SCREEN.blit(text, (10, 10))  # Position the text on the screen

        SCREEN.blit(jumping_surface, jump)
        pygame.display.update()
        CLOCK.tick(60)

except Exception as e:
    print("An error occurred:", e)
    pygame.quit()
    sys.exit()
