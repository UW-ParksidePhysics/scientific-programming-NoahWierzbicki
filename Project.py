import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Function to generate ellipse points


def generate_ellipse(center, x, y, angle, num_points=100):
    theta = np.linspace(0, 2*np.pi, num_points)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    ellipse_points = np.array([a * cos_theta, b * sin_theta])
    #rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
    #                            [np.sin(angle), np.cos(angle)]])
    rotation_matrix = np.array([[1,0], [0,1]])
    rotated_points = np.dot(rotation_matrix, ellipse_points)
    return rotated_points[0] + center[0], rotated_points[1] + center[1]
    return center[0], center[1]
# Function to update the plot


def update(frame):

    # Calculate new position of the moving point
    x = center[0] + np.cos(np.radians(frame)) * a
    y = center[0] + np.sin(np.radians(frame)) * b
    moving_point.set_data(x, y)

    # Update the ellipse
    ellipse.set_data(*generate_ellipse(center, x, y, np.radians(frame)))

    # Update the path of the moving point on the ellipse
    path_line.set_data([center[0], x], [center[0], y])

    return moving_point, ellipse, path_line

# Parameters


center = (0, 0)
a = 5  # Major axis
b = 3  # Minor axis
eccentricity = .206  # Eccentricity
radius = 1  # Radius of rotation

# Create initial plot
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
moving_point, = ax.plot([], [], 'ro')
ellipse, = ax.plot([], [], 'b')
path_line, = ax.plot([], [], 'r--')

# Create animation
ax.set_aspect("equal")
ani = FuncAnimation(fig, update, frames=np.linspace(0, 360, 360),
                    blit=True, interval=50)

plt.show()
