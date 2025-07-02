import json
import os
import numpy as np
import pygame
import colorsys

# Extended color palette with more artistic options
DEFAULT_PALETTE = {
    "1": (255, 50, 50),   # Bright Red
    "2": (50, 255, 50),   # Bright Green  
    "3": (50, 50, 255),   # Bright Blue
    "4": (255, 255, 50),  # Bright Yellow
    "5": (255, 50, 255),  # Bright Magenta
    "6": (50, 255, 255),  # Cyan
    "7": (255, 150, 50),  # Orange
    "8": (150, 50, 255),  # Purple
    "9": (255, 255, 255), # White
}

# Preset initial conditions for interesting patterns
INTERESTING_PRESETS = {
    "chaos": np.array([np.pi/2, np.pi/4, 1.0, -0.5]),
    "figure_eight": np.array([np.pi/3, -np.pi/3, 0.5, 0.5]),
    "spiral": np.array([0.1, np.pi, 0.0, 2.0]),
    "butterfly": np.array([np.pi/6, 5*np.pi/6, 0.2, -0.2]),
    "flower": np.array([np.pi/4, 3*np.pi/4, 0.8, -0.8]),
}


def save_preset(state, palette, filename):
    """
    Save a preset of initial conditions and palette to JSON.
    - state: np.array([theta1, theta2, omega1, omega2])
    - palette: dict mapping keys to RGB tuples
    - filename: output .json filepath
    """
    data = {
        "state": state.tolist(), 
        "palette": palette,
        "description": f"Pendulum preset with initial angles: {state[0]:.3f}, {state[1]:.3f}"
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_preset(filename):
    """
    Load a preset JSON and return (state: np.array, palette: dict).
    """
    with open(filename, "r") as f:
        data = json.load(f)
    state = np.array(data["state"])
    palette = data.get("palette", DEFAULT_PALETTE)
    return state, palette


def save_artwork_with_metadata(surface, state, palette, filename_base=None):
    """
    Save artwork with associated metadata for reproducibility.
    """
    import time
    
    if filename_base is None:
        timestamp = int(time.time())
        filename_base = f"pendulum_art_{timestamp}"
    
    # Save the image
    pygame.image.save(surface, f"{filename_base}.png")
    
    # Save metadata
    metadata = {
        "timestamp": time.time(),
        "initial_state": state.tolist(),
        "palette": palette,
        "description": "Double pendulum art with reproducible parameters"
    }
    
    with open(f"{filename_base}_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    return f"{filename_base}.png", f"{filename_base}_metadata.json"


def list_presets(directory="."):
    """
    List all JSON presets in the given directory.
    """
    return [f for f in os.listdir(directory) if f.endswith(".json") and not f.endswith("_metadata.json")]


def generate_rainbow_palette(num_colors=9):
    """
    Generate a rainbow color palette with specified number of colors.
    """
    palette = {}
    for i in range(num_colors):
        hue = i / num_colors
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        palette[str(i + 1)] = tuple(int(255 * c) for c in rgb)
    return palette


def generate_warm_palette():
    """Generate a warm color palette (reds, oranges, yellows)"""
    return {
        "1": (255, 0, 0),     # Red
        "2": (255, 69, 0),    # Red-Orange
        "3": (255, 140, 0),   # Dark Orange
        "4": (255, 165, 0),   # Orange
        "5": (255, 215, 0),   # Gold
        "6": (255, 255, 0),   # Yellow
        "7": (255, 255, 224), # Light Yellow
        "8": (255, 192, 203), # Pink
        "9": (255, 255, 255), # White
    }


def generate_cool_palette():
    """Generate a cool color palette (blues, greens, purples)"""
    return {
        "1": (0, 0, 255),     # Blue
        "2": (0, 191, 255),   # Deep Sky Blue
        "3": (0, 255, 255),   # Cyan
        "4": (0, 255, 127),   # Spring Green
        "5": (0, 255, 0),     # Green
        "6": (127, 255, 212), # Aquamarine
        "7": (138, 43, 226),  # Blue Violet
        "8": (75, 0, 130),    # Indigo
        "9": (255, 255, 255), # White
    }


def create_preset_pack():
    """
    Create a pack of interesting presets for users to try.
    """
    preset_dir = "presets"
    if not os.path.exists(preset_dir):
        os.makedirs(preset_dir)
    
    palettes = {
        "default": DEFAULT_PALETTE,
        "rainbow": generate_rainbow_palette(),
        "warm": generate_warm_palette(),
        "cool": generate_cool_palette(),
    }
    
    # Create presets with different combinations
    for preset_name, state in INTERESTING_PRESETS.items():
        for palette_name, palette in palettes.items():
            filename = f"{preset_dir}/{preset_name}_{palette_name}.json"
            save_preset(state, palette, filename)
    
    return len(INTERESTING_PRESETS) * len(palettes)


def analyze_artwork_complexity(surface):
    """
    Analyze the complexity/coverage of an artwork.
    Returns metrics about the painting.
    """
    # Convert surface to numpy array for analysis
    width, height = surface.get_size()
    arr = pygame.surfarray.array3d(surface)
    
    # Count non-black pixels (assuming black background)
    non_black_pixels = np.sum(np.any(arr > 10, axis=2))  # threshold for "non-black"
    total_pixels = width * height
    coverage = non_black_pixels / total_pixels
    
    # Calculate color diversity
    unique_colors = len(np.unique(arr.reshape(-1, arr.shape[-1]), axis=0))
    
    # Calculate spatial distribution (spread)
    if non_black_pixels > 0:
        coords = np.where(np.any(arr > 10, axis=2))
        if len(coords[0]) > 0:
            spread_x = np.std(coords[0]) / width
            spread_y = np.std(coords[1]) / height
            spread = (spread_x + spread_y) / 2
        else:
            spread = 0
    else:
        spread = 0
    
    return {
        "coverage": coverage,
        "unique_colors": unique_colors,
        "spatial_spread": spread,
        "complexity_score": coverage * np.log1p(unique_colors) * (1 + spread)
    }
