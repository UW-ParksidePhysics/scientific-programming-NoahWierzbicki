'''
This program takes two dates as inuput, and calculates the distance of
Pluto and Neptue from the Sun throught the interval.

Currently, the dates are automatically set to Jan 1 of 1900 and 2600
as this is an interesting range, showing the previous crossing of the
boides and the next two in the upcoming 600 years. It plots this information.

The program also calculates the rate of change (of distance) of Pluto and Neptune,
and their accelerations based on Newton's law of gravitation. It should be
understood that rate of change is the rate at which their distances change
in relation to the Sun, not their actual velocities.

The distances are plotted in a graph for visualization. For the calculated
distances at and crossing points, this information is printed in a table
and a list for simple, more precise reading.
'''
from skyfield.api import load, Loader
import matplotlib.pyplot as plt
from scipy.constants import G
import numpy as np
from tabulate import tabulate


def get_date_input(prompt, ts):
    # Prompt the user for date input
    # Currently unused. Program instead automatically sets years to 1900 and 2600
    while True:
        print(prompt)
        try:
            year = int(input("Enter the year, must be from 1550-2650 or 1969-17191 (AD): "))
            month = int(input("Enter the month (MM), e.g., 07 for July: "))
            day = int(input("Enter the day (DD), e.g., 15: "))
            # For BC dates, we need to subtract one because there is no year 0 in the astronomical year numbering.
            # BC dates are deprecated, ephamaris files do not contain BC information.
            year = year if year > 0 else year - 1
            date = ts.utc(year, month, day)
            return date
        except ValueError as e:
            print(f"Invalid date entered: {e}")


def select_ephemeris_file(date1, date2, ephemeris_files):
    # Select the appropriate ephemeris file based on the date range
    # Given 1900-2600, will always select de440.bsp
    year1, year2 = date1.utc[0], date2.utc[0]
    for file_name, (start_year, end_year) in ephemeris_files.items():
        if start_year <= year1 <= end_year and start_year <= year2 <= end_year:
            return file_name
    return None


def calculate_celestial_distance(ephemeris, celestial_body_name, date):
    # Calculate the distance from the Sun to a celestial body
    sun = ephemeris['sun']
    celestial_body = ephemeris[celestial_body_name]
    distance = sun.at(date).observe(celestial_body).distance().au
    return distance


def calculate_velocities(dates, distances):
    # Calculate velocities using the central difference method
    velocities = [None]  # No velocity for the first date
    for i in range(1, len(dates) - 1):
        time_diff = (dates[i + 1].tt - dates[i - 1].tt) * 24 * 3600  # Time difference in seconds
        distance_diff = distances[i + 1] - distances[i - 1]  # Distance difference in AU
        velocity = distance_diff / time_diff  # Velocity in AU/s
        velocities.append(velocity * 149597870.7 * 1000)  # Convert AU/s to m/s
    velocities.append(None)  # No velocity for the last date
    return velocities


def calculate_gravitational_force(mass_body, mass_sun, distance):
    # Calculate gravitational force using Newton's law of universal gravitation
    force = G * mass_body * mass_sun / (distance * 149597870.7e3) ** 2  # Convert AU to meters for the distance
    return force


def calculate_acceleration(force, mass_body):
    # Calculate acceleration based on force and mass
    acceleration = (force / mass_body) * 1000000  # Acceleration in micrometers/s^2
    return acceleration


def print_distance_table(years, neptune_distances, neptune_velocities, neptune_accelerations, pluto_distances,
                         pluto_velocities, pluto_accelerations):
    # Print a table of distances, velocities, and accelerations
    # The first and final velocities and accelerations are ommitted
    table = zip(years, neptune_distances, neptune_velocities, neptune_accelerations, pluto_distances, pluto_velocities,
                pluto_accelerations)
    headers = ["Year", "Neptune Distance (AU)", "Neptune RoC (m/s)", "Neptune Acceleration (µ/s²)",
               "Pluto Distance (AU)", "Pluto RoC (m/s)", "Pluto Acceleration (µ/s²)"]
    print(tabulate(table, headers=headers, floatfmt=".2f", missingval="N/A"))


def print_closer_intervals(year_labels, neptune_distances, pluto_distances):
    # Print intervals when Pluto was closer to the Sun than Neptune
    intervals = []
    i = 1
    while i < len(year_labels) - 1:
        if pluto_distances[i] < neptune_distances[i]:
            start_year = year_labels[i]
            while i < len(year_labels) - 1 and pluto_distances[i] < neptune_distances[i]:
                i += 1
            end_year = year_labels[i]
            intervals.append((start_year, end_year))
        i += 1

    print("\nIntervals when Pluto was closer to the Sun than Neptune:")
    for start, end in intervals:
        print(f"From {start:.2f} to {end:.2f}")


