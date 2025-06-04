# MoonPhaseSimulator

This project simulates the phases of the Moon. The script `MoonPhaseSimulator.py`
can display the phase for a specific day or animate an entire lunar cycle.

Usage examples:

```bash
# Display the phase for 5 days after the new moon
python MoonPhaseSimulator.py --days 5

# Animate a 30‑day lunar cycle
python MoonPhaseSimulator.py --animate --cycle 30
```

The cycle length can be adjusted with `--period`.

Additionally, `threebodysim.py` provides a simple visual simulation of a
three-body gravitational system using matplotlib. The simulation parameters can
be customized:

```bash
python threebodysim.py --steps 3000 --dt 0.005 --limit 15
```
