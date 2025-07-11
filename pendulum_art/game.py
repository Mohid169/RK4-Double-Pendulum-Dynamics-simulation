import pygame
import sys
import numpy as np
from pendulum_art.physics import DoublePendulum
from pendulum_art.renderer import draw_pendulum, to_screen
from pendulum_art.utils import save_preset, load_preset, DEFAULT_PALETTE
import os
import time


class PendulumArtGame:
    def __init__(self, width=1000, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Double Pendulum Art")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Create pendulum instance
        self.pendulum = DoublePendulum(l1=1.0, l2=0.5)

        # Initial state: [theta1, theta2, omega1, omega2]
        # Use the original simulation.py initial state that produces chaotic behavior
        self.initial_state = np.array(
            [-np.pi / 3, -5 * np.pi / 6, 0.0, 0.0]
        )  # Original chaotic state
        self.state = self.initial_state.copy()

        # Visual settings
        self.scale = 200  # pixels per meter
        self.show_pendulum = True
        self.show_help = False
        self.paused = False
        self.painting = False

        # Interactive setup mode
        self.setup_mode = False
        self.dragging_bob = None  # None, 1, or 2 for which bob is being dragged
        self.mouse_pos = (0, 0)

        # Trail and canvas
        self.trail_points = []
        self.trail_length = 500
        self.canvas = pygame.Surface((width, height), pygame.SRCALPHA)

        # Color and brush settings
        self.current_color = (255, 255, 255)  # White
        self.brush_size = 3
        self.palette = {
            "1": (255, 100, 100),  # Red
            "2": (100, 255, 100),  # Green
            "3": (100, 100, 255),  # Blue
            "4": (255, 255, 100),  # Yellow
            "5": (255, 100, 255),  # Magenta
            "6": (100, 255, 255),  # Cyan
            "7": (255, 165, 0),  # Orange
            "8": (160, 100, 255),  # Purple
            "9": (255, 255, 255),  # White
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.painting = True
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_c:
                    self.clear_canvas()
                elif event.key == pygame.K_v:
                    self.show_pendulum = not self.show_pendulum
                elif event.key == pygame.K_s:
                    self.save_artwork()
                elif event.key == pygame.K_l:
                    self.load_preset_dialog()
                elif event.key == pygame.K_i:
                    self.setup_mode = not self.setup_mode
                    if self.setup_mode:
                        self.paused = True  # Pause simulation during setup
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    key_str = str(event.key - pygame.K_0)
                    if key_str in self.palette:
                        self.current_color = self.palette[key_str]
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.brush_size = min(10, self.brush_size + 1)
                elif event.key == pygame.K_MINUS:
                    self.brush_size = max(1, self.brush_size - 1)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.painting = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.setup_mode:  # Left click in setup mode
                    self.start_dragging(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if (
                    event.button == 1 and self.setup_mode
                ):  # Left click release in setup mode
                    self.stop_dragging()

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                if self.setup_mode and self.dragging_bob is not None:
                    self.update_pendulum_from_mouse(event.pos)

        return True

    def update_physics(self, dt):
        if not self.paused:
            # Update pendulum state using RK4
            self.state = self.pendulum.rk4_step(self.state, dt)

            # Get pendulum tip position
            (x1, y1), (x2, y2) = self.pendulum.tip_positions(self.state)

            # Convert to screen coordinates
            origin = (self.width // 2, self.height // 2)
            tip_screen = to_screen(
                (x2, y2), (self.width, self.height), self.scale, offset=origin
            )

            # Add to trail
            self.trail_points.append(tip_screen)
            if len(self.trail_points) > self.trail_length:
                self.trail_points.pop(0)

            # Paint if space is held
            if (
                self.painting
                and 0 <= tip_screen[0] < self.width
                and 0 <= tip_screen[1] < self.height
            ):
                pygame.draw.circle(
                    self.canvas, self.current_color, tip_screen, self.brush_size
                )

    def render(self):
        # Clear screen with dark background
        self.screen.fill((20, 20, 30))

        # Draw persistent canvas (artwork)
        self.screen.blit(self.canvas, (0, 0))

        # Draw pendulum if visible
        if self.show_pendulum:
            draw_pendulum(
                self.screen,
                self.state,
                self.pendulum,
                (self.width, self.height),
                scale=self.scale,
                rod_color=(150, 150, 150),
                bob_color=(255, 255, 255),
                rod_width=2,
                bob_radius=6,
            )

            # In setup mode, highlight bobs that can be dragged
            if self.setup_mode:
                self.draw_setup_feedback()

            # Draw trail
            if len(self.trail_points) > 1:
                for i in range(1, len(self.trail_points)):
                    alpha = int(255 * (i / len(self.trail_points)))
                    color = (*self.current_color, alpha)
                    if i > 0:
                        # Create a surface for alpha blending
                        trail_surf = pygame.Surface((3, 3), pygame.SRCALPHA)
                        trail_surf.fill(color)
                        self.screen.blit(trail_surf, self.trail_points[i])

        # Draw UI
        self.draw_ui()

        # Show help overlay
        if self.show_help:
            self.draw_help()

        pygame.display.flip()

    def draw_setup_feedback(self):
        """Draw visual feedback for setup mode"""
        origin = (self.width // 2, self.height // 2)
        (x1, y1), (x2, y2) = self.pendulum.tip_positions(self.state)

        # Convert to screen coordinates
        from pendulum_art.renderer import to_screen

        p1 = to_screen((x1, y1), (self.width, self.height), self.scale, offset=origin)
        p2 = to_screen((x2, y2), (self.width, self.height), self.scale, offset=origin)

        # Get mouse position for hover effects
        mouse_world = self.screen_to_world(self.mouse_pos, origin)
        click_threshold = 30 / self.scale

        # Check if mouse is near bobs
        dist_to_bob1 = np.sqrt((mouse_world[0] - x1) ** 2 + (mouse_world[1] - y1) ** 2)
        dist_to_bob2 = np.sqrt((mouse_world[0] - x2) ** 2 + (mouse_world[1] - y2) ** 2)

        # Draw highlights
        if self.dragging_bob == 1 or (
            self.dragging_bob is None and dist_to_bob1 < click_threshold
        ):
            pygame.draw.circle(
                self.screen, (255, 255, 0), p1, 15, 3
            )  # Yellow highlight

        if self.dragging_bob == 2 or (
            self.dragging_bob is None and dist_to_bob2 < click_threshold
        ):
            pygame.draw.circle(
                self.screen, (255, 255, 0), p2, 15, 3
            )  # Yellow highlight

    def draw_ui(self):
        # Status bar
        status_texts = [
            f"Color: {list(self.palette.keys())[list(self.palette.values()).index(self.current_color)]}",
            f"Brush: {self.brush_size}",
            f"{'Painting' if self.painting else 'Not Painting'}",
            f"{'Paused' if self.paused else 'Running'}",
        ]

        # Add setup mode status
        if self.setup_mode:
            status_texts.append("SETUP MODE: Click and drag pendulum bobs")
            if self.dragging_bob:
                status_texts.append(f"Dragging Bob {self.dragging_bob}")

        y_offset = 10
        for text in status_texts:
            color = (255, 255, 100) if "SETUP MODE" in text else (255, 255, 255)
            surface = self.small_font.render(text, True, color)
            self.screen.blit(surface, (10, y_offset))
            y_offset += 20

        # Color palette preview
        palette_y = self.height - 60
        x_offset = 10
        for key, color in self.palette.items():
            # Draw color square
            rect = pygame.Rect(x_offset, palette_y, 30, 30)
            pygame.draw.rect(self.screen, color, rect)
            if color == self.current_color:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 3)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

            # Draw key label
            key_surface = self.small_font.render(key, True, (255, 255, 255))
            self.screen.blit(key_surface, (x_offset + 35, palette_y + 5))
            x_offset += 70

    def draw_help(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        help_text = [
            "DOUBLE PENDULUM ART - CONTROLS",
            "",
            "SPACE - Hold to paint with pendulum tip",
            "1-9 - Select color from palette",
            "+/- - Change brush size",
            "P - Pause/unpause simulation",
            "R - Reset pendulum to initial position",
            "C - Clear canvas (artwork)",
            "V - Toggle pendulum visibility",
            "I - Toggle interactive setup mode",
            "S - Save current artwork",
            "L - Load preset (if available)",
            "H - Toggle this help",
            "ESC/Q - Quit",
            "",
            "INTERACTIVE SETUP:",
            "Press I to enter setup mode, then click and",
            "drag the pendulum bobs to set initial position.",
            "Press I again to exit setup and start simulation.",
            "",
            "Let the chaotic beauty of the double pendulum",
            "create unique artistic patterns!",
        ]

        y_start = 80
        for i, line in enumerate(help_text):
            if line == "DOUBLE PENDULUM ART - CONTROLS":
                surface = self.font.render(line, True, (255, 255, 100))
            elif line == "INTERACTIVE SETUP:":
                surface = self.small_font.render(line, True, (100, 255, 100))
            elif line == "":
                continue
            else:
                surface = self.small_font.render(line, True, (255, 255, 255))

            x = (self.width - surface.get_width()) // 2
            self.screen.blit(surface, (x, y_start + i * 22))

    def reset(self):
        """Reset pendulum to initial state"""
        self.state = self.initial_state.copy()
        self.trail_points.clear()

    def clear_canvas(self):
        """Clear the artwork canvas"""
        self.canvas.fill((0, 0, 0, 0))

    def save_artwork(self):
        """Save current artwork as PNG"""
        timestamp = int(time.time())
        filename = f"pendulum_art_{timestamp}.png"

        # Create a copy with black background for saving
        save_surface = pygame.Surface((self.width, self.height))
        save_surface.fill((0, 0, 0))
        save_surface.blit(self.canvas, (0, 0))

        pygame.image.save(save_surface, filename)
        print(f"Artwork saved as {filename}")

    def load_preset_dialog(self):
        """Load a preset if available"""
        preset_files = [f for f in os.listdir(".") if f.endswith(".json")]
        if preset_files:
            # For simplicity, load the first preset found
            try:
                state, palette = load_preset(preset_files[0])
                self.state = state
                self.initial_state = state.copy()
                self.palette.update(palette)
                print(f"Loaded preset: {preset_files[0]}")
            except Exception as e:
                print(f"Error loading preset: {e}")
        else:
            print("No preset files found")

    def run(self):
        """Main game loop"""
        running = True

        while running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS, dt in seconds

            running = self.handle_events()
            self.update_physics(dt)
            self.render()

        pygame.quit()
        sys.exit()

    def start_dragging(self, mouse_pos):
        """Start dragging a pendulum bob if clicked near one"""
        # Convert mouse position to world coordinates
        origin = (self.width // 2, self.height // 2)
        mouse_world = self.screen_to_world(mouse_pos, origin)

        # Get current bob positions
        (x1, y1), (x2, y2) = self.pendulum.tip_positions(self.state)

        # Check if mouse is near either bob (within 30 pixels)
        click_threshold = 30 / self.scale  # Convert pixels to world units

        dist_to_bob1 = np.sqrt((mouse_world[0] - x1) ** 2 + (mouse_world[1] - y1) ** 2)
        dist_to_bob2 = np.sqrt((mouse_world[0] - x2) ** 2 + (mouse_world[1] - y2) ** 2)

        if dist_to_bob1 < click_threshold:
            self.dragging_bob = 1
        elif dist_to_bob2 < click_threshold:
            self.dragging_bob = 2
        else:
            self.dragging_bob = None

    def stop_dragging(self):
        """Stop dragging and save the new initial state"""
        if self.dragging_bob is not None:
            # Save current state as new initial state
            self.initial_state = self.state.copy()
            # Reset velocities to zero for new initial state
            self.initial_state[2] = 0.0  # omega1
            self.initial_state[3] = 0.0  # omega2
            self.state = self.initial_state.copy()

        self.dragging_bob = None

    def update_pendulum_from_mouse(self, mouse_pos):
        """Update pendulum angles based on mouse position while dragging"""
        if self.dragging_bob is None:
            return

        # Convert mouse position to world coordinates
        origin = (self.width // 2, self.height // 2)
        mouse_world = self.screen_to_world(mouse_pos, origin)
        mx, my = mouse_world

        if self.dragging_bob == 1:
            # Dragging first bob - calculate theta1
            # theta1 = atan2(x, y) where (0,0) is pivot
            theta1 = np.arctan2(mx, my)

            # Keep theta2 relative to theta1 (maintain second pendulum orientation)
            current_theta1 = self.state[0]
            current_theta2 = self.state[1]
            relative_theta2 = current_theta2 - current_theta1

            self.state[0] = theta1
            self.state[1] = theta1 + relative_theta2

        elif self.dragging_bob == 2:
            # Dragging second bob - calculate theta2
            # First, we need the position of the first bob
            theta1 = self.state[0]
            x1 = self.pendulum.l1 * np.sin(theta1)
            y1 = self.pendulum.l1 * np.cos(theta1)

            # Calculate theta2 based on vector from first bob to mouse
            dx = mx - x1
            dy = my - y1
            theta2 = np.arctan2(dx, dy)

            self.state[1] = theta2

    def screen_to_world(self, screen_pos, origin):
        """Convert screen coordinates to world coordinates"""
        sx, sy = screen_pos
        ox, oy = origin

        # Convert to world coordinates (note: screen y increases downward)
        world_x = (sx - ox) / self.scale
        world_y = (sy - oy) / self.scale

        return world_x, world_y


def main():
    game = PendulumArtGame()
    game.run()


if __name__ == "__main__":
    main()
