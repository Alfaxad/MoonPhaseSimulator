"""Simple three body gravitational simulation with animation."""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


G = 1.0


@dataclass
class Body:
    mass: float
    position: np.ndarray
    velocity: np.ndarray


def _accelerations(positions: np.ndarray, masses: np.ndarray) -> np.ndarray:
    """Compute accelerations on each body due to every other body."""
    n = len(masses)
    acc = np.zeros_like(positions)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            r = positions[j] - positions[i]
            dist = np.linalg.norm(r)
            acc[i] += G * masses[j] * r / (dist ** 3 + 1e-9)
    return acc


def _step(positions: np.ndarray, velocities: np.ndarray, masses: np.ndarray, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """Advance the system by one time step using velocity Verlet."""
    acc = _accelerations(positions, masses)
    positions = positions + velocities * dt + 0.5 * acc * dt * dt
    acc_new = _accelerations(positions, masses)
    velocities = velocities + 0.5 * (acc + acc_new) * dt
    return positions, velocities


def simulate(bodies: list[Body], steps: int = 1000, dt: float = 0.01):
    """Animate the motion of ``bodies`` under mutual gravity."""

    masses = np.array([b.mass for b in bodies])
    positions = np.array([b.position for b in bodies], dtype=float)
    velocities = np.array([b.velocity for b in bodies], dtype=float)

    fig, ax = plt.subplots()
    ax.set_aspect("equal", "box")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    colors = ["tab:red", "tab:blue", "tab:green"]
    points = [ax.plot([], [], "o", color=c)[0] for c in colors]

    def update(frame):
        nonlocal positions, velocities
        positions, velocities = _step(positions, velocities, masses, dt)
        for i, p in enumerate(points):
            p.set_data(positions[i, 0], positions[i, 1])
        return points

    FuncAnimation(fig, update, frames=steps, interval=30, blit=True)
    plt.show()


def main():
    bodies = [
        Body(1.0, np.array([-1.0, 0.0]), np.array([0.0, 0.3])),
        Body(1.0, np.array([1.0, 0.0]), np.array([0.0, -0.3])),
        Body(1.0, np.array([0.0, 0.0]), np.array([0.0, 0.0])),
    ]
    simulate(bodies)


if __name__ == "__main__":
    main()

