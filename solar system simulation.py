"""Create a simulation of the solar system's major objects"""
import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.animation import FuncAnimation


# Function to generate ellipse points


def generate_ellipse(ellipse_center, x, y, angle, a, b, num_points=100):
    """creates ellipses that are used to represent planetary orbits"""
    theta = np.linspace(0, 2 * np.pi, num_points)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    ellipse_points = np.array([a * cos_theta, b * sin_theta])
    # rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
    #                            [np.sin(angle), np.cos(angle)]])
    rotation_matrix = np.array([[1, 0], [0, 1]])
    rotated_points = np.dot(rotation_matrix, ellipse_points)
    return rotated_points[0] + ellipse_center[0], rotated_points[1] + ellipse_center[1]
    # return center[0], center[1]


# parameters_list

# Function to update the plot


def update(frame, parameters):
    e_s = parameters[0]  # eccentricities
    r_s = parameters[1]  # radii       b = a * np.sqrt(1-e**2)

    for index, (e, r) in enumerate(zip(e_s, r_s)):
        a = r
        b = a * np.sqrt(1 - e ** 2)
        # Calculate new position of the moving point
        x = center[0] + np.cos(np.radians(frame)) * a
        y = center[0] + np.sin(np.radians(frame)) * b
        moving_points[index].set_data(x, y)
        # Update the ellipse
        ellipses[index].set_data(*generate_ellipse(center, x, y, np.radians(frame), a, b))

        # Update the path of the moving point on the ellipse
        path_lines[index].set_data([center[0], x], [center[0], y])

    return moving_points, ellipses, path_lines


# Parameters


center = (0, 0)
semimajor_axis = 5  # Major axis
semiminor_axis = 3  # Minor axis
eccentricity = .224  # Eccentricity
eccentricities = [.206, .007, .017, .094, .049, .052]
radii = [.4, .7, 1, 1.52, 5.2, 9.5]
radius = 1  # Radius of rotation

# Create initial plot
fig, ax = plt.subplots()
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)
moving_points, ellipses, path_lines = [], [], []
for planet_index in range(len(eccentricities)):
    moving_points.append([])
    ellipses.append([])
    path_lines.append([])
    moving_points[planet_index], = ax.plot([], [], 'ro')
    ellipses[planet_index], = ax.plot([], [], 'b')
    path_lines[planet_index], = ax.plot([], [], 'r--')

# Create animation
ax.set_aspect("equal")
# ani = FuncAnimation(fig, update, frames=np.linspace(0, 360, 360),
#                    blit=True, interval=50, fargs=[[eccentricities, radii]])
update(0, [eccentricities, radii])
plt.show()
