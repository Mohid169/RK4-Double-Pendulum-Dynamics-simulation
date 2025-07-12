#!/usr/bin/env python3
"""
Main entry point for the Double Pendulum Art application.
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point for the application."""
    print("🎨 Double Pendulum Art")
    print("=" * 30)
    print("Starting the interactive pendulum art application...")
    print("Press H in the game window for help and controls.")
    print()
    
    try:
        from pendulum_art.game import PendulumArtGame
        game = PendulumArtGame()
        game.run()
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Double Pendulum Art!")
    except ImportError as e:
        print("Error: Required dependencies not found.")
        print("Please install the required packages:")
        print("  pip install numpy pygame")
        print("  pip install imageio[ffmpeg]  # For video recording")
        print()
        print(f"Specific error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
