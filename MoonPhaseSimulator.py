"""Moon phase simulator with optional animation of a full lunar cycle."""

import argparse
from math import radians, sqrt, cos
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Default lunar cycle period in days
DEFAULT_PERIOD = 29.5
RADIUS = 100

y = list(range(-RADIUS, RADIUS + 1))
CIRCLE_X_POSITIVE = [sqrt(RADIUS ** 2 - yy ** 2) for yy in y]
CIRCLE_X_NEGATIVE = [-xx for xx in CIRCLE_X_POSITIVE]


def turn_angle_finder(days_num, period=DEFAULT_PERIOD):
    """Return the Moon's angle in degrees at a given day of the cycle."""
    angle = (360 / period) * days_num
    return angle % 360


def dark_side_finder(angle):
    """Which side of the Moon is dark at a given angle."""
    return "left" if angle < 180 else "right"


def terminus_side_finder(angle):
    """Determine whether the terminator is on the left or right."""
    if 0 < angle <= 90:
        return "right"
    if 90 < angle <= 180:
        return "left"
    if 180 < angle <= 270:
        return "right"
    return "left"


def phase_teller(angle):
    """Return the textual moon phase for a given angle."""
    if angle in (0, 360):
        return "New Moon"
    if angle == 90:
        return "First Quarter"
    if angle == 180:
        return "Full Moon"
    if angle == 270:
        return "Last Quarter"
    if 0 < angle < 90:
        return "Waxing Crescent"
    if 90 < angle < 180:
        return "Waxing Gibbous"
    if 180 < angle < 270:
        return "Waning Gibbous"
    return "Waning Crescent"


def ellipse_x_generator(y_val, r, angle):
    """X-coordinate of the terminator for a given y value and angle."""
    radian_angle = radians(angle)
    return abs(r * cos(radian_angle) * sqrt(1 - (y_val / r) ** 2))


def plot_single_phase(days, period):
    """Plot the moon phase for a single day."""
    angle = turn_angle_finder(days, period)
    terminus_side = terminus_side_finder(angle)
    dark_side = dark_side_finder(angle)

    ellipse_x = [
        ellipse_x_generator(yy, RADIUS, angle) if terminus_side == "right" else -ellipse_x_generator(yy, RADIUS, angle)
        for yy in y
    ]

    fig, ax = plt.subplots()
    ax.plot(y, CIRCLE_X_POSITIVE, color="black")
    ax.plot(y, CIRCLE_X_NEGATIVE, color="black")
    ax.plot(ellipse_x, y, color="black")

    if dark_side == "right":
        ax.fill_betweenx(y, CIRCLE_X_POSITIVE, ellipse_x, facecolor="grey")
    else:
        ax.fill_betweenx(y, CIRCLE_X_NEGATIVE, ellipse_x, facecolor="grey")

    ax.set_aspect("equal", "box")
    ax.set_title(f"Moon phase: {phase_teller(angle)}")
    plt.show()


def animate_cycle(cycle_days=30, period=DEFAULT_PERIOD, interval=300):
    """Animate moon phases over an entire cycle."""
    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        angle = turn_angle_finder(frame, period)
        terminus_side = terminus_side_finder(angle)
        dark_side = dark_side_finder(angle)
        ellipse_x = [
            ellipse_x_generator(yy, RADIUS, angle) if terminus_side == "right" else -ellipse_x_generator(yy, RADIUS, angle)
            for yy in y
        ]
        ax.plot(y, CIRCLE_X_POSITIVE, color="black")
        ax.plot(y, CIRCLE_X_NEGATIVE, color="black")
        ax.plot(ellipse_x, y, color="black")
        if dark_side == "right":
            ax.fill_betweenx(y, CIRCLE_X_POSITIVE, ellipse_x, facecolor="grey")
        else:
            ax.fill_betweenx(y, CIRCLE_X_NEGATIVE, ellipse_x, facecolor="grey")
        ax.set_aspect("equal", "box")
        ax.set_xlim(-RADIUS, RADIUS)
        ax.set_ylim(-RADIUS, RADIUS)
        ax.set_title(f"Day {frame}: {phase_teller(angle)}")
        ax.axis('off')

    ani = FuncAnimation(fig, update, frames=range(cycle_days), interval=interval, repeat=True)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moon phase simulator")
    parser.add_argument("--days", type=float, help="Days since new moon to display")
    parser.add_argument("--animate", action="store_true", help="Animate an entire lunar cycle")
    parser.add_argument("--cycle", type=int, default=30, help="Number of days in the animated cycle")
    parser.add_argument("--period", type=float, default=DEFAULT_PERIOD, help="Length of lunar cycle in days")
    args = parser.parse_args()

    if args.animate:
        animate_cycle(args.cycle, args.period)
    else:
        if args.days is None:
            days = float(input("Enter the number of days since new moon: "))
        else:
            days = args.days
        plot_single_phase(days, args.period)
