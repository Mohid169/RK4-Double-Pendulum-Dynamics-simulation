# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for development installation)

## Quick Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install double-pendulum-art
```

### Option 2: Install from Source

```bash
git clone https://github.com/yourusername/RK4-Double-Pendulum-Dynamics-simulation.git
cd RK4-Double-Pendulum-Dynamics-simulation
pip install -e .
```

### Option 3: Development Installation

```bash
git clone https://github.com/yourusername/RK4-Double-Pendulum-Dynamics-simulation.git
cd RK4-Double-Pendulum-Dynamics-simulation
pip install -e ".[dev]"
```

## Optional Dependencies

### Video Recording Support

For video recording capabilities, install the video extras:

```bash
pip install "double-pendulum-art[video]"
```

Or manually install:

```bash
pip install imageio[ffmpeg]
```

### Development Dependencies

For development and testing:

```bash
pip install "double-pendulum-art[dev]"
```

## Verification

Test your installation:

```bash
# If installed from PyPI
pendulum-art

# If installed from source
python -m pendulum_art.main
```

## System Requirements

- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 100MB for installation, additional space for recordings
- **Graphics**: OpenGL support recommended for smooth rendering
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

## Troubleshooting

### Common Issues

1. **pygame not displaying**: Install system dependencies
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-pygame
   
   # macOS
   brew install pygame
   ```

2. **Video recording fails**: Install FFmpeg
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

3. **Permission errors**: Use virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install double-pendulum-art
   ```

### Getting Help

- Check the [FAQ](FAQ.md)
- Report issues on [GitHub Issues](https://github.com/yourusername/RK4-Double-Pendulum-Dynamics-simulation/issues)
- Join our [Discord community](https://discord.gg/your-invite) 