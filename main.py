import os
import numpy as np
import matplotlib.pyplot as plt

g = 9.81          # m/s^2
m = 280           # kg
h_cg = 0.25       # m
d_wheel = 1.590   # m
psi_front = 0.5

mu = np.linspace(0, 2, 21)


def weight_shift(mu):
    a = mu * g
    return a * m * h_cg / d_wheel


def front_force(mu):
    return mu * (m * g * psi_front + weight_shift(mu))


def rear_force(mu):
    return mu * (m * g * (1 - psi_front) - weight_shift(mu))


front = front_force(mu)
rear = rear_force(mu)

assert np.allclose(front + rear, mu * m * g)

print("mu    front (N)    rear (N)")
for i in range(len(mu)):
    print(f"{mu[i]:.1f}   {front[i]:9.2f}   {rear[i]:9.2f}")

plt.figure(figsize=(12, 6.5), dpi=150)
plt.plot(front, rear)

for k in mu[1:]:
    total = k * m * g
    plt.plot([0, total], [total, 0], color="gray", linestyle=":")
    plt.text(total, 25, f"{k:.1f}", fontsize=7, ha="center")

plt.ylim(0, 1400)
plt.grid(True, color="lightgray")
plt.title("Ideal Brake Curve")
plt.xlabel("Front Brake Force (N)")
plt.ylabel("Rear Brake Force (N)")

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
os.makedirs(folder, exist_ok=True)
plt.savefig(os.path.join(folder, "ideal_braking_curve.png"))
plt.show()
