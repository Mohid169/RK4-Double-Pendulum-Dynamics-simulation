# Double Pendulum Art 🎨

An interactive double pendulum simulation that creates art through chaotic motion.

## Features

- Interactive setup: drag pendulum bobs to set starting position
- Real-time physics simulation using RK4 integration
- Spray paint effect when holding SPACE
- 9 color palette (keys 1-9)
- Adjustable brush size and spray particles
- Save artwork as PNG

## Installation

```bash
git clone https://github.com/mohidkhan/double-pendulum-art.git
cd double-pendulum-art
pip install numpy pygame
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Paint while held (when running) |
| `1-9` | Select color |
| `+/-` | Brush size |
| `[ ]` | Spray particles |
| `P` | Pause/Resume |
| `R` | Reset to setup |
| `C` | Clear canvas |
| `V` | Toggle pendulum visibility |
| `S` | Save artwork |
| `H` | Help |
| `Q/ESC` | Quit |

## Usage

1. **Setup**: Drag pendulum bobs to set starting position
2. **Start**: Click anywhere to begin simulation
3. **Paint**: Hold SPACE to create spray paint effect
4. **Save**: Press S to save your artwork

## Physics

The double pendulum demonstrates chaotic behavior - small changes in initial conditions create dramatically different patterns. The simulation uses the exact equations of motion derived from Lagrangian mechanics.

