#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from pendulum_art.main import main

    if __name__ == "__main__":
        main()

except ImportError as e:
    print("Error: Required dependencies not found.")
    print("Please install the required packages:")
    print("  pip install numpy pygame")
    print("  pip install imageio[ffmpeg]  # For video recording")
    print()
    print(f"Specific error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error launching application: {e}")
    sys.exit(1)
