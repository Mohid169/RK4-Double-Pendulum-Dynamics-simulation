"""
Double Pendulum Art - Interactive Physics Simulation and Artistic Visualization

A beautiful, interactive application that combines the chaotic dynamics of a double pendulum
with artistic visualization capabilities. Create stunning patterns by painting with the
pendulum's motion, record videos, and explore the fascinating world of nonlinear dynamics.

Features:
- Interactive pendulum setup with drag-and-drop positioning
- Real-time physics simulation using 4th-order Runge-Kutta integration
- Artistic painting system with customizable colors and brushes
- Video recording capabilities for creating demos and art pieces
- Professional UI with help system and controls

Author: Your Name
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .game import PendulumArtGame
from .physics import DoublePendulum
from .renderer import draw_pendulum, to_screen
from .utils import DEFAULT_PALETTE

def main():
    """Main entry point for the application."""
    print("🎨 Double Pendulum Art")
    print("=" * 30)
    print("Starting the interactive pendulum art application...")
    print("Press H in the game window for help and controls.")
    print()
    
    try:
        game = PendulumArtGame()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Double Pendulum Art!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import sys
        sys.exit(1)

__all__ = [
    "PendulumArtGame",
    "DoublePendulum", 
    "draw_pendulum",
    "to_screen",
    "DEFAULT_PALETTE",
    "main",
] 