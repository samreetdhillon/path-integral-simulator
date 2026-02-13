import sys
import os

# Adds the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from core.samplers.metropolis import local_update

# --- 1. Simulation Parameters ---
N = 100            # Number of lattice sites (Euclidean time points)
a = 0.5            # Lattice spacing
m = 1.0            # Mass
lambda_poly = 0.0  # Set to 0 for pure Harmonic Oscillator
step_size = 1.5    # Metropolis proposal width
n_sweeps = 50000   # Total Monte Carlo iterations
n_thermal = 5000   # Discard initial steps to reach equilibrium

# --- 2. Initialization ---
# Start with a "cold" configuration (all zeros)
path = np.zeros(N)
data = []

print(f"Starting PIMC for QHO (N={N}, a={a})")

# --- 3. The Monte Carlo Loop ---
for sweep in tqdm(range(n_sweeps)):
    # Updated signature: local_update(path, a, m, thermal_step_size, pot_type, lambd)
    acc_rate = local_update(path, a, m, step_size, 0, lambda_poly)
    
    # Only collect data after thermalization
    if sweep > n_thermal and sweep % 10 == 0:
        # We store all points in the path as samples of the wavefunction
        data.extend(path.copy())

# --- 4. Visualization & Validation ---
plt.figure(figsize=(10, 6))

# Histogram of sampled positions
count, bins, _ = plt.hist(data, bins=100, density=True, alpha=0.7, label='PIMC Samples')

# Analytical Ground State: psi(x)^2 = sqrt(m*w/pi) * exp(-m*w*x^2)
# For QHO, omega = 1
x_theory = np.linspace(min(bins), max(bins), 500)
psi_sq = np.sqrt(1.0/np.pi) * np.exp(-x_theory**2)
plt.plot(x_theory, psi_sq, 'r--', lw=2, label='Analytical Ground State')

plt.title("Probability Density: PIMC vs. Theory (QHO)")
plt.xlabel("Position x")
plt.ylabel("P(x)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()