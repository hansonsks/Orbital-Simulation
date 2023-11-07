"""
EnergyConservation - Plots a graph that shows the total energy in the solar system (Beeman / Direct Euler)
"""

from Solar import Solar, SolarEuler
import numpy as np
import matplotlib.pyplot as plt


class EnergyConservation:
    def __init__(self, euler=False):
        """ Initialises a Solar system and an array that holds the energy data """
        self.euler = euler
        if self.euler:
            self.solar = SolarEuler()
        else:
            self.solar = Solar()
        self.energies = []

    def calc_total_energy(self):
        """ Calculates the Total Gravitational Potential Energy in the system """
        te = 0
        for planet in self.solar.planets:
            # Kinetic Energy: 1/2 * planet_mass * planet_velocity^2
            ke = (1 / 2) * planet.mass * (np.linalg.norm(planet.velo) ** 2)
            # Potential Energy: -1 * planet_mass * planet_acceleration * distance_of_planet_from_sun
            pe = -planet.mass * (np.linalg.norm(self.solar.calc_force(planet)) / planet.mass) * \
                 np.linalg.norm(planet.pos - self.solar.get_planet("Sun").pos)
            te += (ke + pe)
        self.energies.append(te)

    def run(self):
        if self.euler:
            limit = 5000
        else:
            limit = 500
        while (len(self.energies) < limit):
            self.solar.run_sim()
            self.calc_total_energy()
        plt.plot(self.energies)
        plt.xlabel("Timesteps")
        plt.ylabel("Total Energy (J)")
        plt.title("Total Energy in the Simulation")
        plt.show()
