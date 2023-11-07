"""
Solar Class - The class that holds the simulation of the Solar System
"""

from Planet import Planet
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import math


class Solar:
    def __init__(self, timestep=100000):
        self.G = 6.6743E-11
        self.planets = []
        with open("input_params.txt") as planet_data:
            csv_reader = csv.reader(planet_data)
            for planet in csv_reader:
                name = str(planet[0])
                mass = float(planet[1])
                pos = np.array([float(planet[2]), float(planet[3])])
                velo = np.array([float(planet[4]), float(planet[5])])
                radius = float(planet[6])  # Not the actual radius, for animation purposes only
                colour = str(planet[7])
                self.planets.append(Planet(self.G, name, mass, pos, velo, radius, colour))
        self.timestep = timestep
        self.time_passed = 0

    def calc_force(self, p1):
        """ Calculates the total force applied on the given planet by other planets (Used for acceleration) """
        total_force = np.array([0.0, 0.0])  # Must be floats to avoid adding floats to ints
        for p2 in self.planets:
            if (p1 != p2):
                s = p2.pos - p1.pos
                direction = self.normalise_vec(s)
                mag_squared = np.linalg.norm(s) ** 2
                if (mag_squared != 0):
                    total_force += ((self.G * p1.mass * p2.mass) / mag_squared) * direction
                else:
                    total_force += np.zeros(2)
        return total_force

    def update_pos(self, planet):
        """ Updates current acceleration for calculation of the next position """
        planet.current_accel = self.calc_force(planet) / planet.mass
        # The following is Beeman Formula 1
        next_pos = planet.pos + (planet.velo * self.timestep) + \
                   (1 / 6) * ((4 * planet.current_accel) - planet.previous_accel) * (self.timestep ** 2)
        return next_pos

    def update_velo(self, planet):
        """ Calculates the next acceleration for the next velocity and Updates the accelerations """
        next_accel = self.calc_force(planet) / planet.mass
        # The following is Beeman Formula 2
        next_velo = planet.velo + (1 / 6) * ((2 * next_accel) + (5 * planet.current_accel) - planet.previous_accel) * \
                    self.timestep
        planet.previous_accel = planet.current_accel
        planet.current_accel = next_accel
        return next_velo

    def run_sim(self):
        """ Each simulation requires updating the positions and velocities of all planets """
        self.time_passed += self.timestep

        planet_coords = []
        for i in range(len(self.planets)):  # Calculate the positions of the planets
            planet_coords.append(self.update_pos(self.planets[i]))
        for j in range(len(self.planets)):  # Update the positions of the planets for the animation
            self.planets[j].pos = planet_coords[j]
        for k in range(len(self.planets)):  # Calculates and Updates the velocities of the planets
            self.planets[k].velo = self.update_velo(self.planets[k])

    def animate(self, i, patches):
        self.run_sim()
        for i in range(len(patches)):
            patches[i].center = (self.planets[i].pos[0], self.planets[i].pos[1])

    def run(self):
        fig = plt.figure()
        ax = plt.axes()

        ax.axis("scaled")
        max_orbit = math.sqrt(np.dot(self.planets[-1].pos[0], self.planets[-1].pos[0])) * 1.15
        ax.set_xlim(-max_orbit, max_orbit)
        ax.set_ylim(-max_orbit, max_orbit)

        patches = []
        for planet in self.planets:
            planet_patch = plt.Circle((planet.pos[0], planet.pos[1]), planet.radius * 750000, color=planet.colour)
            ax.add_patch(planet_patch)
            patches.append(planet_patch)

        anim = FuncAnimation(fig, self.animate, fargs=(patches,), interval=1)
        plt.title("Simulation of the Solar System")
        plt.show()

    def get_planet(self, p1):
        for p2 in self.planets:
            if p2.name == p1:
                return p2

    @staticmethod
    def normalise_vec(vector):
        return vector if (np.linalg.norm(vector) == 0) else (vector / np.linalg.norm(vector))


"""
SolarEuler - Implements the Direct / Forward Euler algorithm instead of the Beeman algorithm
"""

class SolarEuler(Solar):
    def update_pos(self, planet):
        planet.current_accel = self.calc_force(planet) / planet.mass
        # The following is Direct-Euler Formula 1
        next_pos = planet.pos + (planet.velo * self.timestep)
        return next_pos

    def update_velo(self, planet):
        next_accel = self.calc_force(planet) / planet.mass
        # The following is Direct-Euler Formula 2
        next_velo = planet.velo + (planet.current_accel * self.timestep)
        planet.previous_accel = planet.current_accel
        planet.current_accel = next_accel
        return next_velo
