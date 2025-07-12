# User Guide

## Getting Started

### Launching the Application

```bash
# If installed from PyPI
pendulum-art

# If installed from source
python -m pendulum_art.main
```

### First Run

1. The application opens in **Setup Mode**
2. Drag the pendulum bobs to set your starting position
3. Click anywhere else to start the simulation
4. Press **SPACE** to start painting with the pendulum tip
5. Press **H** for help and all available controls

## Game Modes

### Setup Mode
- **Purpose**: Position your pendulum for interesting dynamics
- **Controls**: 
  - Drag pendulum bobs to desired positions
  - Click empty space to start simulation
- **Tips**: Higher positions create more energetic, chaotic motion

### Running Mode
- **Purpose**: Watch physics simulation and create art
- **Controls**: All painting and simulation controls active
- **Features**: Real-time physics, painting, recording

### Paused Mode
- **Purpose**: Pause simulation while keeping painting active
- **Access**: Press **P** during simulation
- **Uses**: Examine current state, adjust settings

## Controls Reference

### Setup Controls
| Key/Action | Function |
|------------|----------|
| **Mouse Drag** | Position pendulum bobs |
| **Click** | Start simulation |

### Painting Controls
| Key | Function |
|-----|----------|
| **SPACE** | Hold to paint with pendulum tip |
| **1-9** | Select color from palette |
| **+/-** | Adjust brush size (1-10) |
| **[ ]** | Adjust spray particles (2-20) |

### Simulation Controls
| Key | Function |
|-----|----------|
| **P** | Pause/Resume simulation |
| **R** | Reset to setup mode |
| **V** | Toggle pendulum visibility |
| **C** | Clear canvas |

### Recording Controls
| Key | Function |
|-----|----------|
| **F1** | Start/Stop video recording |
| **F2** | Save recorded video |

### File Operations
| Key | Function |
|-----|----------|
| **S** | Save current artwork as PNG |
| **Q/ESC** | Quit application |

### Help
| Key | Function |
|-----|----------|
| **H** | Toggle help panel |

## Creating Art

### Basic Painting
1. Set up your pendulum in an interesting position
2. Start the simulation
3. Hold **SPACE** to paint
4. Watch as chaotic motion creates beautiful patterns

### Advanced Techniques

#### Color Transitions
- Start with one color, then switch mid-painting
- Use **1-9** keys to change colors while painting
- Create layered effects with different colors

#### Brush Variations
- Use **+/-** to change brush size during painting
- Larger brushes create bold strokes
- Smaller brushes create fine details

#### Spray Effects
- Use **[ ]** to adjust spray particle count
- More particles create denser, more textured trails
- Fewer particles create cleaner, more defined lines

#### Strategic Pausing
- Press **P** to pause physics but continue painting
- Allows you to paint specific areas manually
- Resume with **P** to continue chaotic motion

## Physics Tips

### Creating Interesting Motion
- **High Energy**: Position pendulums near vertical
- **Symmetric**: Start both pendulums at similar angles
- **Asymmetric**: Use very different starting positions
- **Velocity**: The system adds initial angular velocity automatically

### Understanding Chaos
- Small changes in starting position create vastly different patterns
- The system is deterministic but unpredictable
- Longer simulations reveal more complex patterns
- Energy is conserved (pendulum motion gradually slows)

## Video Recording

### Manual Recording
1. Press **F1** to start recording
2. Set up and paint your artwork
3. Press **F1** again to stop (or wait for 30s limit)
4. Press **F2** to save as MP4 file

### Automatic Demo
```bash
python scripts/create_demo.py
```

### Recording Tips
- Plan your artwork before starting recording
- 30-second limit keeps file sizes manageable
- Higher motion creates more interesting videos
- Consider color progression for visual appeal

## File Management

### Artwork Files
- **Format**: PNG with transparency
- **Location**: Current directory
- **Naming**: `pendulum_art_[timestamp].png`
- **Size**: Varies based on canvas content

### Video Files
- **Format**: MP4 (H.264)
- **Location**: Current directory  
- **Naming**: `pendulum_demo_[timestamp].mp4`
- **Settings**: 30 FPS, 1000x800 resolution

## Troubleshooting

### Performance Issues
- Close other applications for better performance
- Reduce spray particles if frame rate drops
- Use smaller brush sizes for better performance

### Recording Problems
- Ensure `imageio[ffmpeg]` is installed
- Check available disk space
- Try shorter recording sessions

### Physics Anomalies
- Reset if pendulum behavior seems wrong
- Avoid extreme starting positions
- Report persistent issues on GitHub

## Advanced Usage

### Custom Modifications
The application is designed to be extensible:
- Modify color palettes in `utils.py`
- Adjust physics parameters in `physics.py`
- Customize rendering in `renderer.py`

### Batch Processing
Create multiple artworks programmatically:
```python
from pendulum_art import PendulumArtGame
# Your custom automation code here
```
