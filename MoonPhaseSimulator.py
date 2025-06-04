"""Utility functions for visualising the lunar cycle."""

from matplotlib import pyplot as plt
from math import radians, sqrt, cos
import numpy as np

time_period = 29.5
radius = 100


def turn_angle_finder(days_num):
    angle = (360 / time_period) * days_num
    if angle < 360:
        return angle
    else:
        return angle % 360


def dark_side_finder(angle):
    if angle < 180:
        return "left"
    else:
        return "right"


def terminus_side_finder(angle):
    """Return the side on which the terminator should be drawn."""
    # When angle is 0 (new moon) the terminator coincides with the
    # circumference of the moon. In this case we treat it as being on the
    # right so that the full disc is shaded correctly.
    if angle == 0:
        return "right"
    elif 0 < angle <= 90:
        return "right"
    elif 90 < angle <= 180:
        return "left"
    elif 180 < angle <= 270:
        return "right"
    elif 270 < angle <= 360:
        return "left"


def phase_teller(angle):
    if angle == 0 or angle == 360:
        return "New Moon"
    elif angle == 90:
        return "First Quarter"
    elif angle == 180:
        return "Full Moon"
    elif angle == 270:
        return "Last Quarter"
    elif 0 < angle < 90:
        return "Waxing Crescent"
    elif 90 < angle < 180:
        return "Waxing Gibbous"
    elif 180 < angle < 270:
        return "Waning Gibbous"
    elif 270 < angle < 360:
        return "Waning Crescent"


# A function for finding the x coordinates of the moon
def circle_x_generator(y, r):
    return sqrt(r ** 2 - y ** 2)


# A function for finding the x coordinates of the moon’s terminator.
def ellipse_x_generator(y, r, angle):
    radian_angle = radians(angle)
    return abs(r * cos(radian_angle) * sqrt(1 - (y / r) ** 2))


def plot_moon_phase(days, ax=None):
    """Plot the moon phase corresponding to ``days`` since new moon."""
    if ax is None:
        ax = plt.gca()

    y = np.linspace(-radius, radius, 2 * radius + 1)
    circle_x_positive = np.sqrt(radius ** 2 - y ** 2)
    circle_x_negative = -circle_x_positive

    ax.plot(y, circle_x_positive, color="black")
    ax.plot(y, circle_x_negative, color="black")
    ax.axis("square")
    ax.set_xticks([])
    ax.set_yticks([])

    turn_angle = turn_angle_finder(days)
    terminus_side = terminus_side_finder(turn_angle)
    dark_side = dark_side_finder(turn_angle)

    ellipse_x = radius * np.cos(np.radians(turn_angle)) * np.sqrt(1 - (y / radius) ** 2)
    ellipse_x = np.abs(ellipse_x)
    if terminus_side == "left":
        ellipse_x = -ellipse_x

    ax.plot(ellipse_x, y, color="black")

    if dark_side == "right":
        ax.fill_betweenx(y, circle_x_positive, ellipse_x, facecolor="grey")
    else:
        ax.fill_betweenx(y, circle_x_negative, ellipse_x, facecolor="grey")

    title = "Moon phase: " + phase_teller(turn_angle)
    ax.set_title(title)


def animate_moon_cycle(days=time_period, interval=300):
    """Animate the lunar cycle for ``days`` days."""

    fig, ax = plt.subplots()

    from matplotlib.animation import FuncAnimation

    def update(frame):
        ax.cla()
        plot_moon_phase(frame, ax)
        return ax,

    frames = np.linspace(0, days, int(days) + 1)
    FuncAnimation(fig, update, frames=frames, interval=interval, repeat=True)
    plt.show()


def main():
    days = float(input("Enter the number of days since new moon: "))
    plot_moon_phase(days)
    plt.show()


if __name__ == "__main__":
    main()
