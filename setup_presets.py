#!/usr/bin/env python3
"""
Setup script to generate preset files for Double Pendulum Art.

Run this script to create a collection of interesting preset configurations
that showcase different types of pendulum motion and color palettes.
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pendulum_art.utils import create_preset_pack

    def main():
        print("🎨 Double Pendulum Art - Preset Generator")
        print("=" * 45)
        print()

        print("Generating preset files...")
        num_presets = create_preset_pack()

        print(
            f"✅ Successfully created {num_presets} preset files in the 'presets' directory!"
        )
        print()
        print("Presets include:")
        print("- Chaos patterns (unpredictable, beautiful motion)")
        print("- Figure-eight patterns (periodic loops)")
        print("- Spiral patterns (expanding/contracting spirals)")
        print("- Butterfly patterns (symmetric wing-like motion)")
        print("- Flower patterns (petal-like arrangements)")
        print()
        print("Each pattern comes with 4 different color palettes:")
        print("- Default (bright primary colors)")
        print("- Rainbow (full spectrum)")
        print("- Warm (reds, oranges, yellows)")
        print("- Cool (blues, greens, purples)")
        print()
        print("🎮 To use presets in the game:")
        print("1. Launch the main application")
        print("2. Press 'L' to load a preset")
        print("3. Press 'H' for help and full controls")
        print()
        print("Have fun creating art with chaotic motion! 🌟")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print("❌ Error: Missing dependencies!")
    print("Please install required packages:")
    print("  pip install numpy pygame matplotlib")
    print(f"\nSpecific error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error creating presets: {e}")
    sys.exit(1)
