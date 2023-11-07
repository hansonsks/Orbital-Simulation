from EnergyConservation import EnergyConservation
from OrbitalPeriod import OrbitalPeriod
from DoomsdayPlanetaryAlignment import DoomsdayPlanetaryAlignment
from HohmannAnimation import HohmannAnimation
from Hohmann import Hohmann
from Solar import Solar
import math
import matplotlib.pyplot as plt


def main():
    print("Enter 1 for the Energy Conservation Graph")
    print("Enter 2 for the Orbital Periods results to be written to \"orbital_periods.txt\"")
    print("Enter 3 for the Planetary Alignment Text Results (Printed in Console + Written to \"doomsday_alignment.txt\" + "
          "Plot)")
    print("Enter 4 for the Hohmann Transfer Animation (Mostly hard-coded values to satisfy Hohmann Transfer assumptions)")
    print("Enter 5 for the results of the Hohmann Transfer Experiment "
          "(See ideal angle and initial velocity for launching the satellite, and "
          "the period of elliptical orbit of the satellite in the console)")
    print("Enter 6 for the animation of the Solar System (with or without Jupiter)")
    print("Enter 7 for the Energy Conservation Graph using the Direct Euler method")
    print("Enter 0 to Exit")
    print("Note that 3 and 5 are very very slow and take hours to compute the results")

    while True:
        experiment = int(input("Which experiment do you want to see? "))
        if (experiment == 1):
            e = EnergyConservation()
            e.run()

        elif (experiment == 2):
            o = OrbitalPeriod()
            o.write_orbital_periods()

        elif (experiment == 3):
            print("This will take a long time to load")
            print("If you want to check it, "
                  "bump it up to range(30, 51, 5) or above (with large intervals) to save time instead")
            print("FYI running range(5, 61, 1) takes around 3-4 hours (See results in doomsday_alignment.txt)")
            alignment_angles = []
            alignment_years = []
            for threshold in range(10, 61, 5):
                p = DoomsdayPlanetaryAlignment(threshold)
                angle, year = p.write_alignment_year()
                alignment_angles.append(angle)
                alignment_years.append(year)
            plt.plot(alignment_angles, alignment_years)
            plt.xlabel("Threshold")
            plt.ylabel("Alignment Year")
            plt.title("Doomsday Planet Alignment Experiment Results")
            plt.show()

        elif (experiment == 4):
            h = Hohmann()
            ideal_angle = h.get_ideal_angle()
            response = input("Full orbit? 'y' or 'n'   (Shows that at its current rate it will become space debris) ")
            full_orbit = False
            if response.lower() == 'y':
                full_orbit = True
            elif response.lower() == 'n':
                full_orbit = False
            ha = HohmannAnimation(angle=ideal_angle, full_orbit=full_orbit)
            ha.run_sim()

        elif (experiment == 5):
            satellite_angles = []
            satellite_distances = []
            g = Hohmann()
            g.get_ideal_angle()
            g.get_initial_velocity()
            g.get_satellite_orbital_period()
            print("It will take some time to compute data for the graph, maybe a few hours.")
            for i in range(40, 51):
                h = Hohmann()
                angle, distance = h.satellite_sim(i * math.pi / 180.0)
                satellite_angles.append(i)
                satellite_distances.append(distance)
            print(satellite_angles)
            print(satellite_distances)
            plt.plot(satellite_angles, satellite_distances)
            plt.xlabel("Launch Angles")
            plt.ylabel("Distance between the Satellite and Mars (km)")
            plt.title("Hohmann Transfer Experiment Results")
            plt.show()

        elif (experiment == 6):
            s = Solar()
            response = input(("Do you want to see Jupiter in the animation? ('y' = yes; 'n' = no): "))
            if (response.lower() == 'y'):
                s.run()
            elif (response.lower() == 'n'):
                s.planets = s.planets[:-1]
                s.run()
            else:
                print("Please enter 'y' or 'n'")

        elif (experiment == 7):
            se = EnergyConservation(euler=True)
            se.run()

        elif (experiment == 0):
            print("Goodbye!")
            break

        else:
            print("Please enter a valid number (1 - 7) or 0 to Exit")


if __name__ == "__main__":
    main()
