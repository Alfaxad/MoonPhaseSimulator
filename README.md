# MoonPhaseSimulator
Simulate the moon-phase (the appearance and the name of the phase) days after the New Moon phase!

This repository also contains a simple three body simulation and an animated
visualisation of the full lunar cycle.

## Running the tests

This project uses `pytest` for its unit tests. After installing the dependencies,
run the tests from the repository root with:

```bash
pytest
```

## Usage

The classic command line interface remains available by running

```bash
python MoonPhaseSimulator.py
```

To watch the entire lunar cycle animated over 29.5 days:

```bash
python -c "import MoonPhaseSimulator as mps; mps.animate_moon_cycle()"
```

Additional helper functions are available for programmatic use:

```python
import MoonPhaseSimulator as mps
mps.illumination_fraction(7)      # fraction illuminated after 7 days
mps.days_until_next_full_moon(10) # time until the next full moon
```

Run the three body simulation with:

```bash
python threebodysim.py
```
