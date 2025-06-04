import builtins
import importlib
import os
import sys
import types

import pytest


@pytest.fixture(scope="module")
def mps_module():
    # Ensure project root is on sys.path for import
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, project_root)

    input_original = builtins.input
    builtins.input = lambda *args, **kwargs: "0"

    plt = types.SimpleNamespace(
        plot=lambda *a, **k: None,
        axis=lambda *a, **k: None,
        fill_betweenx=lambda *a, **k: None,
        title=lambda *a, **k: None,
        show=lambda *a, **k: None,
    )
    matplotlib = types.SimpleNamespace(pyplot=plt)
    sys.modules['matplotlib'] = matplotlib
    sys.modules['matplotlib.pyplot'] = plt

    module = importlib.import_module("MoonPhaseSimulator")
    yield module

    builtins.input = input_original
    sys.modules.pop('matplotlib', None)
    sys.modules.pop('matplotlib.pyplot', None)
    sys.path.remove(project_root)


def test_turn_angle_finder(mps_module):
    assert mps_module.turn_angle_finder(7.375) == pytest.approx(90.0)
    assert mps_module.turn_angle_finder(0) == 0
    # values over one period should wrap around
    assert mps_module.turn_angle_finder(30) == pytest.approx((360/29.5*30) % 360)


def test_phase_teller(mps_module):
    mps = mps_module
    assert mps.phase_teller(0) == "New Moon"
    assert mps.phase_teller(90) == "First Quarter"
    assert mps.phase_teller(180) == "Full Moon"
    assert mps.phase_teller(270) == "Last Quarter"
    assert mps.phase_teller(45) == "Waxing Crescent"
    assert mps.phase_teller(135) == "Waxing Gibbous"
    assert mps.phase_teller(225) == "Waning Gibbous"
    assert mps.phase_teller(315) == "Waning Crescent"
    assert mps.phase_teller(360) == "New Moon"


def test_terminus_side_finder(mps_module):
    mps = mps_module
    # For a new moon (angle 0) the terminator coincides with the
    # circumference and is treated as being on the right.
    assert mps.terminus_side_finder(0) == "right"
    assert mps.terminus_side_finder(90) == "right"
    assert mps.terminus_side_finder(180) == "left"
    assert mps.terminus_side_finder(270) == "right"
    assert mps.terminus_side_finder(360) == "left"
