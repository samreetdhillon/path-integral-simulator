import sys
import os

# Adds the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import numpy as np
import matplotlib.pyplot as plt
from core.samplers.metropolis import local_update 
# Note: Ensure metropolis.py is calling double_well_potential!
from tqdm import tqdm

# Parameters for Double Well
N, a, m = 100, 0.5, 1.0
V0, a_param = 0.5, 2.0  # Barrier height and distance of minima
n_sweeps = 100000

path = np.zeros(N)
data = []

print("Simulating Quantum Tunneling in a Double Well...")

# --- The Monte Carlo Loop ---
for s in tqdm(range(n_sweeps)):
    # Updated signature: local_update(path, a, m, thermal_step_size, pot_type, lambd, V0, a_dw)
    # pot_type=1 triggers the double_well_potential logic
    acc_rate = local_update(path, a, m, 1.5, 1, 0.0, V0, a_param)
    
    if s > 5000 and s % 10 == 0:
        data.extend(path.copy())

# Plotting the "Bimodal" Distribution
plt.figure(figsize=(10, 6))
plt.hist(data, bins=100, density=True, color='purple', alpha=0.7)
plt.title("Probability Density: Double Well (Quantum Tunneling)")
plt.xlabel("Position x")
plt.ylabel("P(x)")
plt.grid(True, alpha=0.3)
plt.show()