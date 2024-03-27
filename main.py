import pygame

# GLOBAL VARIABLES
SCREEN_SIZE = (1024, 768)
WIDTH, HEIGHT = SCREEN_SIZE
SNAKE_SPEED = 5


def main():
    # Initialize Pygame
    pygame.init()
    # Set the screen size, window title and game clock
    pygame.display.set_caption("Snake Game")
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    # Sample rectangle player
    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 50, 50)
    velocity = pygame.Vector2(SNAKE_SPEED, 0)
    
    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # KEYBOARD EVENTS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    velocity = pygame.Vector2(-SNAKE_SPEED, 0)
                if event.key == pygame.K_d:
                    velocity = pygame.Vector2(SNAKE_SPEED, 0)
                if event.key == pygame.K_w:
                    velocity = pygame.Vector2(0, -SNAKE_SPEED)
                if event.key == pygame.K_s:
                    velocity = pygame.Vector2(0, SNAKE_SPEED)

        # Update the player position
        player.move_ip(velocity.x, velocity.y)

        # Check if the player has collided with the screen boundaries
        if player.clamp(screen.get_rect()) != player:
            velocity = pygame.Vector2(0, 0)

        # Clear the screen
        screen.fill("black")

        # Draw a rectangle
        pygame.draw.rect(screen, "red", player)

        # Update the screen
        pygame.display.flip()

        # Limit FPS to 60
        clock.tick(60)

    # Quit Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
