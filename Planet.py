"""
Planet Class - Represents the planets in a simulation
"""
import numpy as np


class Planet:
    def __init__(self, g, name, mass, pos, velo, radius, colour):
        self.G = g
        self.name = name
        self.mass = mass
        self.pos = pos
        self.velo = velo
        self.current_accel = np.array([0, 0])
        self.previous_accel = np.array([0, 0])
        self.radius = radius
        self.colour = colour
