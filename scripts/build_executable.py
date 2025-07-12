#!/usr/bin/env python3
"""
Build script to create standalone executables for Double Pendulum Art.
"""

import os
import sys
import shutil
import subprocess
import platform

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def clean_build_dirs():
    """Clean up previous build directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}/")

def build_executable():
    """Build the executable using PyInstaller."""
    print("🎨 Building Double Pendulum Art Executable")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found. Please run this script from the project root.")
        return False
    
    # Check if required dependencies are installed
    try:
        import pygame
        import numpy
        import imageio
        print("✅ All dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False
    
    # Clean previous builds
    clean_build_dirs()
    
    # Determine the platform
    system = platform.system()
    print(f"🖥️  Building for {system}")
    
    # Build the executable
    if system == "Darwin":  # macOS
        cmd = "pyinstaller build_executable.spec --clean --noconfirm"
        success = run_command(cmd, "Building macOS app bundle")
        
        if success:
            print("\n🎉 Build completed successfully!")
            print("📦 Executable created: dist/DoublePendulumArt.app")
            print("📝 To run: Double-click DoublePendulumArt.app")
            print("📤 To distribute: Zip the .app file and share")
            
    elif system == "Windows":
        # For Windows, create a simple executable
        cmd = "pyinstaller --onefile --windowed --name DoublePendulumArt main.py"
        success = run_command(cmd, "Building Windows executable")
        
        if success:
            print("\n🎉 Build completed successfully!")
            print("📦 Executable created: dist/DoublePendulumArt.exe")
            print("📝 To run: Double-click DoublePendulumArt.exe")
            print("📤 To distribute: Share the .exe file")
            
    elif system == "Linux":
        # For Linux, create a simple executable
        cmd = "pyinstaller --onefile --name DoublePendulumArt main.py"
        success = run_command(cmd, "Building Linux executable")
        
        if success:
            print("\n🎉 Build completed successfully!")
            print("📦 Executable created: dist/DoublePendulumArt")
            print("📝 To run: ./DoublePendulumArt")
            print("📤 To distribute: Share the executable file")
    else:
        print(f"❌ Unsupported platform: {system}")
        return False
    
    if success:
        # Show file size
        if system == "Darwin":
            if os.path.exists("dist/DoublePendulumArt.app"):
                size = get_dir_size("dist/DoublePendulumArt.app")
                print(f"📊 App bundle size: {size:.1f} MB")
        else:
            exe_name = "DoublePendulumArt.exe" if system == "Windows" else "DoublePendulumArt"
            exe_path = f"dist/{exe_name}"
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"📊 Executable size: {size:.1f} MB")
        
        print("\n💡 Tips for distribution:")
        print("   • Test the executable on a clean system")
        print("   • The executable is self-contained - no Python needed")
        print("   • Users can run it directly without installation")
        
        return True
    
    return False

def get_dir_size(path):
    """Get the size of a directory in MB."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)

def main():
    """Main entry point."""
    if not build_executable():
        sys.exit(1)
    
    print("\n🎨 Double Pendulum Art executable ready for distribution!")

if __name__ == "__main__":
    main() 