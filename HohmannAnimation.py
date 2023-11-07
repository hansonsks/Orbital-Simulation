"""
HohmannAnimation - A simple animation with hard-coded values demonstrating a satellite fly-past of Mars
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math


class HohmannAnimation:
    def __init__(self, angle=44, period=518.5, full_orbit=False):
        self.angle = angle
        self.satellite_period = period
        self.fig = plt.figure()
        self.ax = plt.axes()
        self.orbit = plt.Circle((0, 0), radius=1.75, fill=False, color="white")
        self.sun = plt.Circle((0, 0), radius=0.5, fill=True, color="yellow")
        self.earth = plt.Circle((0, 0), radius=0.09, fill=True, color="blue")
        self.mars = plt.Circle((0, 0), radius=0.05, fill=True, color="brown")
        self.satellite = plt.Circle((0, 0), radius=0.015, fill=True, color="green")
        if full_orbit:
            self.frames = 520
        else:
            self.frames = 250

    def init(self):
        self.earth.center = (0, 0)
        self.ax.add_patch(self.earth)
        self.mars.center = (0, 0)
        self.ax.add_patch(self.mars)
        self.satellite.center = (0, 0)
        self.ax.add_patch(self.satellite)
        return self.earth, self.mars, self.satellite

    def animate(self, i):
        """ Animation for the Earth, Mars, and the Satellite """
        earth_x = math.cos(2 * math.pi * i / 365)
        earth_y = math.sin(2 * math.pi * i / 365)
        self.earth.center = (earth_x, earth_y)

        mars_x = 1.52 * math.cos((2 * math.pi * i / 687) + (self.angle * math.pi / 180))
        mars_y = 1.52 * math.sin((2 * math.pi * i / 687) + (self.angle * math.pi / 180))
        self.mars.center = (mars_x, mars_y)

        satellite_x = 1.26 * (1 - 0.21 ** 2) / (1 + 0.21 * math.cos(2 * math.pi * i / self.satellite_period)) * \
                      math.cos((2 * math.pi * i / self.satellite_period))
        satellite_y = 1.26 * (1 - 0.21 ** 2) / (1 + 0.21 * math.cos(2 * math.pi * i / self.satellite_period)) * \
                      math.sin((2 * math.pi * i / self.satellite_period))
        self.satellite.center = (satellite_x, satellite_y)

        return self.earth, self.mars, self.satellite

    def run_sim(self):
        self.ax.add_patch(self.orbit)
        self.ax.add_patch(self.sun)
        plt.axis("scaled")
        anim = FuncAnimation(self.fig, self.animate, init_func=self.init, frames=self.frames, interval=20, blit=True)
        plt.title("Simulation of launching a satellite from Earth to Mars")
        plt.show()
