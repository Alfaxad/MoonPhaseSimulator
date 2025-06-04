import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

G = 1.0  # Gravitational constant in arbitrary units
DT = 0.01  # Time step
STEPS = 5000


class Body:
    def __init__(self, mass, position, velocity, color="C0"):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color


bodies = [
    Body(1000.0, [0.0, 0.0], [0.0, 0.0], "yellow"),
    Body(1.0, [10.0, 0.0], [0.0, 3.2], "blue"),
    Body(0.1, [12.0, 0.0], [0.0, 3.5], "red"),
]


def accelerations(bodies):
    acc = [np.zeros(2) for _ in bodies]
    for i, b1 in enumerate(bodies):
        for j, b2 in enumerate(bodies):
            if i == j:
                continue
            r = b2.position - b1.position
            dist = np.linalg.norm(r)
            acc[i] += G * b2.mass * r / dist**3
    return acc


def step(bodies, dt):
    acc = accelerations(bodies)
    for body, a in zip(bodies, acc):
        body.velocity += a * dt / 2
    for body in bodies:
        body.position += body.velocity * dt
    acc = accelerations(bodies)
    for body, a in zip(bodies, acc):
        body.velocity += a * dt / 2


fig, ax = plt.subplots()
ax.set_aspect("equal")
limit = 20
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
points = [ax.plot([], [], "o", color=b.color)[0] for b in bodies]


def init():
    for p in points:
        p.set_data([], [])
    return points


def update(frame):
    step(bodies, DT)
    for p, b in zip(points, bodies):
        p.set_data(b.position[0], b.position[1])
    return points


ani = FuncAnimation(fig, update, frames=range(STEPS), init_func=init, blit=True, interval=20)
plt.show()
