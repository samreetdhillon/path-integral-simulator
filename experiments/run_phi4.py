import sys
import os

# Adds the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Main script for Phi^4 theory
import numpy as np
import matplotlib.pyplot as plt
from core.samplers.field_metropolis import field_local_update
from tqdm import tqdm

# Parameters
L = 32           # Lattice size (LxL)
lambd = 1.0      # Coupling
m_sq = -2.0      # Negative mass squared triggers symmetry breaking!
step_size = 0.5
n_sweeps = 10000

field = np.zeros((L, L))
magnetization = []

print(f"Simulating Phi^4 Theory on {L}x{L} lattice...")

# --- The Monte Carlo Loop ---
for s in tqdm(range(n_sweeps)):
    # Match the new signature: field_local_update(field, m_sq, lambd, step_size, pot_type)
    # We use pot_type=0 for the Phi^4 potential
    field_local_update(field, m_sq, lambd, step_size, 0)
    
    if s > 1000: # Post-thermalization
        magnetization.append(np.mean(field))

# Visualization
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(field, cmap='RdBu')
plt.title(f"Field Configuration (m^2={m_sq})")
plt.colorbar()

plt.subplot(1, 2, 2)
plt.plot(magnetization)
plt.title("Order Parameter <phi> over time")
plt.xlabel("Sweep")
plt.ylabel("Mean Field")

plt.tight_layout()
plt.show()