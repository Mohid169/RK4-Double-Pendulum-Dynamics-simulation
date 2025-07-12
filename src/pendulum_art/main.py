#!/usr/bin/env python3
"""
Main entry point for the Double Pendulum Art application.
"""

import sys
from .game import PendulumArtGame


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
        sys.exit(1)


if __name__ == "__main__":
    main() 