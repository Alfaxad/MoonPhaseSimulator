import matplotlib
matplotlib.use('Agg')

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MoonPhaseSimulator import terminus_side_finder, simulate_moon_phase


def test_terminus_side_zero_returns_side():
    side = terminus_side_finder(0)
    assert side in ("left", "right")


def test_plotting_angle_zero_runs_without_error():
    fig, ax = simulate_moon_phase(0)
    # three lines: two for the circle and one for the terminus
    assert len(ax.lines) >= 3
    matplotlib.pyplot.close(fig)