def find_intersections(x, y1, y2):
    # Find intersections between two curves
    intersections = []
    for i in range(len(x) - 1):
        if (y1[i] - y2[i]) * (y1[i + 1] - y2[i + 1]) < 0:
            x_intersect = x[i] + (x[i + 1] - x[i]) * (y2[i] - y1[i]) / ((y1[i + 1] - y1[i]) - (y2[i + 1] - y2[i]))
            y_intersect = np.interp(x_intersect, x, y1)
            intersections.append((x_intersect, y_intersect))
    return intersections


def main():
    # Initialize the loader and timescale
    loader = Loader('~/.skyfield-data', verbose=False)
    ts = loader.timescale()

    # Define ephemeris files with their supported year ranges
    ephemeris_files = {
        'de440s.bsp': (1849, 2150),
        'de440.bsp': (1550, 2650),
        'de441.bsp': (1969, 17191)
    }

    # User normally enters dates, instructed to remove input ability
    # Using range Jan 1 1900 to Jan 1 2600 to show currently relevant periods
    # date1 = get_date_input("Enter the first date:", ts)
    # date2 = get_date_input("Enter the second date:", ts)
    date1 = ts.utc(1900, 1, 1)
    date2 = ts.utc(2600, 1, 1)

    if date2.tt < date1.tt:
        date1, date2 = date2, date1

    file_name = select_ephemeris_file(date1, date2, ephemeris_files)
    if file_name:
        ephemeris = loader(file_name)
        print(f"Loaded {file_name} for the date range.")
    else:
        print("No ephemeris file covers the entire date range entered.")
        exit()

    # Calculate intervals and dates for plotting
    year_splits = 2.5  # 2.5-year intervals to make plot smooth without lag. Can be chaned to impact performance.
    days_difference = abs(date2.tt - date1.tt)
    intervals = max(1, int(days_difference / 365.25 / year_splits))
    intervals = intervals + 1 if days_difference % (365.25 * 5) != 0 else intervals

    dates = [date1 + (date2 - date1) * (i / intervals) for i in range(intervals + 1)]

    try:
        neptune_distances = [calculate_celestial_distance(ephemeris, 'neptune barycenter', date) for date in dates]
        pluto_distances = [calculate_celestial_distance(ephemeris, 'pluto barycenter', date) for date in dates]
    except Exception as e:
        print(f"Error calculating distances: {e}")
    else:
        neptune_velocities = calculate_velocities(dates, neptune_distances)
        pluto_velocities = calculate_velocities(dates, pluto_distances)

        mass_pluto = 1.30900e22
        mass_neptune = 1.024e26
        mass_sun = 1.989e30

        neptune_forces = [
            calculate_gravitational_force(mass_neptune, mass_sun, distance) if distance is not None else None for
            distance in neptune_distances]
        neptune_accelerations = [calculate_acceleration(force, mass_neptune) if force is not None else None for force in
                                 neptune_forces]

        pluto_forces = [calculate_gravitational_force(mass_pluto, mass_sun, distance) if distance is not None else None
                        for distance in pluto_distances]
        pluto_accelerations = [calculate_acceleration(force, mass_pluto) if force is not None else None for force in
                               pluto_forces]

        year_labels = np.linspace(start=date1.utc.year, stop=date2.utc.year, num=len(dates))

        intersections = find_intersections(year_labels, neptune_distances, pluto_distances)

        # Start of Output #
        print("\n_______________________________________")
        print("Start of Output")
        print("Rate of change is calculated by central difference method w/neighbor positions.")
        print("Acceleration is calculated by Newton's law of universal gravitation w/masses of bodies & Sun.")
        print("_______________________________________\n")
        print("Pluto vs Neptune: Distance from the Sun w/RoC + Acceleration\n")

        # Print Tableable
        print_distance_table(year_labels, neptune_distances, neptune_velocities, neptune_accelerations, pluto_distances,
                             pluto_velocities, pluto_accelerations)

        # Prints intervals on which Pluto is closer to the Sun than Neptune
        print_closer_intervals(year_labels, neptune_distances, pluto_distances)

        # Calculate the difference in distances
        distance_difference = np.array(pluto_distances) - np.array(neptune_distances)

        # Set up the figure and subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

        # Plot the first graph: Orbital distances over time
        ax1.plot(year_labels, neptune_distances, label='Neptune')
        ax1.plot(year_labels, pluto_distances, label='Pluto')
        for intersect in intersections:
            ax1.plot(intersect[0], intersect[1], 'o', color='pink')
            ax1.text(intersect[0], intersect[1], f'  {intersect[0]:.2f}', verticalalignment='bottom', color='pink')
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Distance (AU)')
        ax1.set_title('Distance from the Sun to Neptune and Pluto over Time')
        ax1.legend()
        ax1.grid(True)

        # Plot the second graph: Distance difference over time
        ax2.plot(year_labels, distance_difference, label='Pluto - Neptune Distance Difference', color='purple', linewidth=5)
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Distance Difference (AU)')
        ax2.set_title('Distance Difference Between Pluto and Neptune over Time (1900-2600)')
        ax2.legend()
        ax2.grid(True)

        # Adjust layout
        plt.tight_layout()

        # Show the plots
        plt.show()


if __name__ == "__main__":
    main()