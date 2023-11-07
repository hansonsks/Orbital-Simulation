"""
DoomsdayPlanetaryAlignment - Additional Experiment 2: Checks when planets will align within some threshold
"""

from Solar import Solar
from OrbitalPeriod import OrbitalPeriod
import numpy as np
import math


class DoomsdayPlanetaryAlignment:

    def __init__(self, threshold=60):
        self.solar = Solar()
        self.orbit = OrbitalPeriod()    # For the calc_orbital_period function
        self.threshold = threshold

    def get_angle_between_planets(self, p1, p2):
        """ Lecture Slides 7, Page 20, Approach 2 """
        sun_pos = self.solar.get_planet("Sun").pos
        sun_p1_vec = p1.pos - sun_pos
        sun_p2_vec = p2.pos - sun_pos
        angle = math.acos((np.dot(sun_p1_vec, sun_p2_vec)) / (np.linalg.norm(sun_p1_vec) * np.linalg.norm(sun_p2_vec)))
        return angle

    def planets_aligned(self):
        """ Checks when the planets are aligned within some threshold """
        planets_aligned = False
        for p1 in self.solar.planets:
            if (p1.name == "Sun"):  # Ignore the sun
                continue
            for p2 in self.solar.planets:
                # Ignore the sun or if the p1 and p2 are the same planets
                if (p2.name == "Sun" or p1.name == p2.name):
                    continue
                else:
                    if self.get_angle_between_planets(p1, p2) < (self.threshold * math.pi / 180):
                        # print("Angle between " + p1.name + " and " + p2.name + " is " + str(angle_between))
                        planets_aligned = True
                    else:
                        return False
        return planets_aligned

    def write_alignment_year(self):
        """
        Since they start off aligned, run until they are no longer aligned within the threshold
        Then, start counting the years needed for them to align within the threshold again
        """
        self.new_solar = Solar()
        one_earth_year = self.orbit.calc_orbital_period(self.new_solar.get_planet("Earth"))
        while self.planets_aligned():
            self.solar.run_sim()
        self.solar.time_passed = 0

        while not self.planets_aligned():
            self.solar.run_sim()

        alignment_time = self.solar.time_passed / one_earth_year
        doomsday_msg = "The planets aligned within " + str(self.threshold) + " degrees after " + \
                       str(alignment_time) + " years.\n"
        print(doomsday_msg)
        with open("doomsday_alignment.txt", "a") as myTxt:
            myTxt.write(doomsday_msg)
        return (int(self.threshold), alignment_time)

