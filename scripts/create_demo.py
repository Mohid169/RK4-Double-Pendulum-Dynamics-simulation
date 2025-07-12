#!/usr/bin/env python3
"""
Demo Video Creator for Double Pendulum Art
This script automatically creates a demo video showing the application's features.
"""

import sys
import os
import pygame
import numpy as np
import time

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pendulum_art.game import PendulumArtGame


class DemoRecorder(PendulumArtGame):
    """Extended game class for automated demo recording."""
    
    def __init__(self):
        super().__init__()
        self.demo_phase = 0
        self.phase_start_time = 0
        self.demo_actions = []
        self.auto_demo = True
        
    def create_demo_video(self):
        """Create an automated demo video"""
        print("🎬 Creating demo video...")
        print("This will take about 45 seconds to record a 30-second demo.")
        
        # Start recording immediately
        self.toggle_recording()
        
        # Run the demo
        self.run_demo()
        
        # Save the video
        if self.recorded_frames:
            print(f"🎬 Saving demo video with {len(self.recorded_frames)} frames...")
            self.save_video()
            print("✅ Demo video created successfully!")
        else:
            print("❌ No frames recorded!")
    
    def run_demo(self):
        """Run the automated demo sequence"""
        running = True
        demo_start_time = time.time()
        
        # Demo sequence phases
        phases = [
            {"duration": 2, "action": "setup_pendulum"},
            {"duration": 1, "action": "start_simulation"},
            {"duration": 10, "action": "paint_basic"},
            {"duration": 4, "action": "change_colors"},
            {"duration": 8, "action": "paint_more"},
            {"duration": 3, "action": "change_settings"},
            {"duration": 2, "action": "final_paint"},
        ]
        
        current_phase = 0
        phase_start = demo_start_time
        
        while running and current_phase < len(phases):
            dt = self.clock.tick(60) / 1000.0
            current_time = time.time()
            
            # Check if we should move to next phase
            if current_time - phase_start >= phases[current_phase]["duration"]:
                current_phase += 1
                phase_start = current_time
                if current_phase >= len(phases):
                    break
            
            # Execute current phase action
            if current_phase < len(phases):
                action = phases[current_phase]["action"]
                phase_progress = (current_time - phase_start) / phases[current_phase]["duration"]
                self.execute_demo_action(action, phase_progress)
            
            # Handle pygame events (but don't process user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update and render
            self.update_physics(dt)
            self.render()
            
            # Stop if recording is complete
            if not self.recording:
                break
        
        # Make sure we save the video before exiting
        if self.recorded_frames:
            print(f"🎬 Saving demo video with {len(self.recorded_frames)} frames...")
            self.save_video()
        
        pygame.quit()
        sys.exit()
    
    def execute_demo_action(self, action, progress):
        """Execute a specific demo action based on phase"""
        if action == "setup_pendulum":
            # Set up a high-energy, dramatic starting position
            if progress < 0.5:
                # Move first pendulum to near vertical (high energy)
                self.state[0] = np.pi * 0.9 + 0.2 * np.sin(progress * 4 * np.pi)
            else:
                # Move second pendulum to create interesting dynamics
                self.state[1] = np.pi * 0.7 + 0.3 * np.cos(progress * 6 * np.pi)
        
        elif action == "start_simulation":
            if progress > 0.5 and self.game_state == "SETUP":
                # Add some initial angular velocity for more dramatic motion
                self.state[2] = 0.5  # Angular velocity of first pendulum
                self.state[3] = -0.3  # Angular velocity of second pendulum
                self.start_simulation()
        
        elif action == "paint_basic":
            # Start painting
            self.painting = True
            # Use white color initially
            self.current_color = (255, 255, 255)
        
        elif action == "change_colors":
            # Cycle through colors
            colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
            color_index = int(progress * len(colors)) % len(colors)
            self.current_color = colors[color_index]
            self.painting = True
        
        elif action == "paint_more":
            # Continue painting with varied colors
            if progress < 0.3:
                self.current_color = (255, 255, 100)  # Yellow
            elif progress < 0.6:
                self.current_color = (255, 100, 255)  # Magenta
            else:
                self.current_color = (100, 255, 255)  # Cyan
            self.painting = True
        
        elif action == "change_settings":
            # Demonstrate changing brush settings
            self.brush_size = int(3 + 2 * np.sin(progress * 4 * np.pi))
            self.spray_particles = int(8 + 4 * np.cos(progress * 3 * np.pi))
            self.painting = True
        
        elif action == "final_paint":
            # Final painting with orange
            self.current_color = (255, 165, 0)
            self.painting = True


def main():
    """Main entry point for the demo creator."""
    print("🎨 Double Pendulum Art - Demo Video Creator")
    print("=" * 50)
    print("This will create a 30-second demo video showing:")
    print("• Pendulum setup and physics")
    print("• Painting with different colors")
    print("• Brush and spray settings")
    print("• Beautiful chaotic patterns")
    print()
    
    # Create and run demo
    demo = DemoRecorder()
    demo.create_demo_video()


if __name__ == "__main__":
    main() 