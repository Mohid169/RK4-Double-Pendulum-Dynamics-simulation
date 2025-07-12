#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pendulum_art.game import main

    if __name__ == "__main__":
        print("🎨 Double Pendulum Art")
        print("=" * 30)
        print("Starting the interactive pendulum art application...")
        print("Press H in the game window for help and controls.")
        print()
        main()

except ImportError as e:
    print("Error: Required dependencies not found.")
    print("Please install the required packages:")
    print("  pip install numpy pygame matplotlib")
    print()
    print(f"Specific error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error launching application: {e}")
    sys.exit(1)
