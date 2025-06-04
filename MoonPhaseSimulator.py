from matplotlib import pyplot as plt
from math import radians, sqrt, cos

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
    """Return the illuminated side of the terminator.

    Parameters
    ----------
    angle : float
        The angular position in degrees. Values outside the ``0-360`` range
        are normalised so that negative angles or multiples of ``360`` are
        correctly mapped.

    Returns
    -------
    str
        ``"left"`` or ``"right"`` depending on the quadrant. ``0`` degrees is
        considered ``"right"`` so that a new moon still yields a valid side.
    """

    normalised = angle % 360
    if 0 <= normalised <= 90:
        return "right"
    elif 90 < normalised <= 180:
        return "left"
    elif 180 < normalised <= 270:
        return "right"
    else:
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


# A function for finding the x coordinates of the moon's terminus
def ellipse_x_generator(y, r, angle):
    radian_angle = radians(angle)
    return abs(r * cos(radian_angle) * sqrt(1 - (y / r) ** 2))


def simulate_moon_phase(days):
    """Generate a matplotlib figure for the given number of days."""
    y = list(range(-radius, radius + 1))
    circle_x_positive = [circle_x_generator(num, radius) for num in y]
    circle_x_negative = [-num for num in circle_x_positive]

    fig, ax = plt.subplots()
    ax.plot(y, circle_x_positive, color="black")
    ax.plot(y, circle_x_negative, color="black")
    ax.axis("square")

    turn_angle = turn_angle_finder(days)
    terminus_side = terminus_side_finder(turn_angle)
    dark_side = dark_side_finder(turn_angle)

    ellipse_x = []
    if terminus_side == "right":
        ellipse_x = [ellipse_x_generator(num, radius, turn_angle) for num in y]
    elif terminus_side == "left":
        ellipse_x = [-ellipse_x_generator(num, radius, turn_angle) for num in y]

    if ellipse_x:
        ax.plot(ellipse_x, y, color="black")

    if dark_side == "right":
        ax.fill_betweenx(y, circle_x_positive, ellipse_x, facecolor="grey")
    elif dark_side == "left":
        ax.fill_betweenx(y, circle_x_negative, ellipse_x, facecolor="grey")

    ax.set_title("Moon phase: " + phase_teller(turn_angle))
    return fig, ax


if __name__ == "__main__":
    days = float(input("Enter the number of days since new moon: "))
    simulate_moon_phase(days)
    plt.show()
