#!/usr/bin/env python3
"""
Basic usage example for the Double Pendulum Art system.

This example shows how to:
1. Run the interactive art application
2. Create presets programmatically
3. Generate artwork automatically
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pygame
from pendulum_art.game import PendulumArtGame
from pendulum_art.physics import DoublePendulum
from pendulum_art.utils import create_preset_pack, INTERESTING_PRESETS


def run_interactive_game():
    """Launch the interactive pendulum art game"""
    print("Starting Double Pendulum Art...")
    print("Press H in the game for help and controls")
    
    game = PendulumArtGame(width=1000, height=800)
    game.run()


def create_example_presets():
    """Create example preset files"""
    print("Creating example presets...")
    num_presets = create_preset_pack()
    print(f"Created {num_presets} preset files in the 'presets' directory")
    
    # List the presets that were created
    import os
    if os.path.exists("presets"):
        presets = os.listdir("presets")
        print("\nAvailable presets:")
        for preset in sorted(presets):
            print(f"  - {preset}")


def generate_artwork_batch():
    """
    Generate a batch of artworks automatically using different presets.
    This demonstrates programmatic art generation.
    """
    print("Generating artwork batch...")
    
    # Initialize pygame for headless rendering
    pygame.init()
    pygame.display.set_mode((1, 1))  # Minimal display for headless mode
    
    # Create pendulum and canvas
    pendulum = DoublePendulum(l1=1.0, l2=0.5)
    canvas_size = (800, 800)
    
    output_dir = "generated_art"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for name, initial_state in INTERESTING_PRESETS.items():
        print(f"Generating artwork for preset: {name}")
        
        # Create canvas
        canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)
        canvas.fill((0, 0, 0, 0))
        
        # Simulate and paint
        state = initial_state.copy()
        dt = 0.01
        color = (255, 100, 100)  # Red color
        
        for i in range(5000):  # 50 seconds of simulation
            # Update physics
            state = pendulum.rk4_step(state, dt)
            
            # Get tip position and convert to screen coordinates
            (x1, y1), (x2, y2) = pendulum.tip_positions(state)
            screen_x = int(canvas_size[0]//2 + x2 * 200)  # scale factor 200
            screen_y = int(canvas_size[1]//2 + y2 * 200)
            
            # Paint if within bounds
            if 0 <= screen_x < canvas_size[0] and 0 <= screen_y < canvas_size[1]:
                pygame.draw.circle(canvas, color, (screen_x, screen_y), 2)
        
        # Save the artwork
        save_surface = pygame.Surface(canvas_size)
        save_surface.fill((0, 0, 0))  # Black background
        save_surface.blit(canvas, (0, 0))
        
        filename = f"{output_dir}/auto_generated_{name}.png"
        pygame.image.save(save_surface, filename)
        print(f"Saved: {filename}")
    
    pygame.quit()
    print(f"\nGenerated artworks saved in '{output_dir}' directory")


def main():
    """Main example runner"""
    print("Double Pendulum Art - Examples")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Run interactive art game")
        print("2. Create example presets")
        print("3. Generate artwork batch (automatic)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        try:
            if choice == "1":
                run_interactive_game()
            elif choice == "2":
                create_example_presets()
            elif choice == "3":
                generate_artwork_batch()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-4.")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main() 