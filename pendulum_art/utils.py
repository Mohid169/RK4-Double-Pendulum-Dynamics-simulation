import pygame
import colorsys

DEFAULT_PALETTE = {
    "1": (255, 50, 50),
    "2": (50, 255, 50),
    "3": (50, 50, 255),
    "4": (255, 255, 50),
    "5": (255, 50, 255),
    "6": (50, 255, 255),
    "7": (255, 150, 50),
    "8": (150, 50, 255),
    "9": (255, 255, 255),
}


def generate_rainbow_palette(num_colors=9):
    palette = {}
    for i in range(num_colors):
        hue = i / num_colors
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        palette[str(i + 1)] = tuple(int(255 * c) for c in rgb)
    return palette


def generate_warm_palette():
    return {
        "1": (255, 0, 0),
        "2": (255, 69, 0),
        "3": (255, 140, 0),
        "4": (255, 165, 0),
        "5": (255, 215, 0),
        "6": (255, 255, 0),
        "7": (255, 255, 224),
        "8": (255, 192, 203),
        "9": (255, 255, 255),
    }


def generate_cool_palette():
    return {
        "1": (0, 0, 255),
        "2": (0, 191, 255),
        "3": (0, 255, 255),
        "4": (0, 255, 127),
        "5": (0, 255, 0),
        "6": (127, 255, 212),
        "7": (138, 43, 226),
        "8": (75, 0, 130),
        "9": (255, 255, 255),
    }
