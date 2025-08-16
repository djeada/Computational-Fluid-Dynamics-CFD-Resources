import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic data for the plots

# Data for Figure 3
t = np.linspace(0.9, 1.1, 500)
u_a = 3 * np.sin(20 * t) + np.random.normal(0, 2, t.shape)
u_b = 3 * np.cos(20 * t) + np.random.normal(0, 2, t.shape)

# Data for Figure 4
u_prime_a = np.random.normal(0, 2, 1000)
u_prime_b = 0.5 * u_prime_a + np.random.normal(0, 2, 1000)

# Unit vector for Figure 5
phi = np.array([0.894, 0.447])
u_proj = np.dot(np.vstack((u_prime_a, u_prime_b)).T, phi)

# Plot for Figure 3
plt.figure(figsize=(8, 6))
plt.plot(t, u_a, label=r"$u'_a$", color="blue")
plt.plot(t, u_b, label=r"$u'_b$", color="red")
plt.xlabel(r"$t\ (s)$")
plt.ylabel(r"$u'\ (m/s)$")
plt.title("Longitudinal velocity fluctuations $u'(t)$ at positions (a) and (b).")
plt.legend()
plt.show()

# Plot for Figure 4
plt.figure(figsize=(8, 6))
plt.scatter(u_prime_a, u_prime_b, s=10, alpha=0.5)
plt.xlabel(r"$u'_a\ (m/s)$")
plt.ylabel(r"$u'_b\ (m/s)$")
plt.title("Raw data plotted on a plane.")
plt.show()

# Plot for Figure 5
plt.figure(figsize=(8, 6))
plt.scatter(u_prime_a, u_prime_b, s=10, alpha=0.5, label="Data")
plt.scatter(u_prime_a, u_proj, s=10, alpha=0.5, color="red", label="Proj on $\Phi$")
plt.plot(
    u_prime_a,
    phi[1] / phi[0] * u_prime_a,
    color="black",
    label=r"$\Phi=(0.894, 0.447)$",
)
plt.xlabel(r"$u'_a\ (m/s)$")
plt.ylabel(r"$u'_b\ (m/s)$")
plt.title("Raw data projected on unit vector $\Phi$.")
plt.legend()
plt.show()
