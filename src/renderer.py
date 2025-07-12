import pygame
import numpy as np


def to_screen(coord, screen_size, scale=200, offset=None):
    """
    Map meter-based (x, y) coordinates to pixel coordinates.
      - coord: tuple (x, y) in meters
      - screen_size: (width, height) in pixels
      - scale: pixels per meter
      - offset: pixel origin, defaults to screen center
    """
    width, height = screen_size
    if offset is None:
        offset = (width // 2, height // 2)
    x, y = coord
    px = int(offset[0] + x * scale)
    py = int(offset[1] + y * scale)
    return px, py


def draw_pendulum(
    screen,
    state,
    pendulum,
    screen_size,
    scale=200,
    rod_color=(200, 200, 200),
    bob_color=(100, 100, 100),
    rod_width=3,
    bob_radius=8,
):
    """
    Draw the double-inverse pendulum on a Pygame surface.
      - screen: Pygame display surface
      - state: [theta1, theta2, omega1, omega2]
      - pendulum: DoublePendulum instance
      - screen_size: (width, height)
      - scale: conversion factor from meters to pixels
    """
    # Compute bob positions in meters
    (x1, y1), (x2, y2) = pendulum.tip_positions(state)

    # Origin in pixels
    origin = (screen_size[0] // 2, screen_size[1] // 2)
    # Convert to pixel coords
    p0 = origin
    p1 = to_screen((x1, y1), screen_size, scale, offset=origin)
    p2 = to_screen((x2, y2), screen_size, scale, offset=origin)

    # Draw rods
    pygame.draw.line(screen, rod_color, p0, p1, rod_width)
    pygame.draw.line(screen, rod_color, p1, p2, rod_width)

    # Draw bobs
    pygame.draw.circle(screen, bob_color, p1, bob_radius)
    pygame.draw.circle(screen, bob_color, p2, bob_radius)
