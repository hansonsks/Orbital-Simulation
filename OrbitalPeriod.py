"""
OrbitalPeriod - Finds the relative orbital periods of the other planets to Earth
"""

from Solar import Solar
from numpy.linalg import norm
from math import pi


class OrbitalPeriod:
    def __init__(self):
        self.solar = Solar()
        self.orbital_periods_log = "orbital_periods.txt"

    @staticmethod
    def calc_orbital_period(planet):
        """ 2 * pi * orbital_period / time_period """
        if (planet.name == "Sun"):
            return 0
        else:
            return (2 * pi * norm(planet.pos) / norm(planet.velo))

    def get_relative_periods(self):
        """ Get the relative orbital periods of other planets to earth: (planet_orbital_period / earth_orbital_period)"""
        earth_orbital_period = self.calc_orbital_period(self.solar.get_planet("Earth"))
        other_relative_orbit = {}
        for planet in self.solar.planets:
            other_relative_orbit[planet.name] = self.calc_orbital_period(planet) / earth_orbital_period
        return other_relative_orbit

    def write_orbital_periods(self):
        """ Write the relative orbital periods to a file for comparison """
        relative_orbit_periods = self.get_relative_periods()
        with open(self.orbital_periods_log, "a") as orbit_log:
            orbit_log.write("The relative orbital periods of the five inner-most planets to Earth\n")
            for planet in relative_orbit_periods:
                if (planet == "Sun"):
                    continue
                else:
                    orbit_msg = "Earth 1 year = " + str(planet) + " " + \
                                str(round(relative_orbit_periods[planet], 2)) + " years.\n"
                    print(orbit_msg)
                    orbit_log.write(orbit_msg)
            orbit_log.write("This marks the end of one simulation\n\n")
