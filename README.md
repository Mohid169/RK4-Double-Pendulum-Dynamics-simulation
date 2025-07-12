# Pendulum Paint 🎨

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/double-pendulum-art.svg)](https://badge.fury.io/py/double-pendulum-art)

An interactive physics simulation and artistic visualization application that transforms the chaotic beauty of double pendulum dynamics into stunning digital art.

## 🎬 Demo

Watch the mesmerizing patterns created by chaotic pendulum motion:

<div align="center">
  <img src="assets/demos/Demo.gif" alt="Double Pendulum Art Demo" width="600"/>
</div>

*The demo shows the pendulum painting beautiful, unpredictable patterns as it moves through phase space. Each trace is unique due to the chaotic nature of the double pendulum system. Demo was compressed 10 mb to shown in the README.*

## ✨ Features

- 🎯 **Interactive Setup**: Intuitive drag-and-drop pendulum positioning
- ⚡ **Real-time Physics**: Accurate 4th-order Runge-Kutta integration
- 🎨 **Artistic Painting**: Paint with the pendulum tip using customizable colors and brushes
- 📹 **Video Recording**: Record and save your artistic creations as MP4 videos
- 🎮 **Professional UI**: Clean interface with comprehensive help system
- 🔧 **Extensible**: Modular codebase for easy customization

## 🚀 Quick Start

### Installation

```bash
pip install double-pendulum-art
```

### Launch

```bash
pendulum-art
```

### Create Your First Artwork

1. **Setup**: Drag pendulum bobs to interesting positions
2. **Start**: Click anywhere to begin simulation  
3. **Paint**: Hold **SPACE** to paint with the pendulum tip
4. **Record**: Press **F1** to start recording, **F2** to save

> 💡 **Pro Tip**: Try starting with pendulum bobs near vertical positions for dramatic, high-energy patterns like shown in the demo above!

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Mouse Drag** | Position pendulum bobs (setup mode) |
| **SPACE** | Hold to paint with pendulum tip |
| **1-9** | Select colors from palette |
| **+/-** | Adjust brush size (1-10) |
| **[ ]** | Adjust spray particles (2-20) |
| **P** | Pause/Resume simulation |
| **R** | Reset to setup mode |
| **C** | Clear canvas |
| **V** | Toggle pendulum visibility |
| **S** | Save artwork as PNG |
| **F1** | Start/Stop video recording |
| **F2** | Save recorded video |
| **H** | Show help panel |
| **Q/ESC** | Quit application |

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [User Guide](docs/USER_GUIDE.md) - Complete usage documentation
- [API Reference](docs/API.md) - For developers and customization

## 🎯 Physics

The simulation uses the exact equations of motion for a double pendulum system:

- **Accurate Integration**: 4th-order Runge-Kutta method
- **Chaotic Dynamics**: Sensitive dependence on initial conditions
- **Energy Conservation**: Realistic pendulum behavior
- **Numerical Stability**: Robust against computational errors


## 🛠️ Development

### Project Structure
```
├── src/pendulum_art/          # Main package
│   ├── game.py               # Game logic and UI
│   ├── physics.py            # Double pendulum physics
│   ├── renderer.py           # Graphics rendering
│   └── utils.py              # Utilities and constants
├── scripts/                   # Utility scripts
│   ├── create_demo.py        # Automated demo creation
│   ├── convert_to_gif.py     # Video to GIF conversion
│   └── build_executable.py  # Standalone app builder
├── docs/                     # Documentation
└── tests/                    # Test suite
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📊 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 100MB for installation
- **Graphics**: OpenGL support recommended
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Physics equations derived from classical mechanics
- Inspired by chaos theory and nonlinear dynamics
- Built with pygame and modern Python practices
- Thanks to the open-source community for tools and inspiration

---

**Made with ❤️ for science, art, and the beauty of chaos**

