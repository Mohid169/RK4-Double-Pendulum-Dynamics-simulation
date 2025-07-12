import pygame
import sys
import numpy as np
from pendulum_art.physics import DoublePendulum
from pendulum_art.renderer import draw_pendulum, to_screen
from pendulum_art.utils import DEFAULT_PALETTE
import time
import os


class PendulumArtGame:
    def __init__(self, width=1000, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Double Pendulum Art")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.pendulum = DoublePendulum(l1=1.0, l2=0.5)

        self.initial_state = np.array([np.pi / 4, np.pi / 6, 0.0, 0.0])
        self.state = self.initial_state.copy()

        self.game_state = "SETUP"
        self.dragging_bob = None
        self.mouse_pos = (0, 0)

        self.scale = 200
        self.show_pendulum = True
        self.show_help = False
        self.painting = False

        self.canvas = pygame.Surface((width, height), pygame.SRCALPHA)

        # Video recording setup
        self.recording = False
        self.recorded_frames = []
        self.recording_fps = 30
        self.recording_start_time = 0
        self.max_recording_time = 30  # seconds
        self.frame_count = 0

        self.current_color = (255, 255, 255)
        self.brush_size = 3
        self.spray_particles = 8
        self.palette = {
            "1": (255, 100, 100),
            "2": (100, 255, 100),
            "3": (100, 100, 255),
            "4": (255, 255, 100),
            "5": (255, 100, 255),
            "6": (100, 255, 255),
            "7": (255, 165, 0),
            "8": (160, 100, 255),
            "9": (255, 255, 255),
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_state == "RUNNING":
                        self.painting = True
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help
                elif event.key == pygame.K_p:
                    if self.game_state == "RUNNING":
                        self.game_state = "PAUSED"
                    elif self.game_state == "PAUSED":
                        self.game_state = "RUNNING"
                elif event.key == pygame.K_r:
                    self.reset_to_setup()
                elif event.key == pygame.K_c:
                    self.clear_canvas()
                elif event.key == pygame.K_v:
                    self.show_pendulum = not self.show_pendulum
                elif event.key == pygame.K_s:
                    self.save_artwork()
                elif event.key == pygame.K_F1:  # F1 to start/stop recording
                    self.toggle_recording()
                elif event.key == pygame.K_F2:  # F2 to save recorded video
                    if self.recorded_frames:
                        self.save_video()
                elif pygame.K_1 <= event.key <= pygame.K_9:
                    key_str = str(event.key - pygame.K_0)
                    if key_str in self.palette:
                        self.current_color = self.palette[key_str]
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.brush_size = min(10, self.brush_size + 1)
                elif event.key == pygame.K_MINUS:
                    self.brush_size = max(1, self.brush_size - 1)
                elif event.key == pygame.K_RIGHTBRACKET:
                    self.spray_particles = min(20, self.spray_particles + 2)
                elif event.key == pygame.K_LEFTBRACKET:
                    self.spray_particles = max(2, self.spray_particles - 2)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.painting = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_state == "SETUP":
                        if self.try_start_dragging(event.pos):
                            pass
                        else:
                            self.start_simulation()
                    elif self.game_state in ["RUNNING", "PAUSED"]:
                        self.reset_to_setup()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.game_state == "SETUP":
                    self.stop_dragging()

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                if self.game_state == "SETUP" and self.dragging_bob is not None:
                    self.update_pendulum_from_mouse(event.pos)

        return True

    def toggle_recording(self):
        """Toggle video recording on/off"""
        if not self.recording:
            # Start recording
            self.recording = True
            self.recorded_frames = []
            self.recording_start_time = time.time()
            self.frame_count = 0
            print("🎬 Recording started! Press F1 to stop, F2 to save video.")
        else:
            # Stop recording
            self.recording = False
            recording_duration = time.time() - self.recording_start_time
            print(
                f"🎬 Recording stopped! Captured {len(self.recorded_frames)} frames in {recording_duration:.1f}s"
            )
            if self.recorded_frames:
                print("Press F2 to save the video, or F1 to start a new recording.")

    def capture_frame(self):
        """Capture current frame for video recording"""
        if self.recording:
            # Check if we've hit the max recording time
            if time.time() - self.recording_start_time >= self.max_recording_time:
                print(
                    f"🎬 Maximum recording time ({self.max_recording_time}s) reached. Stopping recording."
                )
                self.recording = False
                return

            # Capture the current screen
            frame_surface = self.screen.copy()
            # Convert to a format suitable for video encoding
            frame_array = pygame.surfarray.array3d(frame_surface)
            # Transpose to get correct orientation (pygame uses (width, height, channels))
            frame_array = np.transpose(frame_array, (1, 0, 2))
            self.recorded_frames.append(frame_array)
            self.frame_count += 1

    def save_video(self):
        """Save recorded frames as a video file"""
        if not self.recorded_frames:
            print("❌ No frames to save!")
            return

        try:
            # Try to import imageio for video creation
            import imageio

            # Create filename with timestamp
            timestamp = int(time.time())
            filename = f"pendulum_demo_{timestamp}.mp4"

            print(f"🎬 Saving video with {len(self.recorded_frames)} frames...")

            # Create video writer
            with imageio.get_writer(filename, fps=self.recording_fps) as writer:
                for frame in self.recorded_frames:
                    writer.append_data(frame)

            print(f"✅ Video saved as {filename}")

            # Clear recorded frames to free memory
            self.recorded_frames = []

        except ImportError:
            print("❌ imageio not installed. Installing it now...")
            print("Run: pip install imageio[ffmpeg]")
            print("Then press F2 again to save the video.")

            # Save as individual PNG frames as fallback
            self.save_frames_as_images()

        except Exception as e:
            print(f"❌ Error saving video: {e}")
            print("Saving as individual frames instead...")
            self.save_frames_as_images()

    def save_frames_as_images(self):
        """Fallback: save frames as individual PNG images"""
        timestamp = int(time.time())
        frames_dir = f"pendulum_frames_{timestamp}"
        os.makedirs(frames_dir, exist_ok=True)

        print(f"💾 Saving {len(self.recorded_frames)} frames to {frames_dir}/")

        for i, frame in enumerate(self.recorded_frames):
            # Convert numpy array back to pygame surface
            frame_surface = pygame.surfarray.make_surface(
                np.transpose(frame, (1, 0, 2))
            )
            pygame.image.save(frame_surface, f"{frames_dir}/frame_{i:04d}.png")

        print(f"✅ Frames saved! You can create a video with:")
        print(
            f"ffmpeg -framerate {self.recording_fps} -i {frames_dir}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p pendulum_demo_{timestamp}.mp4"
        )

    def update_physics(self, dt):
        if self.game_state == "RUNNING":
            self.state = self.pendulum.rk4_step(self.state, dt)

            if self.painting:
                (x1, y1), (x2, y2) = self.pendulum.tip_positions(self.state)

                origin = (self.width // 2, self.height // 2)
                tip_screen = to_screen(
                    (x2, y2), (self.width, self.height), self.scale, offset=origin
                )

                if 0 <= tip_screen[0] < self.width and 0 <= tip_screen[1] < self.height:
                    self.create_spray_effect(tip_screen)

    def create_spray_effect(self, center_pos):
        import random

        cx, cy = center_pos

        for _ in range(self.spray_particles):
            angle = random.uniform(0, 2 * np.pi)
            distance = random.uniform(0, self.brush_size * 2)

            offset_x = int(distance * np.cos(angle))
            offset_y = int(distance * np.sin(angle))

            particle_x = cx + offset_x
            particle_y = cy + offset_y

            particle_size = random.randint(1, 3)

            r, g, b = self.current_color
            r = max(0, min(255, r + random.randint(-20, 20)))
            g = max(0, min(255, g + random.randint(-20, 20)))
            b = max(0, min(255, b + random.randint(-20, 20)))
            particle_color = (r, g, b)

            alpha = random.randint(100, 255)

            if 0 <= particle_x < self.width and 0 <= particle_y < self.height:
                particle_surf = pygame.Surface(
                    (particle_size * 2, particle_size * 2), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    particle_surf,
                    (*particle_color, alpha),
                    (particle_size, particle_size),
                    particle_size,
                )
                self.canvas.blit(
                    particle_surf,
                    (particle_x - particle_size, particle_y - particle_size),
                )

    def render(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.canvas, (0, 0))

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

        if self.game_state == "SETUP":
            self.draw_setup_feedback()
            self.draw_setup_instructions()

        self.draw_ui()

        # Draw recording indicator
        if self.recording:
            self.draw_recording_indicator()

        if self.show_help:
            self.draw_help()

        pygame.display.flip()

        # Capture frame after rendering
        self.capture_frame()

    def draw_recording_indicator(self):
        """Draw recording indicator in top-right corner"""
        # Blinking red circle
        if int(time.time() * 2) % 2:  # Blink every 0.5 seconds
            pygame.draw.circle(self.screen, (255, 0, 0), (self.width - 30, 30), 10)

        # Recording text
        recording_time = time.time() - self.recording_start_time
        time_text = f"REC {recording_time:.1f}s"
        text_surface = self.small_font.render(time_text, True, (255, 0, 0))
        self.screen.blit(text_surface, (self.width - 120, 20))

        # Frame count
        frame_text = f"Frames: {len(self.recorded_frames)}"
        frame_surface = self.small_font.render(frame_text, True, (255, 255, 255))
        self.screen.blit(frame_surface, (self.width - 120, 45))

    def draw_setup_feedback(self):
        origin = (self.width // 2, self.height // 2)
        (x1, y1), (x2, y2) = self.pendulum.tip_positions(self.state)

        pos1 = to_screen((x1, y1), (self.width, self.height), self.scale, offset=origin)
        pos2 = to_screen((x2, y2), (self.width, self.height), self.scale, offset=origin)

        # Draw constraint circles (valid drag areas)
        pygame.draw.circle(
            self.screen, (40, 40, 40), origin, int(self.pendulum.l1 * self.scale), 1
        )
        pygame.draw.circle(
            self.screen, (40, 40, 40), pos1, int(self.pendulum.l2 * self.scale), 1
        )

        # Enhanced bob visualization
        if self.dragging_bob == 1:
            # Dragging bob 1 - show it following mouse with constraint
            constrained_pos = self.get_constrained_position(
                self.mouse_pos, origin, self.pendulum.l1
            )

            # Check if constrained (different from mouse position)
            is_constrained = (
                abs(constrained_pos[0] - self.mouse_pos[0]) > 5
                or abs(constrained_pos[1] - self.mouse_pos[1]) > 5
            )

            # Draw ghost/preview at mouse position if constrained
            if is_constrained:
                pygame.draw.circle(self.screen, (255, 255, 0, 100), self.mouse_pos, 12)
                pygame.draw.circle(self.screen, (255, 255, 0), self.mouse_pos, 12, 2)

            # Draw actual position
            pygame.draw.circle(self.screen, (255, 255, 0), constrained_pos, 15, 3)

            # Draw constraint line
            pygame.draw.line(self.screen, (255, 255, 0), origin, constrained_pos, 2)

        elif self.dragging_bob == 2:
            # Dragging bob 2 - show it following mouse with constraint
            constrained_pos = self.get_constrained_position(
                self.mouse_pos, pos1, self.pendulum.l2
            )

            # Check if constrained (different from mouse position)
            is_constrained = (
                abs(constrained_pos[0] - self.mouse_pos[0]) > 5
                or abs(constrained_pos[1] - self.mouse_pos[1]) > 5
            )

            # Draw ghost/preview at mouse position if constrained
            if is_constrained:
                pygame.draw.circle(self.screen, (255, 255, 0, 100), self.mouse_pos, 12)
                pygame.draw.circle(self.screen, (255, 255, 0), self.mouse_pos, 12, 2)

            # Draw actual position
            pygame.draw.circle(self.screen, (255, 255, 0), constrained_pos, 15, 3)

            # Draw constraint line
            pygame.draw.line(self.screen, (255, 255, 0), pos1, constrained_pos, 2)

        else:
            # Not dragging - show hover effects
            mouse_dist1 = np.linalg.norm(np.array(self.mouse_pos) - np.array(pos1))
            mouse_dist2 = np.linalg.norm(np.array(self.mouse_pos) - np.array(pos2))

            # Larger, more obvious grab areas
            if mouse_dist1 < 40:
                pygame.draw.circle(self.screen, (255, 255, 0), pos1, 20, 3)
                pygame.draw.circle(self.screen, (255, 255, 0, 50), pos1, 20)
                # Show constraint preview
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 0, 30),
                    origin,
                    int(self.pendulum.l1 * self.scale),
                    2,
                )
            elif mouse_dist2 < 40:
                pygame.draw.circle(self.screen, (255, 255, 0), pos2, 20, 3)
                pygame.draw.circle(self.screen, (255, 255, 0, 50), pos2, 20)
                # Show constraint preview
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 0, 30),
                    pos1,
                    int(self.pendulum.l2 * self.scale),
                    2,
                )
            else:
                # Default state - show grabbable areas subtly
                pygame.draw.circle(self.screen, (100, 100, 100), pos1, 15, 2)
                pygame.draw.circle(self.screen, (100, 100, 100), pos2, 15, 2)

    def draw_setup_instructions(self):
        # Create a clean instruction panel
        panel_width = 400
        panel_height = 120
        panel_x = (self.width - panel_width) // 2
        panel_y = 40

        # Semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 180))
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Border
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            (panel_x, panel_y, panel_width, panel_height),
            2,
        )

        # Instructions
        title = self.font.render("SETUP", True, (255, 255, 100))
        instruction1 = self.small_font.render(
            "Drag the pendulum bobs to set position", True, (255, 255, 255)
        )
        instruction2 = self.small_font.render(
            "Click anywhere else to start", True, (255, 255, 255)
        )

        # Center text
        title_rect = title.get_rect(center=(panel_x + panel_width // 2, panel_y + 25))
        inst1_rect = instruction1.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 55)
        )
        inst2_rect = instruction2.get_rect(
            center=(panel_x + panel_width // 2, panel_y + 80)
        )

        self.screen.blit(title, title_rect)
        self.screen.blit(instruction1, inst1_rect)
        self.screen.blit(instruction2, inst2_rect)

    def draw_ui(self):
        # Status panel (top-left)
        if self.game_state == "SETUP":
            return  # Don't show UI controls in setup mode

        # Create control panel
        panel_width = 200
        panel_height = 140
        panel_x = 10
        panel_y = 10

        # Semi-transparent background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((0, 0, 0, 160))
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Border
        pygame.draw.rect(
            self.screen, (80, 80, 80), (panel_x, panel_y, panel_width, panel_height), 1
        )

        # Status
        if self.game_state == "RUNNING":
            status_text = "RUNNING"
            status_color = (100, 255, 100)
        elif self.game_state == "PAUSED":
            status_text = "PAUSED"
            status_color = (255, 255, 100)

        status = self.small_font.render(status_text, True, status_color)
        self.screen.blit(status, (panel_x + 10, panel_y + 10))

        # Paint status
        if self.painting:
            paint_text = self.small_font.render("🎨 PAINTING", True, (255, 255, 0))
            self.screen.blit(paint_text, (panel_x + 10, panel_y + 30))
        else:
            hint_text = self.small_font.render(
                "Hold SPACE to paint", True, (150, 150, 150)
            )
            self.screen.blit(hint_text, (panel_x + 10, panel_y + 30))

        # Controls
        y_offset = 55
        controls = [
            f"Brush: {self.brush_size} (+/-)",
            f"Spray: {self.spray_particles} ([/])",
        ]

        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, (200, 200, 200))
            self.screen.blit(text, (panel_x + 10, panel_y + y_offset + i * 18))

        # Color preview with label
        color_y = panel_y + y_offset + 36
        color_text = self.small_font.render("Color:", True, (200, 200, 200))
        self.screen.blit(color_text, (panel_x + 10, color_y))

        color_preview = pygame.Surface((20, 20))
        color_preview.fill(self.current_color)
        pygame.draw.rect(color_preview, (255, 255, 255), (0, 0, 20, 20), 1)
        self.screen.blit(color_preview, (panel_x + 60, color_y - 2))

        # Quick controls hint
        hint_text = self.small_font.render("Press H for help", True, (120, 120, 120))
        self.screen.blit(hint_text, (panel_x + 10, panel_y + panel_height - 20))

        # Color palette (bottom of screen)
        self.draw_color_palette()

    def draw_color_palette(self):
        """Draw color palette at bottom of screen"""
        if self.game_state == "SETUP":
            return

        palette_width = 300
        palette_height = 40
        palette_x = (self.width - palette_width) // 2
        palette_y = self.height - palette_height - 10

        # Background
        palette_surface = pygame.Surface(
            (palette_width, palette_height), pygame.SRCALPHA
        )
        palette_surface.fill((0, 0, 0, 140))
        self.screen.blit(palette_surface, (palette_x, palette_y))

        # Border
        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            (palette_x, palette_y, palette_width, palette_height),
            1,
        )

        # Color swatches
        swatch_size = 25
        start_x = palette_x + 15
        start_y = palette_y + 7

        for i, (key, color) in enumerate(self.palette.items()):
            x = start_x + i * 30

            # Color swatch
            swatch_rect = pygame.Rect(x, start_y, swatch_size, swatch_size)
            pygame.draw.rect(self.screen, color, swatch_rect)

            # Highlight current color
            if color == self.current_color:
                pygame.draw.rect(self.screen, (255, 255, 255), swatch_rect, 2)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), swatch_rect, 1)

            # Key number
            key_text = self.small_font.render(key, True, (255, 255, 255))
            key_rect = key_text.get_rect(
                center=(x + swatch_size // 2, start_y + swatch_size + 8)
            )
            self.screen.blit(key_text, key_rect)

    def draw_help(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Help panel
        panel_width = 500
        panel_height = 450
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2

        # Background
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((20, 20, 20, 240))
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Border
        pygame.draw.rect(
            self.screen,
            (100, 100, 100),
            (panel_x, panel_y, panel_width, panel_height),
            2,
        )

        # Title
        title = self.font.render("CONTROLS & HELP", True, (255, 255, 100))
        title_rect = title.get_rect(center=(panel_x + panel_width // 2, panel_y + 30))
        self.screen.blit(title, title_rect)

        # Sections
        sections = [
            (
                "SETUP MODE:",
                [
                    "• Drag pendulum bobs to set starting position",
                    "• Click anywhere else to start simulation",
                ],
            ),
            (
                "PAINTING:",
                [
                    "• SPACE - Hold to paint with pendulum tip",
                    "• 1-9 - Select color palette",
                    "• +/- - Adjust brush size",
                    "• [ ] - Adjust spray particles",
                ],
            ),
            (
                "SIMULATION:",
                [
                    "• P - Pause/Resume",
                    "• R - Reset to setup mode",
                    "• C - Clear canvas",
                    "• V - Toggle pendulum visibility",
                ],
            ),
            (
                "RECORDING:",
                [
                    "• F1 - Start/Stop video recording",
                    "• F2 - Save recorded video",
                    "• Max 30 seconds per recording",
                ],
            ),
            ("FILE:", ["• S - Save artwork as PNG", "• Q/ESC - Quit application"]),
        ]

        y_offset = 70
        for section_title, items in sections:
            # Section title
            section_text = self.small_font.render(section_title, True, (100, 255, 100))
            self.screen.blit(section_text, (panel_x + 30, panel_y + y_offset))
            y_offset += 25

            # Items
            for item in items:
                item_text = self.small_font.render(item, True, (200, 200, 200))
                self.screen.blit(item_text, (panel_x + 50, panel_y + y_offset))
                y_offset += 20

            y_offset += 10  # Space between sections

        # Close instruction
        close_text = self.small_font.render(
            "Press H again to close", True, (150, 150, 150)
        )
        close_rect = close_text.get_rect(
            center=(panel_x + panel_width // 2, panel_y + panel_height - 20)
        )
        self.screen.blit(close_text, close_rect)

    def reset(self):
        self.state = self.initial_state.copy()
        self.game_state = "SETUP"
        self.dragging_bob = None
        self.painting = False

    def clear_canvas(self):
        self.canvas.fill((0, 0, 0, 0))

    def save_artwork(self):
        timestamp = int(time.time())
        filename = f"pendulum_art_{timestamp}.png"
        pygame.image.save(self.canvas, filename)
        print(f"Artwork saved as {filename}")

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0

            running = self.handle_events()
            self.update_physics(dt)
            self.render()

        pygame.quit()
        sys.exit()

    def get_constrained_position(self, mouse_pos, anchor_pos, max_distance):
        """Get position constrained to a circle around anchor point"""
        dx = mouse_pos[0] - anchor_pos[0]
        dy = mouse_pos[1] - anchor_pos[1]
        distance = np.sqrt(dx * dx + dy * dy)

        # Constrain to circle if outside radius
        if distance > max_distance * self.scale:
            scale_factor = (max_distance * self.scale) / distance
            constrained_x = anchor_pos[0] + dx * scale_factor
            constrained_y = anchor_pos[1] + dy * scale_factor
            return (int(constrained_x), int(constrained_y))
        else:
            # Within radius - use mouse position directly
            return mouse_pos

    def try_start_dragging(self, mouse_pos):
        origin = (self.width // 2, self.height // 2)
        (x1, y1), (x2, y2) = self.pendulum.tip_positions(self.state)

        pos1 = to_screen((x1, y1), (self.width, self.height), self.scale, offset=origin)
        pos2 = to_screen((x2, y2), (self.width, self.height), self.scale, offset=origin)

        mouse_dist1 = np.linalg.norm(np.array(mouse_pos) - np.array(pos1))
        mouse_dist2 = np.linalg.norm(np.array(mouse_pos) - np.array(pos2))

        # Larger grab areas for better UX
        if mouse_dist1 < 40:
            self.dragging_bob = 1
            return True
        elif mouse_dist2 < 40:
            self.dragging_bob = 2
            return True

        return False

    def start_simulation(self):
        self.game_state = "RUNNING"
        self.dragging_bob = None

    def reset_to_setup(self):
        self.state = self.initial_state.copy()
        self.game_state = "SETUP"
        self.dragging_bob = None
        self.painting = False

    def stop_dragging(self):
        self.dragging_bob = None

    def update_pendulum_from_mouse(self, mouse_pos):
        origin = (self.width // 2, self.height // 2)

        if self.dragging_bob == 1:
            # Get constrained position and convert to world coordinates
            constrained_pos = self.get_constrained_position(
                mouse_pos, origin, self.pendulum.l1
            )
            world_pos = self.screen_to_world(constrained_pos, origin)

            # Calculate angle from constrained position
            theta1 = np.arctan2(world_pos[0], world_pos[1])
            self.state[0] = theta1

        elif self.dragging_bob == 2:
            # Get first bob position in screen coordinates
            (x1, y1), _ = self.pendulum.tip_positions(self.state)
            pos1 = to_screen(
                (x1, y1), (self.width, self.height), self.scale, offset=origin
            )

            # Get constrained position and convert to world coordinates
            constrained_pos = self.get_constrained_position(
                mouse_pos, pos1, self.pendulum.l2
            )
            world_pos = self.screen_to_world(constrained_pos, origin)

            # Calculate relative position and angle
            relative_pos = world_pos - np.array([x1, y1])
            theta2 = np.arctan2(relative_pos[0], relative_pos[1])
            self.state[1] = theta2

        # Reset velocities for clean setup
        self.state[2] = 0.0
        self.state[3] = 0.0

    def screen_to_world(self, screen_pos, origin):
        screen_x, screen_y = screen_pos
        origin_x, origin_y = origin

        world_x = (screen_x - origin_x) / self.scale
        world_y = (screen_y - origin_y) / self.scale

        return np.array([world_x, world_y])


def main():
    game = PendulumArtGame()
    game.run()


if __name__ == "__main__":
    main()
