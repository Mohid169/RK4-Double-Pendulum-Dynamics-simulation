import json
import os
import numpy as np

# Default color palette: keys '1'–'5'
DEFAULT_PALETTE = {
    "1": (255, 0, 0),  # Red
    "2": (0, 255, 0),  # Green
    "3": (0, 0, 255),  # Blue
    "4": (255, 255, 0),  # Yellow
    "5": (255, 0, 255),  # Magenta
}


def save_preset(state, palette, filename):
    """
    Save a preset of initial conditions and palette to JSON.
    - state: np.array([theta1, theta2, omega1, omega2])
    - palette: dict mapping keys to RGB tuples
    - filename: output .json filepath
    """
    data = {"state": state.tolist(), "palette": palette}
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


def list_presets(directory="."):
    """
    List all JSON presets in the given directory.
    """
    return [f for f in os.listdir(directory) if f.endswith(".json")]
