"""
Hohmann - Calculates the best angle and initial velocity to launch a satellite to Mars, how long it takes to reach Mars,
          and returns the closest distance between the satellite and Mars for a given launch angle
"""

from Solar import Solar
from Planet import Planet
from OrbitalPeriod import OrbitalPeriod
import numpy as np
import math


class Hohmann:
    def __init__(self):
        self.solar = Solar(timestep=1000)
        self.solar.planets = self.solar.planets[:-1]    # Removes Jupiter
        self.orbit = OrbitalPeriod()
        self.sun = self.solar.get_planet("Sun")
        self.earth = self.solar.get_planet("Earth")
        self.mars = self.solar.get_planet("Mars")
        self.satellite = None

    def calc_semi_major_axis(self, p1, p2):
        return (1 / 2) * (np.linalg.norm(p1.pos - self.sun.pos) + np.linalg.norm(p2.pos - self.sun.pos))

    def calc_elliptical_orbit(self, p1, p2):
        return math.sqrt((self.calc_semi_major_axis(p1, p2) ** 3) * ((math.pi ** 2) * 4) / (self.solar.G * self.sun.mass))

    def calc_phase_angle(self, p1, p2):
        return (1 - 2 * ((self.calc_elliptical_orbit(p1, p2) / 2) / self.orbit.calc_orbital_period(p2))) * math.pi

    def calc_transfer_velo(self, p1, p2):
        r1 = np.linalg.norm(p1.pos - self.sun.pos)
        r2 = np.linalg.norm(p2.pos - self.sun.pos)
        return math.sqrt(2 * self.solar.G * self.sun.mass * (r2 / (r1 * (r1 + r2)))) * (p1.velo / np.linalg.norm(p1.velo))

    def calc_clockwise_angle(self, planet):
        sun_p_vec = planet.pos - self.sun.pos
        angle = math.atan2(sun_p_vec[1], sun_p_vec[0])
        return (2 * math.pi + angle) if angle < 0 else angle

    def satellite_sim(self, angle):
        """ Launches a Satellite (as a Planet object) from the given angle on Earth """
        satellite_angle = round(angle + math.pi, 4)
        while (self.solar.time_passed < 2 * self.orbit.calc_orbital_period(self.earth)):
            self.solar.run_sim()
        mars_angle = round(self.calc_clockwise_angle(self.mars) - self.calc_clockwise_angle(self.earth), 4)
        while (satellite_angle != mars_angle):  # Rounding Error may cause issues
            self.solar.run_sim()
            mars_angle = round(self.calc_clockwise_angle(self.mars) - self.calc_clockwise_angle(self.earth), 4)

        # Initialise a Satellite as a Planet
        satellite_pos = (-1) * self.earth.pos
        satellite_velo = (-1) * self.calc_transfer_velo(self.earth, self.mars)
        self.satellite = Planet(self.solar.G, "Satellite", 10000, satellite_pos, satellite_velo, 10, "green")
        self.solar.planets.append(self.satellite)

        # Find the closest distance between the Satellite and Mars
        closest_distance = 1e99
        while (self.solar.time_passed < self.solar.time_passed + self.calc_elliptical_orbit(self.earth, self.mars)):
            self.solar.run_sim()
            satellite_mars_distance = np.linalg.norm(self.mars.pos - self.satellite.pos)
            if (satellite_mars_distance < closest_distance):
                closest_distance = satellite_mars_distance
        angle_fired = (mars_angle - math.pi) * 180 / math.pi
        closest_distance /= 1000    # Convert m to km
        return (angle_fired, closest_distance)

    def get_ideal_angle(self):
        ideal_angle = self.calc_phase_angle(self.earth, self.mars) * 180 / math.pi
        print("Ideal launch angle: " + str(ideal_angle) + "°")
        return ideal_angle

    def get_satellite_orbital_period(self):
        satellite_orbital_period = self.calc_elliptical_orbit(self.earth, self.mars) / (24 * 60 ** 2)
        print("Orbital Period of the Satellite: " + str(satellite_orbital_period) + " days")
        return satellite_orbital_period

    def get_initial_velocity(self):
        initial_velo = self.calc_transfer_velo(self.earth, self.mars)
        print("The initial velocity needed: " + str(initial_velo[1] / 1000) + " km/s")
        return initial_velo
