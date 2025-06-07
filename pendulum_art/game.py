import pygame
import sys
import numpy as np
from pendulum_art.physics import DoublePendulum


def main():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Pendulum Art")
    clock = pygame.time.Clock()

    # Create pendulum instance (to be implemented in physics.py)
    pendulum = DoublePendulum(l1=1.0, l2=0.5)

    # Initial state: [theta1, theta2, omega1, omega2]
    state = np.array([np.pi / 4, np.pi / 2, 0.0, 0.0])

    # Canvas surface for persistent painting
    canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    # Painting controls
    spraying = False
    current_color = (255, 0, 0)
    brush_size = 5

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # delta time in seconds

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spraying = True
                # TODO: map keys 1-5 to change current_color
                if event.key == pygame.K_1:
                    current_color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    current_color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    current_color = (0, 0, 255)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    spraying = False

        # Physics update (placeholder; replace with RK4 from physics.py)
        # state = pendulum.rk4_step(state, dt)

        # Render background and existing canvas
        screen.fill((30, 30, 30))
        screen.blit(canvas, (0, 0))

        # Painting logic
        if spraying:
            # Placeholder: draw at center. Replace with pendulum tip coords
            x, y = 400, 400
            pygame.draw.circle(canvas, current_color, (x, y), brush_size)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

    main()