#!/usr/bin/env python3
"""
Package the executable for distribution to end users.
"""

import os
import shutil
import zipfile
import platform
from datetime import datetime

def create_distribution_package():
    """Create a distribution package with the executable and instructions."""
    print("📦 Creating distribution package...")
    
    system = platform.system()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Determine package name and executable
    if system == "Darwin":
        package_name = f"DoublePendulumArt_macOS_{timestamp}"
        executable_name = "DoublePendulumArt.app"
    elif system == "Windows":
        package_name = f"DoublePendulumArt_Windows_{timestamp}"
        executable_name = "DoublePendulumArt.exe"
    elif system == "Linux":
        package_name = f"DoublePendulumArt_Linux_{timestamp}"
        executable_name = "DoublePendulumArt"
    else:
        print(f"❌ Unsupported platform: {system}")
        return False
    
    # Check if executable exists
    exe_path = f"dist/{executable_name}"
    if not os.path.exists(exe_path):
        print(f"❌ Executable not found: {exe_path}")
        print("Please run the build script first: python scripts/build_executable.py")
        return False
    
    # Create package directory
    package_dir = f"dist/{package_name}"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy executable
    if system == "Darwin":
        # Copy the entire .app bundle
        shutil.copytree(exe_path, f"{package_dir}/{executable_name}")
    else:
        # Copy the executable file
        shutil.copy2(exe_path, f"{package_dir}/{executable_name}")
    
    # Copy README
    shutil.copy2("dist/README_DISTRIBUTION.md", f"{package_dir}/README.md")
    
    # Copy demo GIF for reference
    if os.path.exists("assets/demos/Demo.gif"):
        shutil.copy2("assets/demos/Demo.gif", f"{package_dir}/Demo.gif")
    
    # Create a simple launcher script for easier access
    if system != "Darwin":  # macOS doesn't need this
        launcher_content = create_launcher_script(executable_name, system)
        launcher_name = "Launch_DoublePendulumArt.bat" if system == "Windows" else "launch.sh"
        
        with open(f"{package_dir}/{launcher_name}", "w") as f:
            f.write(launcher_content)
        
        if system == "Linux":
            os.chmod(f"{package_dir}/{launcher_name}", 0o755)
    
    print(f"✅ Package created: {package_dir}")
    
    # Create ZIP file
    zip_path = f"{package_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_path)
    
    # Get package size
    zip_size = os.path.getsize(zip_path) / (1024 * 1024)
    
    print(f"✅ Distribution package created: {zip_path}")
    print(f"📊 Package size: {zip_size:.1f} MB")
    print(f"📤 Ready to distribute! Share the ZIP file with users.")
    
    return True

def create_launcher_script(executable_name, system):
    """Create a launcher script for the executable."""
    if system == "Windows":
        return f"""@echo off
echo Starting Double Pendulum Art...
echo.
echo If you see any errors, try running as administrator.
echo Close this window to exit the application.
echo.
"{executable_name}"
pause
"""
    else:  # Linux
        return f"""#!/bin/bash
echo "Starting Double Pendulum Art..."
echo ""
echo "If you see any errors, try running with sudo or check permissions."
echo "Close this terminal to exit the application."
echo ""
./{executable_name}
echo ""
echo "Application closed. Press Enter to exit."
read
"""

def main():
    """Main entry point."""
    print("🎨 Double Pendulum Art - Distribution Packager")
    print("=" * 50)
    
    if not create_distribution_package():
        print("❌ Packaging failed!")
        return False
    
    print("\n🎉 Distribution package ready!")
    print("\n💡 Distribution tips:")
    print("   • Test the package on a different computer")
    print("   • Include the README.md for user instructions")
    print("   • The ZIP file contains everything users need")
    print("   • No Python installation required for end users")
    
    return True

if __name__ == "__main__":
    main() 