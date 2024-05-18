import sys
import pygame

def init():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mario Jumps")
    return screen

def load_assets():
    assets = {}
    error_messages = []
    try:
        assets["standing"] = pygame.transform.scale(pygame.image.load("assets/standing.png"), (52, 86))
    except pygame.error:
        error_messages.append("Error loading standing.png")
    try:
        assets["right_jump"] = pygame.transform.scale(pygame.image.load("assets/jumping_right.png"), (50, 58))
    except pygame.error:
        error_messages.append("Error loading jumping_right.png")
    try:
        assets["left_jump"] = pygame.transform.scale(pygame.image.load("assets/jumping_left.png"), (50, 58))
    except pygame.error:
        error_messages.append("Error loading jumping_left.png")
    try:
        assets["background"] = pygame.transform.scale(pygame.image.load("assets/bg.png"), (600, 600))
    except pygame.error:
        error_messages.append("Error loading bg.png")

    return assets, error_messages

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def handle_input(keys_pressed, state):
    if keys_pressed[pygame.K_SPACE] and not state["jumping"]:
        state["jumping"] = True
        state["jump_count"] += 1
        state["last_jump_time"] = pygame.time.get_ticks()
        state["y_velocity"] = state["min_jump_height"] + state["jump_count"] * 2
        if state["y_velocity"] > state["max_jump_height"]:
            state["y_velocity"] = state["max_jump_height"]
    if keys_pressed[pygame.K_LEFT]:
        state["x_position"] -= 5
        if state["jumping"]:
            state["jumping_surface"] = state["assets"].get("left_jump", state["jumping_surface"])
    if keys_pressed[pygame.K_RIGHT]:
        state["x_position"] += 5
        if state["jumping"]:
            state["jumping_surface"] = state["assets"].get("right_jump", state["jumping_surface"])
    if keys_pressed[pygame.K_DOWN]:
        state["x_position"] = state["x_initial"]
        state["y_position"] = state["y_initial"]
        state["y_velocity"] = state["min_jump_height"]
        state["jump_count"] = 0
    return state

def update_jump(state):
    if state["jumping"]:
        state["y_position"] -= state["y_velocity"]
        state["y_velocity"] -= state["y_gravity"]
        if state["y_velocity"] < -state["min_jump_height"] and state["y_position"] >= state["ground_level"] - state["jump"].height / 2.5:
            state["jumping"] = False
            state["y_velocity"] = state["min_jump_height"]
    else:
        state["jumping_surface"] = state["assets"].get("standing", state["jumping_surface"])
    return state

def check_collision(state):
    if state["y_position"] >= state["ground_level"]:
        state["y_position"] = state["ground_level"]
        state["jumping"] = False
        state["y_velocity"] = state["min_jump_height"]
    return state

def reset_jump_count(state):
    current_time = pygame.time.get_ticks()
    if current_time - state["last_jump_time"] > 1600:
        state["jump_count"] = 0
    return state

def render(screen, assets, state, error_messages):
    screen.blit(assets.get("background", pygame.Surface((600, 600))), (0, 0))
    text = state["font"].render(f"Jump Count: {state['jump_count']}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    state["jump"] = state["jumping_surface"].get_rect(center=(state["x_position"], state["y_position"]))
    screen.blit(state["jumping_surface"], state["jump"])
    if error_messages:
        error_text = state["font"].render(" | ".join(error_messages), True, (255, 0, 0))
        screen.blit(error_text, (50, 550))
    pygame.display.update()

def main():
    screen = init()
    assets, error_messages = load_assets()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    state = {
        "x_initial": 300,
        "y_initial": 480,
        "x_position": 300,
        "y_position": 480,
        "jumping": False,
        "y_gravity": 0.5,
        "min_jump_height": 7,
        "max_jump_height": 22,
        "y_velocity": 7,
        "ground_level": 480,
        "jump_count": 0,
        "last_jump_time": 0,
        "jumping_surface": assets.get("standing", pygame.Surface((52, 86))),  # Default to a blank surface if asset is missing
        "assets": assets,
        "font": font,
    }

    while True:
        handle_events()
        keys_pressed = pygame.key.get_pressed()
        state = handle_input(keys_pressed, state)
        state = update_jump(state)
        state = check_collision(state)
        state = reset_jump_count(state)
        render(screen, assets, state, error_messages)
        clock.tick(60)

if __name__ == "__main__":
    main()
